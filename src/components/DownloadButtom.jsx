import React, { useState, useEffect,Component } from 'react';
import Button from 'react-bootstrap/Button'


function simulateNetworkRequest() {
   return new Promise((resolve) => setTimeout(resolve, 2000));
}
  

function DownloadButton() {
  const [isLoading, setLoading] = useState(false);


  useEffect(() => {
    if (isLoading) {
    
    
      simulateNetworkRequest().then(() => {
        setLoading(false);
      });


    }
  }, [isLoading]);



  const handleClick = () => setLoading(true);



  return (

    <Button
      variant="primary"
      disabled={isLoading}
      onClick={!isLoading ? handleClick : null}
      href='./UserOutputData/data.zip' download='signspotter.zip'
    >
      {isLoading ? 'Loading your file…' : 'Download .CSV/KMZ'}
    </Button> 

  );
}

export default DownloadButton
