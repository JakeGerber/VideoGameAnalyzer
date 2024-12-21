/*import React, { useEffect, useRef } from "react";
import Webcam from "react-webcam";
//import jsQR from "jsqr";

const videoConstraints = {
  width: 540,
  facingMode: "environment"
};

const Camera = () => {
  const webcamRef = useRef(null);
  const [url, setUrl] = React.useState(null);

  const capturePhoto = React.useCallback(async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setUrl(imageSrc);
  }, [webcamRef]);

  const onUserMedia = (e) => {
    console.log(e);
  };

  return (
    <>
      <Webcam
        ref={webcamRef}
        audio={true}
        screenshotFormat="image/jpeg"
        videoConstraints={videoConstraints}
        onUserMedia={onUserMedia}
      />
      <button onClick={capturePhoto}>Capture</button>
      <button onClick={() => setUrl(null)}>Refresh</button>
      {url && (
        <div>
          <img src={url} alt="Screenshot" />
        </div>
      )}
    </>
  );
};

export default Camera;
*/

import React, { useEffect, useRef } from "react";
import Webcam from "react-webcam";

const videoConstraints = {
  width: 540,
  facingMode: "environment"
};

const Camera = ({ onCapture }) => {
  const webcamRef = useRef(null);
  const [url, setUrl] = React.useState(null);

  const capturePhoto = React.useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setUrl(imageSrc);
    if (onCapture) {
      onCapture(imageSrc);
    }
  }, [webcamRef, onCapture]);

  return (
    <>
      <Webcam
        ref={webcamRef}
        audio={false}
        screenshotFormat="image/jpeg"
        videoConstraints={videoConstraints}
      />
      <button onClick={capturePhoto}>Capture</button>
      <button onClick={() => setUrl(null)}>Refresh</button>
      {url && (
        <div>
          <img src={url} alt="Screenshot" />
        </div>
      )}
    </>
  );
};

export default Camera;
