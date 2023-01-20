from django.db import models


class CarManager(models.Manager):
    def activebookable(self):
        return self.get_queryset().filter(
            status="active",
        )
