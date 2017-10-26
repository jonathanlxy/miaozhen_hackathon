import requests
from .parser import PostbackError

class URL_downloader:
    def __init__(self, save_folder=None):
        if save_folder:
            self.save_folder = save_folder

    def get_url_list(self, save_file=None, download_url=None, test=True):
        if test:
            url_postback = open('Demo_William/init_test_url.csv').read()
        else:
            url_postback = requests.get(download_url)
        #### TODO: Condition for intermission (which returns the
        #### seconds to next open window)
        if not url_postback.ok:
            raise PostbackError
        else:
            # Save the raw URL list
            if (self.save_folder and save_file):
                filename = '{}/{}'.format(self.save_folder, save_file)
                with open(filename, 'wb') as f:
                    f.write(url_postback.content)
            # Parse URL into a list (TODO: error handler)
            url_list = url_postback.text.split('\n')
            return url_list

if __name__ == '__main__':
    download_url = 'http://hackathon.mzsvn.com/download.php'
    downloader = URL_downloader(save_folder=cfg['URL_SAVE_FOLDER'])
    url_list = downloader.get_url_list(
        save_file=cfg['URL_SAVE_FILE'],
        download_url=download_url,
        test=False)[70:90]
    url_list = get_url_list(download_url, test=False)
