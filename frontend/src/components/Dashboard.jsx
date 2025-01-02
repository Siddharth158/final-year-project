import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import axios from "axios";
import { toast } from "react-toastify";

const Dashboard = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [studentData, setStudentData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [enrolledSubjects, setEnrolledSubjects] = useState([]);
  const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

  useEffect(() => {
    const fetchStudentData = async () => {
      try {
        const response = await axios.get(`${BASE_API_URL}/api/students/get-student-data`, {
          headers: {
            Authorization: `Bearer ${JSON.parse(localStorage.getItem("authTokens")).access}`,
          },
        });

        setStudentData(response.data);
        console.log(response.data);

        // Extract subject IDs and fetch their details
        const subjectIds = response.data.subjects || [];
        if (subjectIds.length > 0) {
          const subjectResponse = await axios.post(
            `${BASE_API_URL}/api/students/get-subjects-by-ids/`,
            { subject_ids: subjectIds },
            {
              headers: {
                Authorization: `Bearer ${JSON.parse(localStorage.getItem("authTokens")).access}`,
              },
            }
          );
          console.log(subjectResponse.data);
          setEnrolledSubjects(subjectResponse.data);
        }
      } catch (error) {
        console.error("Error fetching student data:", error);
        setStudentData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchStudentData();
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await axios.get(
        `${BASE_API_URL}/api/students/subjects/search?code=${searchQuery.trim()}`,
        {
          headers: {
            Authorization: `Bearer ${JSON.parse(localStorage.getItem("authTokens")).access}`,
          },
        }
      );

      setSearchResults(response.data);
    } catch (error) {
      console.error("Error searching subjects:", error);
      setSearchResults([]);
    }
  };

  const handleEnroll = async (subjectId) => {
    try {
      const response = await axios.post(
        `${BASE_API_URL}/api/students/enroll/`,
        { subject_id: subjectId, student_id: studentData.usn },
        {
          headers: {
            Authorization: `Bearer ${JSON.parse(localStorage.getItem("authTokens")).access}`,
          },
        }
      );
      // console.log(response.data);

      setEnrolledSubjects([...enrolledSubjects, response.data]);
      toast.success("Enrolled successfully!");
      // console.log(response);
    } catch (error) {
      console.error("Error enrolling in subject:", error);
      toast.error("Failed to enroll in subject.");
    }
  };

  const handleMarkAttendance = async (current_location, subject_code) => {
    try {
      // Step 1: Get the student's current location
      console.log(current_location)
      const getCurrentLocation = () => {
        return new Promise((resolve, reject) => {
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
              (position) => {
                resolve({
                  latitude: parseFloat(position.coords.latitude.toFixed(4)), // Round to 4 decimal places
                  longitude: parseFloat(position.coords.longitude.toFixed(4)), // Round to 4 decimal places
                });
              },
              (error) => {
                reject(error);
              }
            );
          } else {
            reject(new Error("Geolocation is not supported by this browser."));
          }
        });
      };

      const studentLocation = await getCurrentLocation();

      // Step 2: Fetch the teacher's current location
      // const teacherLocation = teacherData.current_location; // Format: "Lat: 12.9716, Long: 77.5946"

      const [teacherLat, teacherLong] = current_location
        .replace("Lat: ", "")
        .replace("Long: ", "")
        .split(", ")
        .map((coord) => parseFloat(parseFloat(coord).toFixed(4))); // Round teacher location to 4 decimals
      console.log(teacherLat, teacherLong);

      // Step 3: Compare locations
      const isLocationMatch =
        Math.abs(studentLocation.latitude - teacherLat) < 0.005 &&
        Math.abs(studentLocation.longitude - teacherLong) < 0.005;

      if (!isLocationMatch) {
        toast.error("Student's location does not match the teacher's location.");
        return;
      }

      navigate("/attendance-capture", {
        state: {
          student_id: studentData.usn,
          subject_code: subject_code,
          student_name: studentData.name,
          // timestamp: currentDateTime,
        },
      });
    } catch (error) {
      console.error("Error during location check:", error);
      toast.error("An error occurred while checking location.");
    }
  };

  const handleCheckAttendance = (subjectId) => {
    toast.info(`Checking attendance for subject ID: ${subjectId}`);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="h-screen bg-gray-100">
      <div className="flex justify-between items-center px-6 py-4 bg-white shadow">
        <h1 className="text-xl font-bold">Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition duration-200"
        >
          Logout
        </button>
      </div>

      <div className="p-6">
        <h2 className="text-2xl font-semibold mb-4">Welcome, {studentData ? studentData.name : "Student"}!</h2>

        {/* Verification Box */}
        {studentData && !studentData.is_verified && (
          <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-6">
            <p className="font-bold">Verification Required</p>
            <p>Your account is not verified. Please verify your face to gain full access.</p>
            <button
              onClick={() => navigate("/verify-face", { state: { studentData } })}
              className="mt-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
            >
              Verify Face
            </button>
          </div>
        )}

        {/* Search Section */}
        <div className="mt-6">
          <input
            type="text"
            placeholder="Enter subject code..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="border border-gray-300 rounded py-2 px-4 w-full md:w-1/2"
          />
          <button
            onClick={handleSearch}
            className="mt-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
          >
            Search
          </button>
        </div>

        {/* Search Results Section */}
        {searchResults.length > 0 && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold mb-4">Search Results</h3>
            <div className="space-y-4">
              {searchResults.map((subject) => (
                <div
                  key={subject.id}
                  className="bg-white p-4 rounded shadow-md border border-gray-200 flex justify-between items-center"
                >
                  <div>
                    <h4 className="text-lg font-bold">{subject.subject_name}</h4>
                    <p className="text-gray-600">Code: {subject.subject_code}</p>
                    <p className="text-gray-600">Semester: {subject.semester}</p>
                  </div>
                  {!enrolledSubjects.some((s) => s.id === subject.id) && (
                    <button
                      onClick={() => handleEnroll(subject.id)}
                      className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
                    >
                      Enroll
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Enrolled Subjects Section */}
        {enrolledSubjects.length > 0 && (
          <div className="mt-8">
            <h3 className="text-xl font-semibold mb-4">Enrolled Subjects</h3>
            <div className="space-y-4">
              {enrolledSubjects.map((subject) => (
                <div
                  key={subject.id}
                  className="bg-white p-4 rounded shadow-md border border-gray-200 flex justify-between items-center"
                >
                  <div>
                    <h4 className="text-lg font-bold">{subject.subject_name}</h4>
                    <p className="text-gray-600">Code: {subject.subject_code}</p>
                    <p className="text-gray-600">Semester: {subject.semester}</p>
                  </div>
                  <div className="space-x-4">
                    <button
                      onClick={() => handleMarkAttendance(subject.current_location, subject.subject_code)}
                      disabled={!subject.is_active}
                      className={`py-2 px-4 rounded transition duration-200 ${subject.is_active ? "bg-blue-500 hover:bg-blue-600 text-white" : "bg-gray-300 text-gray-500 cursor-not-allowed"
                        }`}
                    >
                      Mark Attendance
                    </button>
                    <button
                      onClick={() => handleCheckAttendance(subject.id)}
                      className="bg-yellow-500 text-white py-2 px-4 rounded hover:bg-yellow-600 transition duration-200"
                    >
                      Check Attendance
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
