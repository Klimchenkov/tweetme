import { backendLookup } from "../lookup"


export function apiTweetCreate(newTweet, callback){
    backendLookup("POST", "/tweets/create/", callback, newTweet)
    // backendLookup("POST", "/tweets/create/", callback, {content: newTweet})
  }

export function apiTweetAction(tweetId, action, callback){
    const data = {id: tweetId, action: action}
    backendLookup("POST", "/tweets/action/", callback, data)
  }

export function apiTweetDetail(tweetId, callback) {
    backendLookup('GET', `/tweets/${tweetId}/`, callback)
  }
  
export function apiTweetDelete(tweetId, callback) {
    backendLookup('DELETE', `/tweets/${tweetId}/delete/`, callback)
  }  

export function apiTweetFeed(callback, nextUrl) {
    let endpoint = '/tweets/feed/'
    if (nextUrl !== null && nextUrl !== undefined) {
      endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }
    backendLookup('GET', endpoint, callback)
  }

export function apiTweetList(username, callback, nextUrl) {
      let endpoint = '/tweets/'
      if (username) {
        endpoint = `/tweets/?username=${username}`
      }
      if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
      }
      backendLookup('GET', endpoint, callback)
    }

export function apiCreateComment(tweetId, comment, callback){
      const data = {tweet_id: tweetId, comment: comment}
      backendLookup("POST", "/tweets/create_comment/", callback, data)
  }

export function apiCommentAction(commentId, action, comment, callback){
    const data = {comment_id: commentId, action:action, comment: comment}
    backendLookup("POST", "/tweets/comment/action/", callback, data)
}

export function apiUpdateComment(commentId, comment, callback){
    const data = {comment_id: commentId, comment: comment}
    backendLookup("PUT", `/tweets/${commentId}/update_comment/`, callback, data)
}

export function apiDeleteComment(commentId, callback){
    backendLookup("DELETE", `/tweets/${commentId}/delete_comment/`, callback)
}