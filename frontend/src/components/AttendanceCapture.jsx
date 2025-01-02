import React, { useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';


const AttendanceCapture = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [loading, setLoading] = useState(false);
    const [statusMessage, setStatusMessage] = useState('');
    const [isError, setIsError] = useState(false);
    const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

    const location = useLocation();
    const navigate = useNavigate();

    // Extract subjectCode from state
    const subjectCode = location.state?.subject_code;
    const student_id = location.state?.student_id;
    const student_name= location.state?.student_name;
    
    // const timestamp = location.state?.timestamp;

    const showStatus = (message, isError = false) => {
        setStatusMessage(message);
        setIsError(isError);
    };

    const initializeCamera = async () => {
        try {
            const constraints = {
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user',
                },
            };
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
            }
        } catch (err) {
            console.error('Camera access error:', err);
            showStatus('Camera access denied. Please ensure camera permissions are granted.', true);
        }
    };

    useEffect(() => {
        // Ensure subjectCode is present
        if (!subjectCode) {
            showStatus('Subject Code not provided. Redirecting...', true);
            setTimeout(() => navigate('/dashboard'), 2000);
            return;
        }
        initializeCamera();

        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                const tracks = videoRef.current.srcObject.getTracks();
                tracks.forEach((track) => track.stop());
            }
        };
    }, [subjectCode, navigate]);

    const handleCapture = async () => {
        if (!videoRef.current || !canvasRef.current) {
            showStatus('Video stream not ready. Please wait.', true);
            return;
        }

        setLoading(true);
        try {
            const video = videoRef.current;
            const canvas = canvasRef.current;

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            const dataURL = canvas.toDataURL('image/png');
            console.log(dataURL)

            const response = await fetch(`${BASE_API_URL}/api/students/mark_attendance/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${JSON.parse(localStorage.getItem("authTokens")).access}`,
                },
                body: JSON.stringify({

                    student_name: student_name,
                    subject_code: subjectCode,
                    student_id: student_id,
                    image: dataURL,
                }),
            });

            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'success') {
                showStatus('Attendance marked successfully!');
                console.log(data);
                setTimeout(() => navigate('/dashboard'), 1500);
            } else {
                showStatus(data.message || 'Error marking attendance. Please try again.', true);
            }
        } catch (error) {
            console.error('Error:', error);
            showStatus('Error marking attendance. Please try again.', true);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', background: '#f0f0f0', fontFamily: 'Arial, sans-serif' }}>
            <h1>Mark Attendance for Subject Code: {subjectCode || 'N/A'}</h1>
            <video ref={videoRef} width="640" height="480" autoPlay playsInline style={{ marginBottom: '20px' }}></video>
            <button
                onClick={handleCapture}
                style={{
                    margin: '20px',
                    padding: '10px 20px',
                    fontSize: '16px',
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                }}
                disabled={loading}
            >
                {loading ? 'Processing...' : 'Capture'}
            </button>
            {statusMessage && (
                <div
                    style={{
                        margin: '10px',
                        padding: '10px',
                        borderRadius: '5px',
                        backgroundColor: isError ? '#ffebee' : '#e8f5e9',
                        color: isError ? '#c62828' : '#2e7d32',
                    }}
                >
                    {statusMessage}
                </div>
            )}
            <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
        </div>
    );
};

export default AttendanceCapture;

