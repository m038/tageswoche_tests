class ApiException(Exception):

    def __init__(self, url, response, exception, *args, **kwargs):
        result_message = """URL: {url}
Response: {response}
Error: "{exception}: {message}"
        """.format(
            url=url,
            response=response,
            exception=exception.__class__.__name__, message=exception.message
        )
        super(ApiException, self).__init__(result_message, *args, **kwargs)
