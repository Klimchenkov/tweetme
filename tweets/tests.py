from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Comment, Tweet
# Create your tests here.

User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='abc', password='somepassword')
        self.userb = User.objects.create_user(username='cba', password='somepassword')
        Tweet.objects.create(content="my first tweet", user=self.user)
        Tweet.objects.create(content="my second tweet", user=self.user)
        Tweet.objects.create(content="my third tweet", user=self.userb)
        self.currentCount = Tweet.objects.all().count()
        self.currentCommentsCount = Comment.objects.all().count()
        
    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="my second tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
    
    def test_tweets_related_name(self):
        user = self.user
        self.assertEqual(user.tweets.count(), 2)
        
        
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        user = self.user
        my_like_instances_count = user.tweetlike_set.count()
        self.assertEqual(my_like_instances_count, 1)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        response = client.post("/api/tweets/action/", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
        
    def test_action_retweet(self):
        client = self.get_client()
        current_count = self.currentCount
        response = client.post("/api/tweets/action/", 
                               {"id": 2, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)
        
    def test_tweet_create_api_view(self):   
        request_data = {"content": "This is my test tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_tweet_id)
        
    def test_comments_create(self):
        # create comment
        request_data = {"comment": "this is a test comment", "tweet_id":1}
        client = self.get_client()
        response = client.post("/api/tweets/create_comment/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_comment_id = response_data.get("id")
        self.assertEqual(self.currentCommentsCount+1, new_comment_id)
        # reply comment
        request_data = {"comment":"this is the reply", "comment_id":1, "action":"reply"}
        response = client.post("/api/tweets/comment/action/", request_data)
        sub_comment = response.json()
        tweet = client.get("/api/tweets/1/")
        tweet = tweet.json()
        self.assertEqual(sub_comment["comments"][0]["subcomments"][0]["parent"], 1)
        self.assertEqual(tweet["comments"][0]["subcomments"][0]["comment"], sub_comment["comments"][0]["subcomments"][0]["comment"])
        # update comment
        request_data = {"comment": "this is the updated comment"}
        api = "/api/tweets/" + str(sub_comment["comments"][0]["subcomments"][0]["id"]) + "/update_comment/"
        response = client.put(api, request_data)
        tweet = client.get("/api/tweets/1/")
        tweet = tweet.json()
        self.assertEqual(tweet["comments"][0]["subcomments"][0]["comment"], request_data['comment'])
        # like comment
        request_data = {"comment_id":1, "action":"like"}
        response = client.post("/api/tweets/comment/action/", request_data)
        tweet = client.get("/api/tweets/1/")
        tweet = tweet.json()
        self.assertEqual(tweet["comments"][0]["likes"], 1)
        # unlike comment
        request_data = {"comment_id":1, "action":"unlike"}
        response = client.post("/api/tweets/comment/action/", request_data)
        tweet = client.get("/api/tweets/1/")
        tweet = tweet.json()
        self.assertEqual(tweet["comments"][0]["likes"], 0)
        # delete comment
        api = "/api/tweets/" + str(new_comment_id) + "/delete_comment/"
        response = client.delete(api)
        tweet = client.get("/api/tweets/1/")
        tweet = tweet.json()
        self.assertEqual(len(tweet["comments"]), 0)
        
    def test_tweet_detail_api_view(self):   
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)
        
    def test_tweet_delete_api_view(self):   
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)
