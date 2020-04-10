import json
from re import findall

from url_downloader import get_resource, save_file
from downloader import create_user_dir


def _get_last_tweet_id(html_data: str) -> str:
    """
    Find the id of the last tweet in html page
    :param html_data: Html page
    :return: Tweet id
    """
    tweet_ids = findall(r'data-tweet-id="([^"]*)', html_data)
    if tweet_ids:
        return tweet_ids[-1]
    else:
        raise ValueError


def _get_next_page(user: str, html_last_page: str) -> str:
    """
    Get the next media "page", when scrolling down
    :param user: Twitter user name
    :param html_last_page: Previous html page
    :return: Next html page
    """
    # Find last ID and make request
    last_tweet_id = _get_last_tweet_id(html_last_page)
    url = "https://twitter.com/i/profiles/show/%s/media_timeline?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false" % (
        user, last_tweet_id)
    # Retrieve html from the json response
    data = json.loads(get_resource(url))
    return data['items_html']


def download_twitter(url: str, directory: str = '.'):
    """
    Download all media of the twitter user.
    :param directory: Directory to save media in
    :param url: Url of the twitter user's page
    """

    # Get twitter user, and download media page
    user = findall('twitter.com/([^/]*)', url)[0]
    url = 'https://twitter.com/%s/media' % user
    html = get_resource(url)
    print(url)
    if not html:
        raise ValueError('Invalid twitter user')

    user_dir = create_user_dir(directory, user)

    while html:
        # Get image urls and save each
        image_urls = findall(r'data-aria-label-part src="([^"]*)', html)
        if image_urls:
            for image_url in image_urls:
                save_file(image_url, user_dir)
                print(image_url)


        html = _get_next_page(user, html)
        video_urls = findall(r'(<video[^<]*)', html)
        if video_urls:
            print(video_urls)

# TODO videos on twitter