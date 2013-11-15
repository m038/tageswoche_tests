from test_tool.api.api_call import api_get_with_auth
from test_tool.settings import USER_LOGIN, USER_PASS

def profile(session, username=USER_LOGIN, password=USER_PASS):
    return api_get_with_auth('/api/profile', username=username, password=password, session=session)
