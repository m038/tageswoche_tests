SERVER_URL = "https://tw-dev:SoFab@tw-reloaded.lab.sourcefabric.org/"
DEFAULT_BLOG = 1

ADMIN_LOGIN = "admin"
ADMIN_PASS = "a"

USER_LOGIN = "user"
USER_PASS = "u"

ADMIN_URI = "/content/lib/core/start.html"
EMBED_URI = "/content/lib/livedesk-embed/index.html"
ADMIN_ANCHORS = {
    'users': '#/users',
    'live-blog': '#/live-blog/{0}',
    'live-blog-config': '#live-blog/{0}/config',
}

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
