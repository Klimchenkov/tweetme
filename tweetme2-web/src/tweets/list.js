import React, { useEffect, useRef, useState } from "react";
import useObserver from "../hooks.js/useObserver";
import { Tweet } from "./detail";
import { apiTweetList } from "./lookup";


export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [nextUrl, setNextUrl] = useState(null)
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    const ref = useRef(null);
    const Obs = useObserver(ref)
    useEffect(()=>{
        const final = [...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length) {
          setTweets(final)
        }
      }, [props.newTweets, tweets, tweetsInit])

    useEffect(() => {
      if (tweetsDidSet === false) {  
        const handleTweetListLookup = (response, status) => {
            if (status === 200) {
                setNextUrl(response.next)
                setTweetsInit(response.results)
                setTweetsDidSet(true)
            } else {
            alert("There was an error")
            }
        }
        apiTweetList(props.username, handleTweetListLookup)
    }
    }, [tweetsInit, tweetsDidSet, setTweetsDidSet, props.username])
    
    const handleDidRetweet = (newTweet) => {
        const updateTweetsInit = [...tweetsInit]
        updateTweetsInit.unshift(newTweet)
        setTweetsInit(updateTweetsInit)
        const updateFinalTweets = [...tweets]
        updateFinalTweets.unshift(newTweet)
        setTweets(updateFinalTweets)
      }

    const handleLoadNext = (event) => {
        event.preventDefault()
        if (nextUrl !== null) {
            const handleLoadNextResponse = (response, status) => {
                if (status === 200) {
                    const newTweets = [...tweets].concat(response.results)
                    setNextUrl(response.next)
                    setTweetsInit(newTweets)
                    setTweets(newTweets) 
                } else {
                    alert("There was an error")
                }
            }
            apiTweetList(props.username, handleLoadNextResponse, nextUrl)
        }
    }

    return <React.Fragment>{tweets.map((item, index) => { 
              return <Tweet 
                tweet={item}
                didRetweet={handleDidRetweet} 
                key={`${item.id}`} 
                className='my-3 py-4 border bg-white text-dark'
                {...props} />
            })}
            
            {nextUrl !== null && <div ref={ref} onClick={handleLoadNext}/>}
            </React.Fragment>      
  }
 