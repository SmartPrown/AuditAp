from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Check(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    reason = models.TextField()
    init_date = models.DateTimeField(default=timezone.now)
    test_field = models.CharField(max_length=50, default="ttt")
    # file = models.FileField(upload_to="checks/")

    def init(self):
        self.init_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
