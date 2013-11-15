from test_tool.api.api_call import api_get

def search(session, query):
    return api_get('/api/search', params={'query_string': query}, session=session)
