from django.db import models


class EncodedModel(models.Model):
    """
    Base model for entity models where some confidential field data should be
    encoded to disallow db admins to manipulate the data from the direct db instance.
    """
    def pre_save(self):
        # Scramble up the model data fields
        pass

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.pre_save()
        super().save(force_insert, force_update, using, update_fields)
        self.post_save()


    def post_save(self):
        # Unscramble the model data fields
        pass
