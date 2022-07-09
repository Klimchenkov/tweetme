import React from "react";
import { UserDisplay, UserPicture } from "../profiles";
import moment from 'moment';

import { apiCommentAction, apiDeleteComment, apiUpdateComment } from "../tweets/lookup";


export function Comment (props) {
    const {comment, didPerformAction} = props
    const like = comment.user_liked ? 'Unlike' : 'Like'

    const handleActionBackendEvent = (response, status) => {
        if ((status === 200 || status === 201) && didPerformAction) {
            didPerformAction(response, status)
        }
    }

    const handleClick = (event, currentAction) => {
        if (['Like', 'Unlike'].includes(currentAction)){
            apiCommentAction(comment.id, currentAction.toLowerCase(), 'no comment', handleActionBackendEvent)
        }
        else if (currentAction === 'update_comment') {
            const newComment = prompt("Update your comment here", comment.comment)
            if (newComment === null){
                return
            }
            apiUpdateComment(comment.id, newComment, handleActionBackendEvent)
        } else if (currentAction === 'reply'){

            const replyComment = prompt("Reply here")
            if (replyComment === null){
                return
            }
            apiCommentAction(comment.id, currentAction, replyComment, handleActionBackendEvent)
        } else if (currentAction === 'delete_comment') {
            apiDeleteComment(comment.id, handleActionBackendEvent)
        }
        }

    return <div className='mt-3'>
        <div className="d-flex">
            <div>
                <UserPicture user = {comment.user} className='avatar_comment' />
            </div>
            <div className="col-11">
                <div className='comment'>
                    <p>
                        <UserDisplay includeFullName user={comment.user}/>
                    </p>
                    <p>
                            {comment.comment}
                    </p>
                    { comment.likes !==0 &&
                        <div className='text-right'> 
                                <i className="fa fa-thumbs-up fa-tag"/>
                                <span className='ml-2 h5 text-secondary'>
                                    {comment.likes}
                                </span>
                        </div>
                    }
                </div> 
                <div className='ml-2 d-flex text-muted'>
                    <p>{moment(comment.updated).fromNow()}</p> 
                    <p 
                        onClick={(e) => {
                            handleClick(e, like)
                        }} 
                        className={'commentBtn'}
                    >
                        {like}
                    </p>
                    <p 
                        onClick={(e) => {
                            handleClick(e, 'reply')
                        }} 
                        className={'commentBtn'}
                    >
                        Reply
                    </p>
                    { comment.user.username === props.deleter && 
                        <p 
                            className={'commentBtn'}
                            onClick={(e) => {
                                handleClick(e, 'update_comment')
                            }} 
                        >
                            Update
                        </p> 
                    }
                    { comment.user.username === props.deleter && 
                        <p 
                            className={'commentBtn'}
                            onClick={(e) => {
                                handleClick(e, 'delete_comment')
                            }} 
                        >
                            Delete
                        </p> 
                    }
                </div>
                
                {comment.subcomments.map((subcomment,index) => {
                        return <Comment 
                                    comment={subcomment}
                                    key={`${subcomment.id}`}
                                    deleter = {props.deleter}
                                    didPerformAction = {didPerformAction}   
                                />
                    })}
            </div>
        </div>
        </div>
}