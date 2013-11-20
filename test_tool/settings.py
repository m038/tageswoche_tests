SERVER_URL = "http://www.tageswoche.ch/"
PRODUCTION = True
ADMIN_LOGIN = "admin"
ADMIN_MAIL = "admin"
ADMIN_PASS = "a"
USER_LOGIN = "user"
USER_MAIL = "user"
USER_PASS = "u"
BLOGGER_LOGIN = "blogger"
BLOGGER_MAIL = "blogger"
BLOGGER_PASS = "b"

ADMIN_URI = "/admin"

DEFAULT_WAIT = 0.5

WAIT_FOR_AJAX = 1.5
MAX_FOR_AJAX = 3
LONG_AJAX = 30

MAX_WAIT = 10

WEBDRIVER = "firefox"

DEBUG=False

try:
    from settings_local import *
except Exception:
    pass
