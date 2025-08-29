from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class ShortedURL(models.Model):
    """
        Database table representing relation between original url and shortened
    """
    id = models.AutoField(primary_key=True)
    original_url = models.URLField()
    shorted_url = models.CharField(max_length=32, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='urls')
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.original_url} -> {self.shorted_url}'