import os
import shutil
from requests import Session
from urlparse import urljoin

from test_tool.logger import logger
from test_tool.api.exceptions import ApiException
from test_tool.settings import USER_MAIL, USER_PASS, SERVER_URL
from test_tool.helpers.selenium_stuff import id_generator


def upload_picture(session, message='test', subject='test', email=USER_MAIL, password=USER_PASS, path_to_image=None):
    if session is None:
        session = Session()

    delete_after = False
    if path_to_image is None:
        delete_after = True
        path_to_image = os.path.join(os.path.dirname(__file__), './{0}.png'.format(id_generator()))
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "../../test.png"), path_to_image)
    logger.debug('UPLOADING IMAGE {0}'.format(path_to_image))

    uri = '/api/feedback'
    try:
        with open(path_to_image) as image_file:
            response = session.post(
                url=urljoin(SERVER_URL, uri),
                files={'image_data': image_file},
                data={
                    'username': email,
                    'password': password,
                    'message': message,
                    'subject': subject,
                },
                verify=False,
            )
    finally:
        if delete_after:
            os.remove(path_to_image)

    if response.text not in ['', ' ']:
        raise ApiException(uri, response.text, Exception('wrong answer'))
