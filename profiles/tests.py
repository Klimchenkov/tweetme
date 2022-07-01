from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Profile

User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
         self.user = User.objects.create_user(username='abc', password='somepassword')
         self.userb = User.objects.create_user(username='cba', password='somepassword')
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client
           
    def test_profile_created_via_signal(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)
        
    def test_following(self):
        first = self.user
        second = self.userb
        first.profile.followers.add(second)
        qs = second.following.filter(user=first)
        first_user_following_no_one = first.following.all()
        self.assertTrue(qs.exists())
        self.assertFalse(first_user_following_no_one.exists())
    
    def test_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.userb.username}/follow",
            {"action": "follow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count,1)
    
    def test_unfollow_api_endpoint(self):
        first = self.user
        second = self.userb
        first.profile.followers.add(second)
        
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.userb.username}/follow",
            {"action": "unfollow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count,0)
        
    def test_cannot_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.user.username}/follow",
            {"action": "follow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count,0)