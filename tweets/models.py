import random
from sqlite3 import Timestamp
from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from platformdirs import user_cache_dir
from tweetme2.yandex_s3_storage import ClientDocsStorage


User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)
        
        
    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user_id", flat=True)
        return self.filter(Q(user__id__in = followed_users_id) |
                                Q(user=user)
                                ).distinct().order_by("-timestamp")
        
class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)
    
    def feed(self, user):
        return self.get_queryset().feed(user)

class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="tweets")
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(storage=ClientDocsStorage(), upload_to='tweetme/tweet_img', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = TweetManager()
    
    def __str__(self):
        if self.content is None:
            return "No content in this one"
        return self.content
    
    class Meta:
        ordering = ['-id']
    
    @property
    def is_retweet(self):
        return self.parent != None

class CommentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(CommentManager, self).get_queryset()\
            .annotate(likes_count=Count('likes')).order_by('-likes_count')
            
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", related_name="sub_comments", blank=True, null=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="comment_user", blank = True, through=CommentLike)
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    
    objects = CommentManager()
    
    def __str__(self):
        if self.comment is None:
            return "This comment is blank"
        return self.comment
        
    class Meta:
        ordering = ['-updated']
        
    @property
    def has_reply(self):
        return self.sub_comments.exists()

    
 
    