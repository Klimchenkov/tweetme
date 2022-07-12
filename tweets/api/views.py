import random
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from ..models import Comment, Tweet 
from ..forms import TweetForm
from ..serializers import (
    CommentActionSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    TweetSerializer, 
    TweetActionSerializer, 
    TweetCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(instance=obj, context={"request": request})
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet."}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed."}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(instance=obj, context={"request": request})
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(instance=obj, context={"request": request})
            return Response(serializer.data, status=200)
        elif action == "retweet":  
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content)
            serializer = TweetSerializer(instance=new_tweet, context={"request": request})
            return Response(serializer.data, status=201)
    return Response({}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = TweetSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.feed(user)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create_view(request, *args, **kwargs):
    try:
        serializer = CommentCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            tweet_id = data.get('tweet_id')
            qs = Tweet.objects.filter(id=tweet_id)
            tweet_obj = qs.first()
            serializer.save(user = request.user, tweet = tweet_obj)
            serializer=TweetSerializer(instance=tweet_obj, context={"request": request})
            return Response(serializer.data, status=201)
        return Response({}, status=400)
    except Exception as e:
        raise e

# TODO

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def comment_delete_view(request, comment_id, *args, **kwargs):
    try:
        qs = Comment.objects.filter(id=comment_id)
        if not qs.exists():
            return Response({}, status=404)
        qs = qs.filter(user=request.user)
        if not qs.exists():
            return Response({"message": "You cannot delete this tweet."}, status=403)
        obj = qs.first()
        serializer = TweetSerializer(instance=obj.tweet, context={"request": request})
        obj.delete()
        return Response(serializer.data, status=200)
    except Exception as e:
        raise e

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_update_view(request, comment_id, *args, **kwargs):
    try:
        print(comment_id)
        obj = get_object_or_404(Comment, id=comment_id, user=request.user)
        obj.comment = request.data["comment"]
        obj.save()
        serializer = TweetSerializer(instance=obj.tweet, context={"request": request})
        return Response(serializer.data, status=200)
    except Exception as e:
        raise e
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_action_view(request, *args, **kwargs):
    try:
        serializer = CommentActionSerializer(data = request.data)
        context={
            'Show_Parents':True,
            "request": request
            }
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            comment_id = data.get("comment_id")
            action = data.get("action")
            comment = data.get("comment")
            qs = Comment.objects.filter(id=comment_id)
            if not qs.exists():
                return Response({}, status=404)
            obj = qs.first()
            if action == "like":
                obj.likes.add(request.user)
                serializer = TweetSerializer(instance=obj.tweet, context={"request": request})
                return Response(serializer.data, status=200)
            elif action == "unlike":
                obj.likes.remove(request.user)
                serializer = TweetSerializer(instance=obj.tweet, context={"request": request})
                return Response(serializer.data, status=200)
            elif action == "reply":
                new_comment = Comment.objects.create(
                    user=request.user,
                    parent = obj,
                    comment = comment,
                    tweet=obj.tweet
                )
                serializer = TweetSerializer(instance=obj.tweet, context={"request": request})
                return Response(serializer.data, status=201)
        return Response({}, status=200)
    except Exception as e:
        raise e
    
@api_view(['GET'])
def comment_detail_view(request, comment_id, *args, **kwargs):
    qs = Comment.objects.filter(id=comment_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    context={
        'Show_Parents':True,
        "request": request}
    serializer = CommentSerializer(instance=obj, context=context)
    return Response(serializer.data, status=200)
