from media_downloader.instagram import download_instagram
from media_downloader.twitter import download_twitter


def _download(url: str, directory: str = '.'):
    directory = directory.strip().strip('"')
    url = url.strip()
    if not directory:
        directory = '.'

    if "twitter" in url:
        download_twitter(url, directory)
    if "instagram" in url:
        download_instagram(url, directory)


if __name__ == "__main__":
    _download(url=input('User link: '), directory=input('Directory: '))

# TODO fix twitter image resolve
# TODO twitter video
# TODO test coverage