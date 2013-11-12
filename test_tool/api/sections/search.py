from test_tool.api.api_call import api_get

def search(query):
    return api_get('/api/search?query_string={query}'.format(query=query))
