import json
from requests import Session
from urlparse import urljoin

from test_tool.settings import SERVER_URL
from test_tool.api.auth import log_in
from test_tool.api.exceptions import ApiException


def session_dict_wrapper(session_dict=None):
    if session_dict is None:
        session_dict = {}
    #if 'session_key' not in session_dict:
    #    session_dict = log_in()
    if 'session' not in session_dict:
        session_dict['session'] = Session()
    return session_dict


def api_call(function):

    def wrapper(session_dict = None, *args, **kwargs):
        session_dict = session_dict_wrapper(session_dict)
        return function(session_dict, *args, **kwargs)

    return wrapper


def make_api_call(session_dict, type, uri, auth=True, data=None, **kwargs):
    session_dict = session_dict_wrapper(session_dict)
    if auth:
        uri = uri + '&Authorization={session_key}'.format(session_key=session_dict['session_key'])
    url = urljoin(SERVER_URL, uri)
    session = session_dict['session']
    response = session.request(type, url, data=data, verify=False, **kwargs)
    try:
        return json.loads(response.text)
    except ValueError as e:
        raise ApiException(url, response.text, e)

def api_get(uri, session_dict=None, auth=False, session=None):
    if session_dict is None:
        session_dict={}
        session_dict['session'] = Session()
    return make_api_call(session_dict, 'GET', uri, auth)
