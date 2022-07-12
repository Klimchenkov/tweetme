from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Comment, Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS
COMMENT_ACTION_OPTIONS = settings.COMMENT_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)
    
    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value
       
class CommentSerializer(serializers.ModelSerializer):
    subcomments = serializers.SerializerMethodField()
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    user_liked = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
                  'id',
                  'parent', 
                  'has_reply',
                  'user',
                  'tweet',
                  'likes',
                  'user_liked',
                  'comment',
                  'subcomments', 
                  'created',
                  'updated'
                  ]
    
    def get_subcomments(self, obj):
        if obj.sub_comments.exists():
            context={'Show_Parents':True}
            context.update(self.context)
            return CommentSerializer(obj.sub_comments.all(), many=True, read_only=True, context=context).data
        else: 
            return []
        
    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_user_liked(self, obj):
        if self.context.get("request"):
            request = self.context.get("request")
            return request.user in obj.likes.all()
        return False
  
    def to_representation(self, data):
        if self.context.get('Show_Parents'):
            return super(CommentSerializer, self).to_representation(data)
        elif data.parent is None:
            return super(CommentSerializer, self).to_representation(data)

class TweetCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Tweet
        fields = ['user', 'id', 'content', 'comments', 'image', 'likes', 'timestamp']
        
    def get_likes(self, obj):
        return obj.likes.count() 
    
    def get_comments(self, obj):
        serializer = CommentSerializer(instance=obj.comments.all(), context=self.context, many=True, read_only=True).data
        return [comment for comment in serializer if comment!=None] 
      
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value    
        
class TweetSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Tweet
        fields = [
            'user', 
            'id', 
            'content',
            'comments', 
            'likes',            
            'image', 
            'is_retweet',
            'parent',
            'timestamp']
        
    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_comments(self, obj):
        serializer = CommentSerializer(instance=obj.comments.all(), context=self.context, many=True, read_only=True).data
        return [comment for comment in serializer if comment!=None]
    
class CommentCreateSerializer(serializers.ModelSerializer):
    tweet_id = serializers.IntegerField()
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['user', 'id', 'comment', 'likes', 'created', 'tweet_id']
    def get_likes(self, obj):
        return obj.likes.count()
    
class CommentActionSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    action = serializers.CharField()
    comment = serializers.CharField(allow_blank=True, required=False)
    
    def validate_action(self, value):
        value = value.lower().strip()
        if not value in COMMENT_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for comments")
        return value