import React from "react";
import { apiTweetCreate } from "./lookup";

export function TweetCreate(props) {
    const textAreaRef = React.createRef()
    const imageRef = React.createRef()
    const {didTweet} = props
    const handleBackendUpdate = (response, status) => {
        if(status===201) {
            didTweet(response)
        } else {
            alert("An error occured please try again.")
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        const newImage = imageRef.current.files[0]
        const formData = new FormData()
        if (newImage){
            formData.append('image', newImage)
        }
        formData.append('content', newVal)
        const newTweet = formData
        apiTweetCreate(newTweet, handleBackendUpdate)
        textAreaRef.current.value = ''
    }
    return  <div className={props.className}>
                <form onSubmit={handleSubmit} encType="multipart/form-data">
                    <textarea ref={textAreaRef} required={true} className="form-control" name='tweet'>

                    </textarea>
                    <div className="mt-3">
                    <label htmlFor="image">Add an image to your tweet</label>
                    <input ref={imageRef} type='file' className="form-control-file" id="image" name='image' accept=".jpg, .jpeg, .png"/>
                    </div>
                     <button type='submit' className="btn btn-primary my-3">Tweet</button>
                </form>
            </div>
}
