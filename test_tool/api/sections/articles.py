from test_tool.api.api_call import api_get


def list(session, section_id):
    return api_get('/api/articles/list', params={'section_id': section_id}, session=session)
