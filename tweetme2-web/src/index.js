import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { FeedComponent, TweetDetailComponent, TweetsComponent } from './tweets';
import { ProfileBadgeComponent } from './profiles';


const appEl = document.getElementById('root')

if (appEl){
  const root = ReactDOM.createRoot(appEl);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}

const e = React.createElement
const tweetsEl = document.getElementById('tweetme')
if (tweetsEl) {
  const root = ReactDOM.createRoot(tweetsEl);
  root.render(
    // MyComponent
    <React.StrictMode>
      {e(TweetsComponent, tweetsEl.dataset)}
    </React.StrictMode>
  );
}

const tweetFeedEl = document.getElementById('tweetme-feed')
if (tweetFeedEl) {
  const root = ReactDOM.createRoot(tweetFeedEl);
  root.render(
    // MyComponent
    <React.StrictMode>
      {e(FeedComponent, tweetFeedEl.dataset)}
    </React.StrictMode>
  );
}

const tweetDetailElements = document.querySelectorAll(".tweetme-detail")

tweetDetailElements.forEach(container => {
  const root = ReactDOM.createRoot(container);
  root.render(
    <React.StrictMode>
      {e(TweetDetailComponent, container.dataset)}
    </React.StrictMode>
  );
})

const userProfileBadgeElements = document.querySelectorAll(".tweetme-profile-badge")

userProfileBadgeElements.forEach(container => {
  const root = ReactDOM.createRoot(container);
  root.render(
    <React.StrictMode>
      {e(ProfileBadgeComponent, container.dataset)}
    </React.StrictMode>
  );
})


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
