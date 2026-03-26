from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = ResizedImageField(
        size=[500, 500], 
        quality=75, 
        upload_to='photos/', 
        force_format='JPEG', 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='tweet_likes', blank=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'
    
    # Helper to count total likes
    def total_likes(self):
        return self.likes.count()
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    profile_image = ResizedImageField(
        size=[300, 300], 
        quality=75, 
        crop=['middle', 'center'], 
        upload_to='profile_pics/', 
        default='profile_pics/default.jpg' # Point to the subfolder
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'