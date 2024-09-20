import datetime
import os
import subprocess
import pandas
import zipfile


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    datadir = 'C:/Dev/nextclade-tools/'

    # files with a lower/earlier file name will not be processed
    earliest_file_prefix = "ALL-2023-12-23"

    # for running nextclade using release definition data
    nextclade_cmd_template = 'nextclade run --input-dataset ' + \
        datadir + 'data\sars-cov-2 -q --output-tsv=' + \
        datadir + 'output\[filename].tsv ' + \
        datadir + 'input\[filename].fasta'

    # for running nextclade using nightly definition data
    nextclade_cmd_template = 'nextclade run -d sars-cov-2 --input-tree nightly.json -q --output-tsv=' + \
        datadir + 'output\[filename].tsv ' + \
        datadir + 'input\[filename].fasta'
    
    needed_columns = ['seqName', 'clade', 'Nextclade_pango', 'partiallyAliased']

    for file in os.listdir(datadir + 'input'):
        filename = os.fsdecode(file)
        # only process files on or after the specified start file name
        if filename >= earliest_file_prefix:
            delete_this_fasta_after = False

            # unzip each input .zip file, only if a matching output .tsv file does not exist.
            if filename.endswith('.zip') and not os.path.exists(str.replace(datadir + 'output/' + filename, ".fasta.zip", ".tsv")):
                delete_this_fasta_after = True
                print (str(datetime.datetime.now()) + ' Unzipping: ' + filename)
                with zipfile.ZipFile(datadir + 'input/' + filename, 'r') as zip_ref:
                    zip_ref.extractall(datadir + 'input')
            
                filename = str.replace(filename,".zip", "")

            # process each input .fasta file, only if a matching output .tsv file does not exist.
            if filename.endswith('.fasta') and not os.path.exists(str.replace(datadir + 'output/' + filename, ".fasta", ".tsv")):
                nextclade_cmd = str.replace(nextclade_cmd_template, "[filename]", str.replace(filename,".fasta", ""))
                print (str(datetime.datetime.now()) + ' Calling: ' + nextclade_cmd)
                subprocess.call (nextclade_cmd, shell=True)
                
                # uncomment this section to trim the output columns
                # filename_tsv = str.replace(filename,".fasta", ".tsv")
                # print (str(datetime.datetime.now()) + ' Dropping columns from: ' + filename_tsv)
                # df1 = pandas.read_csv(datadir + "output/" + filename_tsv, usecols = needed_columns, sep="\t")
                # df1.to_csv(datadir + "output/" + filename_tsv, index=False, sep="\t" )

            if delete_this_fasta_after:
                print (str(datetime.datetime.now()) + ' Deleting: ' + filename)
                os.remove(datadir + 'input/' + filename)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()