import React, { Component } from 'react';
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
        <a href='/public/UserOutputData/data.csv'></a>
      });


    }
  }, [isLoading]);



  const handleClick = () => setLoading(true);



  return (

    <Button
      variant="primary"
      disabled={isLoading}
      onClick={!isLoading ? handleClick : null}
    >
      {isLoading ? 'Loading your file…' : 'Download .CSV/KMZ'}
    </Button> 

  );
}

export default DownloadButton
