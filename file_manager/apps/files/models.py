from apps.common.models import UpdatedCreatedAtModel
from django.db import models


class Image(UpdatedCreatedAtModel):
    title = models.CharField(max_length=255, null=False, blank=False, db_index=True, unique=True)
    image = models.ImageField(upload_to="uploads/")
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)

    def __str__(self):
        return self.title
