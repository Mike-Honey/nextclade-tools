# nextclade-tools
Python scripts and notes for running the [nextclade cli tool](nextclade.org). Nextclade produces lineage classifications from genomic sequencing data, e.g. the GISAID database of SARS-CoV-2 sequences. Nextclade's lineages are considered more accurate by most experts, and the classification configuration is updated faster for new lineages.

These scripts were built on Windows Server, using [python](python.org) 3.11. The only package dependency is pandas.

# Setup / config steps

1. Create a base folder e.g. C:\dev\nextclade, with subfolders data, input and output.
2. Download and extract nextclade exe file into that folder. Usually it's filename includes the version number - rename to nextclade.exe for convenience.
3. Download the latest nextclade config by running this command line > nextclade dataset get --name "sars-cov-2" --output-dir "data/sars-cov-2"

# Run steps

1. Check for any [updates to the nextclade config](https://github.com/nextstrain/nextclade_data/releases), if needed re-run step 3 from Setup above.
2. Download your .fasta files into the input sub-folder. If you want to process the "All sequences" FASTA archive, you can use the script nextclade-unpack-input.py to unpack the .tar.xz file.
4. Run the script nextclade-run.py. This will produce .tsv files in the output sub-folder. The script deletes all but a few key columns. Note this script will skip any files that already exist in the output sub-folder (ignoring the file extension).
5. If you have processed the "All sequences" FASTA archive, the output sequences.tsv file has an issue with the seqName column format. This is fixed by the script: nextclade-fix-seqName.py, which looks up the expected seqName values from a GISAID metadata file.

# Environment requirements

Rough run times, on a 8 vcpu machine:
- 2 hours - download and unpack the "All sequences" FASTA archive (once off)
- 15 hours - reprocess the "All sequences" FAST archive (once or twice a months)

Processing the "All sequences" FASTA archive needs around 400GB free disk space.  Daily data for the global GISAID sequences requires around 
