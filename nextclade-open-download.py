import datetime
import os
import pathlib
import requests
import tarfile
import zstandard

def download_file(file_url, local_dir):
    # Get the filename from the URL
    filename = os.path.basename(file_url)
    local_path = os.path.join(local_dir, filename)

    # Download the file
    response = requests.get(file_url)

    # Save the file to the local directory
    with open(local_path, "wb") as file:
        file.write(response.content)
    print(str(datetime.datetime.now()) + f"Downloaded {filename} to {local_dir}")


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    datadir = 'C:/Dev/nextclade-tools/open/'
    root_url = 'https://data.nextstrain.org/files/ncov/open/'
    file_download_list = [
        'metadata.tsv.zst',
        'nextclade.tsv.zst'
    ]

    for filename in file_download_list:
        download_file(root_url + filename, datadir)
        # process each input .fasta file, only if a matching output .tsv file does not exist.
        if filename.endswith('.zst'):
            print (str(datetime.datetime.now()) + ' Decompressing: ' + filename)
            zst_file = pathlib.Path(datadir + filename)
            with open(zst_file, 'rb') as compressed:
                decomp = zstandard.ZstdDecompressor()
                output_path = pathlib.Path(datadir) / zst_file.stem
                with open(output_path, 'wb') as destination:
                    decomp.copy_stream(compressed, destination)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
