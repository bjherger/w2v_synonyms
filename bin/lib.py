import logging
import os
import requests


def download_file(url, local_file_path, filename):
    """
    Download the file at `url` in chunks, to the location at `local_file_path`
    :param url: URL to a file to be downloaded
    :type url: str
    :param local_file_path: Path to download the file to
    :type local_file_path: str
    :param filename: Filename to save the data to
    :type filename: str
    :return: The path to the file on the local machine (same as input `local_file_path`)
    :rtype: str
    """
    logging.info('Downloading file from url: {}, to path: {}'.format(url, local_file_path))
    # Reference variables
    chunk_count = 0
    local_file_path = os.path.expanduser(local_file_path)
    if not os.path.exists(local_file_path):
        os.makedirs(local_file_path)

    local_file_path = os.path.join(local_file_path, filename)

    # Open output file
    if not os.path.exists(local_file_path):
        with open(local_file_path, 'wb') as open_file:

            # Create connection to the stream
            request = requests.get(url, stream=True)

            # Iterate through chunks of file
            for chunk in request.iter_content(chunk_size=1048576):

                logging.debug('Downloading chunk: {} for file: {}'.format(chunk_count, local_file_path))

                # If there is a chunk to write to file, write it
                if chunk:
                    open_file.write(chunk)

                # Increase chunk counter
                chunk_count = chunk_count + 1

        request.close()
    return local_file_path
