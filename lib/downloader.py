import requests

def url_saver(url_raw, save_file):
    # Save the raw URL list
    with open(save_file, 'w') as f:
        f.write(url_raw)

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
        url_saver(url_raw, filename)

        # Parse URL into a list (TODO: error handler)
        url_list = url_raw.split('\n')

        return url_list

if __name__ == '__main__':
    download_url = 'http://hackathon.mzsvn.com/download.php'
    url_list = get_url_list(download_url, test=False)
