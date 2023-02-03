# nextclade-tools
Python scripts and notes for running the [nextclade cli tool](https://nextclade.org). Nextclade produces lineage classifications from genomic sequencing data, e.g. the [GISAID](https://gisaid.org) database of SARS-CoV-2 sequences. Nextclade's lineages are considered more accurate by most experts, and the classification configuration is updated faster for new lineages.

These scripts were built on Windows Server, using [python](https://python.org) 3.11. The only package dependency is pandas.

# Setup / config steps

1. Pull from github or create a base folder e.g. C:\dev\nextclade-tools, with subfolders data, input and output.
2. Download the nextclade cli executable file into that folder. Usually it's filename includes the version number e.g. `nextclade-x86_64-pc-windows-gnu.exe` - rename to nextclade.exe for convenience.
3. Download the latest nextclade config by running this command line > `nextclade dataset get --name "sars-cov-2" --output-dir "data/sars-cov-2"`
4. Run the script **nextclade-tree-to-text.py** - this produces a flattened tsv file version of the nextclade tree as data/sars-cov-2/tree.tsv

# Run steps

1. Check for any [updates to the nextclade config](https://github.com/nextstrain/nextclade_data/releases), if there has been a release, re-run **Setup / config** steps 3 onwards.
2. Download your .fasta files into the input sub-folder. If you want to process the "All sequences" FASTA archive, you can use the script **nextclade-unpack-input.py** to unpack the .tar.xz file.
3. Run the script **nextclade-run.py**. This will produce .tsv files in the output sub-folder. The script deletes all but a few key columns. Note this script will skip any files that already exist in the output sub-folder (ignoring the file extension).
4. If you have processed the "All sequences" FASTA archive, the output sequences.tsv file has an issue with the seqName column format. This is fixed by the script: **nextclade-fix-seqName.py**, which looks up the expected seqName values from a GISAID metadata file (should be the same age or more recent than the "All sequences" FASTA archive).

# Environment requirements

Rough run times, on a 8 vcpu Windows Server machine:
- 2 hours - download and unpack the "All sequences" FASTA archive (once off)
- 15 hours - reprocess the "All sequences" FAST archive (once or twice a month)
- 1 min/day - process the FASTA files for one day of submissions

Processing the "All sequences" FASTA archive needs around 450GB free disk space (as of early 2023).  Daily data for the global GISAID sequences requires around 400MB per day.

I downloaded the "All sequences" FASTA archive once, and then have downloaded the daily FASTA data since.

When the nextclade config is updated (typically once or twice per month), I delete all the files in the output subfolder and carry out the **Run steps** above to re-categorise all lineages.

# Other scripts

## nextclade-tree-to-text.py
This script turns the lineage tree in the nextclade configuration data into a text file format, for easier processing with other tools.  It should be re-run each time the updated nextclade config is downloaded, see Setup step 3 above.
