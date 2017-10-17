# import requests
# download_url = "http://hackathon.mzsvn.com/download.php"
#
class URL_downloader:
    def __init__(self, save_path):
        self.path = save_path

    def get_url_list(self, file_name, download_url=None, test=True):
        if test:
            url_raw = open('Demo/init_test_url.csv').read()
        else:
            url_raw = requests.get(download_url)
        # Save the raw URL list
        filename = '{}/{}'.format(self.path, file_name)
        with open(filename, 'wb') as f:
            f.write(url_raw)

        # Read URL (TODO: error handler)
        url_list = url_raw.split('\n')
        return url_list