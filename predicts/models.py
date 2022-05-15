from django.db import models
from django.conf import settings

# Create your models here.

class Predict(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 역참조 매니저 이름이 겹침! user 필드랑! => related_name!!
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_images')
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster_url = models.ImageField(blank=True, upload_to='images/')
    predict_name = models.CharField(blank=True,null=True,max_length=15)
    def __str__(self):
        return self.title


class Comment(models.Model):
    predict = models.ForeignKey(Predict, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
