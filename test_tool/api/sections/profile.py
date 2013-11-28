from test_tool.api.api_call import api_get_with_auth
from test_tool.settings import USER_MAIL, USER_PASS


def profile(session, email=USER_MAIL, password=USER_PASS):
    return api_get_with_auth('/api/profile', email=email, password=password, session=session)
