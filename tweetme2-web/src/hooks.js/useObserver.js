import React, { useEffect } from 'react';

const useObserver = (ref) => {

    useEffect(()=>{
        const observer = new IntersectionObserver(
            ([entry]) => {
              if (entry.isIntersecting) {
                entry.target.click()
              }     
            },
            { 
              root: null,
              rootMargin: "500px", 
              threshold: 0.1 
            }
          );
        
        if (ref.current) {
            observer.observe(ref.current);
          }
    }, [ref.current])
    return (
        null
    );
};

export default useObserver;