import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const FaceVerification = () => {
  const navigate = useNavigate();
  const videoRef = useRef(null); // Reference to the video element
  const [capturing, setCapturing] = useState(false);
  const [images, setImages] = useState([]);
  const [captureCount, setCaptureCount] = useState(0);
  const captureInterval = useRef(null);
  const location = useLocation();
  const { studentData } = location.state;
  // console.log(studentData)
  const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;


  useEffect(() => {
    // Access the webcam
    const setupWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Error accessing webcam:", error);
        alert("Unable to access the webcam. Please check your permissions.");
      }
    };

    setupWebcam();

    // Cleanup webcam on component unmount
    return () => {
      if (videoRef.current?.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks(); // Get all tracks from the media stream
        tracks.forEach((track) => track.stop()); // Stop each track
        videoRef.current.srcObject = null; // Clear the video source
      }
      clearInterval(captureInterval.current); // Clear any capture interval
    };
  }, []);

  const startCapture = () => {
    setCapturing(true);
    setCaptureCount(0);
    setImages([]);

    const canvas = document.createElement("canvas");
    let localCaptureCount = 0; // Local variable to track the count

    captureInterval.current = setInterval(() => {
      if (localCaptureCount >= 10) {
        clearInterval(captureInterval.current);
        setCapturing(false);
        return;
      }

      if (videoRef.current) {
        const video = videoRef.current;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL("image/jpeg").split(",")[1]; // Base64 image data
        setImages((prevImages) => [...prevImages, imageData]);
        localCaptureCount += 1; // Increment the local count
        setCaptureCount(localCaptureCount); // Update the state for UI
      }
    }, 1000); // Capture every second
  };

  const recaptureImages = () => {
    setImages([]);
    setCaptureCount(0);
    startCapture();
  };

  const stopCapture = () => {
    setCapturing(false);
    clearInterval(captureInterval.current);
  };

  const submitImages = async () => {
    if (images.length < 10) {
      alert("Please capture at least 10 images before submitting.");
      return;
    }

    try {
      const response = await fetch(`${BASE_API_URL}/api/students/create-dataset/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Authorization: `Bearer ${JSON.parse(localStorage.getItem("authTokens")).access}`,
        },
        body: new URLSearchParams({ 
          images: images.join(","),
          student_id: studentData.usn,
          student_name: studentData.name, }),
      });

      const result = await response.json();
      if (result.status === "success") {
        alert("Face verification data saved successfully.");
        navigate("/dashboard", { state: { studentData } });
      } else {
        alert("Error: " + result.message);
      }
    } catch (error) {
      console.error("Error submitting images:", error);
      alert("An error occurred while submitting images.");
    }
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold mb-4">Face Verification</h1>
      <video
        ref={videoRef}
        autoPlay
        muted
        className="w-1/3 rounded shadow" // Reduced the width
        style={{ border: "2px solid black" }}
      ></video>
      <div className="mt-4 flex flex-col items-center">
        <p className="text-gray-700 mb-2">
          {capturing ? `Capturing images... (${captureCount}/10)` : images.length === 10 ? "10/10 images captured." : "Ready to capture."}
        </p>
        {capturing ? (
          <button
            onClick={stopCapture}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Stop Capture
          </button>
        ) : images.length === 10 ? (
          <button
            onClick={recaptureImages}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Recapture Images
          </button>
        ) : (
          <button
            onClick={startCapture}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Start Capture
          </button>
        )}
        <button
          onClick={submitImages}
          className="mt-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          disabled={images.length < 10}
        >
          Submit Images
        </button>
      </div>
    </div>
  );
};

export default FaceVerification;
