# Corrected workbook: row-level data inventory

**Source:** `data/Information_for_Baris_corrected.xlsx` (three sheets). The inventory file is `ouput/csv/row_level_data_inventory.csv`; it contains one row per peptide per result block and records source cell locations, sequences, replicate values, and any matching third-sheet category row.

## Data-resolution decisions applied

- The corrected workbook changes third-sheet category row identifier `S19` to `SP19`, `Ηigh` to `High`, and `Np` to `No`. Those corrections are present in the corrected data. This records the corrected labels as given; it does not independently validate the biological meaning or provenance of the categorical ratings.
- The numeric result value **0** is retained as the number `0` (not converted to missing). It occurs at `Results!B9`, SP9, Blot 2, replicate 1. This is the observed value; the workbook does not verify that zero means no detection.
- For this inventory, peptide ordering in each “ranked” results block is interpreted as **right-to-left descending by average fold change across that block’s listed replicates**, per the stated working assumption. In ordinary left-to-right workbook order, this appears ascending by mean. Replicate values are kept unchanged; rank is a column-order convention, not an independently verified ranking calculation. For mean ties or any departures from the assumption, inspect the raw values.
- Replicate observations are represented as replicate-labelled rows under each peptide column. The inventory serializes their source cells into replicate 1–4 fields; it does not assert whether replicates are biological or technical.

## Structure and reconciliation

- **32 distinct main-screen peptides** are present in sequence inventory rows 5–36 of `Information for feeding`, and each appears once across Blot 1–3, with 3 replicate measurements per peptide.
- **7 validation-blot peptide entries** (SP2, SP3, SP32, SP26, SP5, SP19, SP4) each have 4 replicate measurements. These IDs also occur in the main-screen result blocks and sequence inventory.
- Therefore the CSV has **39 peptide-by-result-block rows** (32 main + 7 validation), representing 39 distinct block/peptide combinations, not 39 unique peptides.
- The third sheet has category data for **4 corrected IDs**: SP3, SP5, SP19, SP26. These match sequence IDs and result IDs. Category fields are copied as categories, not converted to numerical outcomes.
- Peptides without third-sheet category rows have blank category fields in the inventory; this means no row is listed for that peptide in that small table, not “No” category.

## Column and cell-reference conventions

CSV columns include peptide ID, sequence-sheet row reference, AA and nucleotide sequence, result block, result header cell, up to four replicate source cell/value pairs, third-sheet category row reference, and the seven protein-category columns. Cell references are fully qualified, for example `Results!B9` and `SP and other collagen proteins!A5`.

See `ouput/csv/row_level_data_inventory.csv` for the row-level mapping. The source values have not been summarized, recalculated, or imputed in that file.
