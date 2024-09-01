import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from django.conf import settings
from django.db import models

def encode_content(plaintext):
    """
    Encodes plaintext content as encoded base64 cipher using the given
    AES SECRET and AES SALT value
    """
    padded_plaintext = pad(plaintext, 16)
    cipher = AES.new(settings.AES_SECRET_KEY, AES.MODE_CBC, settings.AES_IV)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_b64 = base64.b64encode(ciphertext).decode()
    return ciphertext_b64
    
def decode_content(data):
    """
    Decodes encoded base64 cipher using the given
    AES SECRET and AES SALT value into plaintext
    """
    encrypted_data = data
    enc = base64.b64decode(encrypted_data)
    cipher = AES.new(settings.AES_SECRET_KEY, AES.MODE_CBC, settings.AES_IV)
    decrypted_data = unpad(cipher.decrypt(enc),16)
    return decrypted_data


class EncodedModel(models.Model):
    """
    Base model for entity models where some confidential field data should be
    encoded to disallow db admins to manipulate the data from the direct db instance.
    """

    encoded_fields = []

    def pre_save(self):
        for field in self.encoded_fields:
            if isinstance(self._meta.concrete_fields[field], (models.CharField, models.SlugField, models.TextField)) or issubclass(self._meta.concrete_fields[field], (models.CharField, models.SlugField, models.TextField)):
                field_attr = getattr(self, field)
                setattr(self, field, encode_content(field_attr.encode()).decode('utf-8'))
        pass

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.pre_save()
        super().save(force_insert, force_update, using, update_fields)
        self.post_save()


    def post_save(self):
        for field in self.encoded_fields:
            if isinstance(self._meta.concrete_fields[field], (models.CharField, models.SlugField, models.TextField)) or issubclass(self._meta.concrete_fields[field], (models.CharField, models.SlugField, models.TextField)):
                field_attr = getattr(self, field)
                setattr(self, field, decode_content(field_attr.encode()).decode('utf-8'))
        pass
