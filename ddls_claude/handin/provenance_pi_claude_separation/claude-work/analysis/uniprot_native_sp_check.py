#!/usr/bin/env python3
"""Compare every supplied signal peptide with its native UniProt sequence.

The thesis identifies all 32 peptides as native B. subtilis 168 signal peptides amplified from
genomic DNA. If that is so, each supplied sequence should match the UniProt SIGNAL feature of
its source protein exactly. Any systematic departure - in particular the uniform A-S-A ending
found across all 32 - would mean the library was engineered rather than inherited, which
changes how the C-region constant should be interpreted.

Queries the UniProt REST API for reviewed B. subtilis 168 (taxid 224308) entries by gene name.
Network data is parsed as data only.

Outputs are written beneath ddls_claude/analysis/.
"""
from pathlib import Path
import json
import time
import urllib.parse
import urllib.request

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TAXID = 224308  # Bacillus subtilis subsp. subtilis str. 168

SP_GENE = {
    'SP1': 'amyE', 'SP2': 'aprE', 'SP3': 'bpr', 'SP4': 'epr', 'SP5': 'mpr', 'SP6': 'pel',
    'SP7': 'penP', 'SP8': 'phoA', 'SP9': 'phoB', 'SP10': 'vpr', 'SP11': 'xynA',
    'SP12': 'ybdN', 'SP13': 'ylqB', 'SP14': 'yncM', 'SP15': 'yoaW', 'SP16': 'yocH',
    'SP17': 'yqxI', 'SP18': 'yvgO', 'SP19': 'ywaD', 'SP20': 'yweA', 'SP21': 'ywtF',
    'SP22': 'yxaL', 'SP23': 'nprB', 'SP24': 'sacB', 'SP25': 'sacC', 'SP26': 'abnA',
    'SP27': 'bglS', 'SP28': 'yolA', 'SP29': 'csn', 'SP30': 'bsn', 'SP31': 'cwlO',
    'SP32': 'eglS',
}

FIELDS = 'accession,id,gene_names,protein_name,sequence,ft_signal'


def query(gene):
    q = f'gene:{gene} AND organism_id:{TAXID} AND reviewed:true'
    url = ('https://rest.uniprot.org/uniprotkb/search?'
           + urllib.parse.urlencode({'query': q, 'fields': FIELDS, 'format': 'json',
                                     'size': 5}))
    req = urllib.request.Request(url, headers={'User-Agent': 'ddls-project-analysis'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def signal_end(entry):
    for f in entry.get('features', []):
        if f.get('type') == 'Signal':
            return f['location']['end']['value']
    return None


mine = pd.read_csv(ROOT / 'ouput' / 'analysis' / 'step3' / 'peptide_features.csv')
seqs = dict(zip(mine.peptide_id, mine.aa_sequence))

rows = []
for pid, gene in SP_GENE.items():
    rec = dict(peptide_id=pid, gene=gene, supplied_sequence=seqs[pid],
               supplied_length=len(seqs[pid]), supplied_last3=seqs[pid][-3:])
    try:
        res = query(gene)
        hits = res.get('results', [])
        # Prefer the hit whose primary gene name matches exactly.
        best = None
        for h in hits:
            names = [g.get('geneName', {}).get('value', '') for g in h.get('genes', [])]
            if any(n.lower() == gene.lower() for n in names):
                best = h
                break
        best = best or (hits[0] if hits else None)
        if best is None:
            rec.update(status='no UniProt hit')
        else:
            full = best['sequence']['value']
            end = signal_end(best)
            rec.update(
                accession=best.get('primaryAccession'),
                uniprot_has_signal_annotation=end is not None,
                native_signal_length=end,
                native_signal_sequence=full[:end] if end else '',
                native_last3=full[:end][-3:] if end else '',
                mature_first3=full[end:end + 3] if end else '',
                status='ok',
            )
    except Exception as exc:                                    # network/parse failures
        rec.update(status=f'error: {type(exc).__name__}')
    rows.append(rec)
    time.sleep(0.25)

df = pd.DataFrame(rows)

# Comparisons
df['exact_match'] = df.apply(
    lambda r: bool(r.get('native_signal_sequence')) and
              r.supplied_sequence == r.native_signal_sequence, axis=1)
df['length_difference'] = df.native_signal_length - df.supplied_length
df['c_terminus_differs'] = df.apply(
    lambda r: bool(r.get('native_last3')) and r.supplied_last3 != r.native_last3, axis=1)

df.to_csv(OUT / 'uniprot_native_sp_comparison.csv', index=False)

ok = df[df.status == 'ok']
print(f'Queried {len(df)} genes; {len(ok)} resolved; '
      f'{int(ok.uniprot_has_signal_annotation.fillna(False).sum())} have a SIGNAL annotation.')
print(f'Exact matches to the native signal peptide: {int(df.exact_match.sum())} of {len(df)}')
print()

ann = ok[ok.uniprot_has_signal_annotation == True]
if len(ann):
    print('Native C-terminal tripeptide (positions -3,-2,-1) in UniProt:')
    print(ann.native_last3.value_counts().to_string())
    print(f'\nSupplied C-terminal tripeptide: '
          f'{df.supplied_last3.value_counts().to_dict()}')
    print(f'\nPeptides whose C-terminus differs from native: '
          f'{int(ann.c_terminus_differs.sum())} of {len(ann)}')
    print()
    cols = ['peptide_id', 'gene', 'accession', 'supplied_length', 'native_signal_length',
            'length_difference', 'supplied_last3', 'native_last3', 'exact_match']
    print(ann[cols].to_string(index=False))

missing = df[df.status != 'ok']
if len(missing):
    print('\nUnresolved:')
    print(missing[['peptide_id', 'gene', 'status']].to_string(index=False))

print(f'\nWrote {OUT / "uniprot_native_sp_comparison.csv"}')
