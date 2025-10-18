from django.db import models


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class UpdatedCreatedAtModel(CreatedAtModel):
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
