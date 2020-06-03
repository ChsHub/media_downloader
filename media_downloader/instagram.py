import json
from os.path import exists, join
from re import findall
from urllib.parse import quote

from url_downloader import save_file, get_resource
from media_downloader.downloader import create_user_dir


def _get_page_data(page_id, end_cursor=""):
    if end_cursor:
        next_page_query = '{"id":"%s","first":%s,"after":"%s"}' % (page_id, 12, end_cursor)
    else:
        next_page_query = '{"id":"%s","first":%s}' % (page_id, 12)

    next_page_query = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=' + quote(
        next_page_query)

    data = get_resource(next_page_query)
    data = json.loads(data)['data']['user']['edge_owner_to_timeline_media']

    end_cursor = data['page_info']['end_cursor']
    return data, end_cursor


def _download_node(data, user_dir):
    if data['is_video']:
        url = data['video_url']
        file_name = url.split('?')[-2].split('/')[-1]
    else:
        url = data['display_resources'][-1]['src']
        file_name = url.split('?')[-2].split('/')[-1]

    if not exists(join(user_dir, file_name)):
        save_file(url=url, file_path=user_dir, file_name=file_name)
    print(url)


def download_instagram(url: str, directory: str = '.'):
    """
    Download all media of the twitter user.
    :param directory: Directory to save media in
    :param url: Url of the twitter user's page
    """
    user = findall('instagram.com/([^/]*)', url)[0]
    user_dir = create_user_dir(directory, user)

    html = get_resource(url)  # from website
    page_id = findall('owner":{"id":"(\d*)"', html)[0]

    data, end_cursor = _get_page_data(page_id)
    while True:
        for image_data in data['edges']:
            image_data = image_data['node']

            if 'edge_sidecar_to_children' in image_data:
                print(len(image_data['edge_sidecar_to_children']['edges']))
                # Side cars
                for image_data in image_data['edge_sidecar_to_children']['edges']:
                    image_data = image_data['node']
                    _download_node(image_data, user_dir)
            else:
                _download_node(image_data, user_dir)

        if not data['page_info']['has_next_page']:
            return
        data, end_cursor = _get_page_data(page_id, end_cursor)
