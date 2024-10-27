from django.db import models
from django.contrib.auth.models import User

class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField()
    published_at = models.DateTimeField()
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article_id')