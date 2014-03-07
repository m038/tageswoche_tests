import re
from test_tool.helpers.actions.frontend.playlists import goto_playlist


def get_current_publication(browser):
    try:
        pub_id = re.findall('.*/de/(.*)/basel/', browser.current_url)[0]
    except Exception:
        goto_playlist(browser, 'basel')
        pub_id = re.findall('.*/de/(.*)/basel/', browser.current_url)[0]
    return pub_id
