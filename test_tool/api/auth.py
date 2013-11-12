from requests import Session
from urlparse import urljoin
import hashlib
import hmac
import json

from test_tool.settings import SERVER_URL, ADMIN_LOGIN, ADMIN_PASS
from test_tool.api.exceptions import ApiException

#@TODO: rewrite it according to newscoop auth

def log_in(username=ADMIN_LOGIN, password=ADMIN_PASS, session=None):
    if session == None:
        session = Session()

    step1_url = urljoin(SERVER_URL, '/resources/Security/Authentication')
    step1 = session.post(
        url=step1_url,
        data={
            'userName': username,
        }
    )
    try:
        step1_answer = json.loads(step1.text)
    except ValueError as e:
        raise ApiException(step1_url, step1.text, e)
    try:
        token = step1_answer['Token']
    except KeyError as e:
        raise ApiException(step1_url, step1.text, e)

    sha_password = hashlib.sha512(password).hexdigest()
    hashed_username = hmac.new(
        username,
        sha_password,
        hashlib.sha512
    ).hexdigest()
    hashed_token = hmac.new(
        bytes(hashed_username),
        bytes(token),
        hashlib.sha512
    ).hexdigest()

    step2_url = urljoin(SERVER_URL, '/resources/Security/Authentication/Login')
    step2 = session.post(
        url=step2_url,
        data={
            'UserName': username,
            'Token': token,
            'HashedToken': hashed_token
        }
    )
    try:
        step2_answer = json.loads(step2.text)
    except ValueError as e:
        raise ApiException(step2_url, step2.text, e)
    try:
        session_key = step2_answer['Session']
        user = step2_answer['User']
    except KeyError as e:
        raise ApiException(step2_url, step2.text, e)

    result = {
        'session_key': session_key,
        'session': session,
        'user': user,
    }
    return result
