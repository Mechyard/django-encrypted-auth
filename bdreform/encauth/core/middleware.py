class AuditLogMiddleware:
    """
    Provide audit trace functionality to all incoming and outgoing
    requests and allows for easy logging of request information.
    """
    def __init__(self, response_func):
        self.response_func = response_func

    def __call__(self, request):
        request = self.pre_process(request)
        response = self.response_func(request)
        response = self.post_process(response)
        return response

    def pre_process(self, request):
        #todo: log request related trace information
        return request

    def post_process(self, response):
        #todo: log response related trace information
        return response


class E2EEncryptionMiddleware:
    """
    Provides end-to-end encryption between data transmitted from the system and data
    received by the system. All subscribing system will be enforced to implement the
    end-to-end encryption for valid data transmission.

    This will reduce the risk of man-in-middle attacks and will reduce data listening
    effectiveness.

    This will be compute intensive to maintain so not recommended for use in systems
    which do not require such high level of security.
    """
    def __init__(self, response_func):
        self.response_func = response_func

    def __call__(self, request):
        request = self.pre_process(request)
        response = self.response_func(request)
        response = self.post_process(response)
        return response

    def pre_process(self, request):
        #todo: unscramble request body
        return request

    def post_process(self, response):
        #todo: scramble response body
        return response
