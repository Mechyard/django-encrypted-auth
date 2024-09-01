import logging
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from django.conf import settings


class AuditLogMiddleware:
    """
    Provide audit trace functionality to all incoming and outgoing
    requests and allows for easy logging of request information.
    """
    def __init__(self, response_func):
        self.formatter = '%(remote_address)s - %(remote_host)s - %(remote_browser)s - %(remote_is_mobile)s - %(remote_platform)s'
        self.response_func = response_func

    def __call__(self, request):
        request = self.pre_process(request)
        response = self.response_func(request)
        response = self.post_process(response)
        return response

    def pre_process(self, request):
        remote_address = request.META['REMOTE_ADDR']
        remote_host = request.META['REMOTE_HOST']
        remote_browser = request.META['HTTP_SEC_CH_UA']
        remote_is_mobile = request.META['HTTP_SEC_CH_UA_MOBILE']
        remote_platform = request.META['HTTP_SEC_CH_UA_PLATFORM']
        logging.log(
            logging.INFO,
            self.formatter,
            dict(
                remote_address=remote_address, 
                remote_host=remote_host, 
                remote_browser=remote_browser,
                remote_is_mobile = remote_is_mobile,
                remote_platform = remote_platform
            )
        )
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

    def encode_content(self, plaintext):
        """
        Encodes plaintext content as encoded base64 cipher using the given
        AES SECRET and AES SALT value
        """
        padded_plaintext = pad(plaintext, 16)
        cipher = AES.new(settings.AES_SECRET_KEY, AES.MODE_CBC, settings.AES_IV)
        ciphertext = cipher.encrypt(padded_plaintext)
        ciphertext_b64 = base64.b64encode(ciphertext).decode()
        return ciphertext_b64
    
    def decode_content(self, data):
        """
        Decodes encoded base64 cipher using the given
        AES SECRET and AES SALT value into plaintext
        """
        encrypted_data = data
        enc = base64.b64decode(encrypted_data)
        cipher = AES.new(settings.AES_SECRET_KEY, AES.MODE_CBC, settings.AES_IV)
        decrypted_data = unpad(cipher.decrypt(enc),16)
        return decrypted_data

    def pre_process(self, request):
        """
        Pre-processes the request to decode the encoded body content
        into plaintext content
        """
        if len(request.body) < 1:
            return request
        decrypted_data = self.decode_content(request)
        request.body = decrypted_data
        return request

    def post_process(self, response):
        """
        Converts the response into an encoded cipher text
        and outputs it
        """
        plaintext = response.content
        ciphertext_b64 = self.encode_content(plaintext)
        response.content = ciphertext_b64
        return response


    def __init__(self, response_func):
        self.response_func = response_func

    def __call__(self, request):
        request = self.pre_process(request)
        response = self.response_func(request)
        response = self.post_process(response)
        return response
