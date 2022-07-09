from django.urls import path

from .views import (
    comment_detail_view,
    comment_update_view,
    tweet_action_view, 
    tweet_create_view, 
    tweet_delete_view, 
    tweet_detail_view, 
    tweet_list_view,
    tweet_feed_view,
    comment_create_view,
    comment_delete_view,
    comment_action_view
)

urlpatterns = [
    path('', tweet_list_view),
    path('feed/', tweet_feed_view),
    path('action/', tweet_action_view),
    path('create/', tweet_create_view),
    path('<int:tweet_id>/', tweet_detail_view),
    path('<int:tweet_id>/delete/', tweet_delete_view),
    path('create_comment/', comment_create_view),
    path('<int:comment_id>/delete_comment/', comment_delete_view),
    path('<int:comment_id>/update_comment/', comment_update_view),
    path('comment/action/', comment_action_view),
    path('comment/<int:comment_id>', comment_detail_view)
]
