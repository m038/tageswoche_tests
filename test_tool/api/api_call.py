import json
from requests import Session
from urlparse import urljoin

from test_tool.settings import SERVER_URL, USER_LOGIN, USER_PASS
from test_tool.api.exceptions import ApiException


def make_api_call(session, type, uri, params=None, data=None, **kwargs):
    url = urljoin(SERVER_URL, uri)
    response = session.request(type, url, data=data, verify=False, params=params, **kwargs)
    try:
        return json.loads(response.text)
    except ValueError as e:
        raise ApiException(url, response.text, e)


def api_get(uri, session=None, params=None):
    if session is None:
        session = Session()
    return make_api_call(session, 'GET', uri, params=params)


def api_get_with_auth(uri, session=None, auth=False, params=None, username=USER_LOGIN, password=USER_PASS):
    if params is None:
        params = {}
    params['username'] = username
    params['password'] = password
    if session is None:
        session = Session()
    return make_api_call(session, 'GET', uri, params=params)


def api_post_with_auth(uri, session=None, auth=False, data=None, username=USER_LOGIN, password=USER_PASS, **kwargs):
    if data is None:
        data = {}
    data['username'] = username
    data['password'] = password
    if session is None:
        session = Session()
    return make_api_call(session, 'POST', uri, data=data, **kwargs)
