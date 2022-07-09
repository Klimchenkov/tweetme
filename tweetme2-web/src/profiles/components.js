import React from "react";


export function UserLink (props) {
    const {username} = props
    const handleUserLink = (event) => {
        window.location.href = `/profile/${username}`
    }
    return <span className='pointer' onClick={handleUserLink}>
        {props.children}
    </span>
}

export function UserDisplay (props) {
    const {user, includeFullName, hideLink} = props
    const nameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name} ` : null
    
    return <React.Fragment>
        <strong>
            {nameDisplay}
            {hideLink === true ? `@${user.username}` : <UserLink username={user.username}>@{user.username}</UserLink>}
        </strong>
    </React.Fragment>
}

export function UserPicture (props) {
    const {user, hideLink, className } = props
    const userIdSpan =  user.image ?
                        <img src={user.image} className={className}/>:
                        <span className={className}>
                            {user.username[0]}
                        </span>
                        
    return  hideLink === true ? userIdSpan : <UserLink username={user.username}>{userIdSpan}</UserLink>
}
