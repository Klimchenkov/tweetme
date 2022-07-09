import React, { useState } from "react";
import { Comment } from "../comments";
import { UserDisplay, UserPicture } from "../profiles";
import { ActionBtn } from "./buttons";
import { TweetsComponent } from "./components";
import { apiTweetDelete } from "./lookup";

export function ParentTweet(props) {
    const {tweet} = props
    
    return tweet.parent ?   <Tweet isRetweet reTweeter={props.reTweeter} hideActions className={' '} tweet={tweet.parent} />  : null                
}  


export function Tweet(props) {
    const {tweet, didRetweet, hideActions, isRetweet, reTweeter} = props
    const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null)
    let className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    className = isRetweet === true ? `${className} p-2 border rounded`: className
    const path = window.location.pathname
    const match = path.match(/(?<tweetid>\d+)/)
    const urlTweetId = match ? match.groups.tweetid : -1
    const isDetail = `${tweet.id}` === `${urlTweetId}`
    const [Display, setDisplay] = useState('')
    const [showComments, setShowComments] = useState(' d-none')
    const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/${tweet.id}`
    }
    const handlePerformAction = (newActionTweet, status, action) => {
        if (status === 200) {
            setActionTweet(newActionTweet)
        } else if (action === 'retweet') {
            if (didRetweet) {
                didRetweet(newActionTweet)
            } 
        } else if (action === 'comment') {
            setActionTweet(newActionTweet)
        } else if (status === 201) {
            setActionTweet(newActionTweet)
        }
    }

    const handleDelete = (response, status) => {
        if (status === 200) {
            setDisplay(' d-none')
        } else {
            alert("There was an error deleting your tweet.")
        }
    }
    const deleteTweet = (event) => {
        apiTweetDelete(tweet.id, handleDelete)
    }
    return <div><div className={className + Display}>
        { props.deleter===tweet.user.username && !isRetweet ? <button onClick={deleteTweet} className='float-right btn btn-danger btn-sm mr-3'>Delete</button> : null}
        {isRetweet === true && <div className='mb-2'>
            <span className='small text-muted'>Retweet via <UserDisplay user={reTweeter}/></span>
        </div>}
        <div className="d-flex">
        <div className=''>
            <UserPicture user = {tweet.user} className='avatar_sm' />
        </div>
        <div className='col-11'>
            <div>
                <p>
                    <UserDisplay includeFullName user={tweet.user}/>
                </p>
                <p>{tweet.content}</p>
                {tweet.image ? <img src={tweet.image} className="tweetimg"/> : null}
                <ParentTweet tweet={tweet} reTweeter={tweet.user}/>
            </div>
        
        
        <div className='btn btn-group px-0'>
        {actionTweet && hideActions !== true && <React.Fragment>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'like', display:"Likes"}}/>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'unlike', display:"Unlike"}}/>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'retweet', display:"Retweet"}}/>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'comment', display:"Comment"}}/>
            </React.Fragment>
        }
            {isDetail === true ? null : <button className='btn btn-outline-primary btn-sm' onClick={handleLink}>View</button>}
        </div>
        </div>
    </div>
    </div>
    {!isRetweet && 
        <div className={'pb-3 col-11 ml-5 mr-5' + Display + showComments}>
            {actionTweet.comments.map((comment,index) => {
                return <Comment 
                        comment={comment}
                        key={`${comment.id}`}
                        deleter = {props.deleter}
                        didPerformAction={handlePerformAction}
                        />
            })}
        </div>
    } 
    {  !isRetweet &&   <div className='row'>
    {
            showComments === ' d-none' 
            ?
            <btn 
                className={'btn btn-outline-primary mx-auto btn-sm mb-5 mt-3'}
                onClick={()=>{setShowComments('')}}
            >
                Show Comments
            </btn> 
            : actionTweet.comments.length !== 0 
                ?
                    <btn 
                        className={'btn btn-outline-primary mx-auto btn-sm mb-5 mt-3'}
                        onClick={()=>{setShowComments(' d-none')}}
                    >
                        Hide Comments
                    </btn> 
                : 
                    <div className='mx-auto pb-5'>
                    <div className='mb-2'>Nobody commented on this one yet, you can be first!</div>
                    <div className='text-center'>
                        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'comment', display:"Comment"}}/>
                    </div>
                    </div>
            
        }
        </div>}
    </div>
    }
