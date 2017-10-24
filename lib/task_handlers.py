# import requests
# download_url = "http://hackathon.mzsvn.com/download.php"

def result_dump(result_list, path):
    '''
    Dump the list into a file, separated by \n
    '''
    with open(path, 'w') as f:
        for res in result_list:
            f.write('{}\n'.format(res))

class URL_downloader:
    def __init__(self, save_folder):
        self.save_folder = save_folder

    def get_url_list(self, save_file, download_url=None, test=True):
        if test:
            url_raw = open('Demo_William/init_test_url.csv').read()
        else:
            url_raw = requests.get(download_url)
        # Save the raw URL list
        filename = '{}/{}'.format(self.save_folder, save_file)
        with open(filename, 'w') as f:
            f.write(url_raw)

        # Read URL (TODO: error handler)
        url_list = url_raw.split('\n')
        return url_list

