import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import axios from "axios";

const TeacherDashboard = () => {
  const navigate = useNavigate();
  const [teacherData, setTeacherData] = useState({id: "", name: "", email: ""});
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    subject_code: "",
    subject_name: "",
    semester: "",
  });
  const [subjects, setSubjects] = useState([]);
  const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;


  const fetchSubjects = async (data) => {
    try {
      const subjectListResponce = await axios.get(`${BASE_API_URL}/api/teachers/subjects/${data.id}/`);
      // console.log(subjectListResponce.data)
      setSubjects(subjectListResponce.data.subjects);
    }
    catch (error) {
      console.error("Error fetching subjects:", error);
    }
}

  const fetchTeacherData = async () => {
    try {
      const response = await axios.get(`${BASE_API_URL}/api/teachers/get-teacher-data`, {
        headers: {
          Authorization: `Bearer ${JSON.parse(localStorage.getItem("teacherAuthTokens")).access}`,
        },
      });

      setTeacherData(response.data);
      fetchSubjects(response.data);
      
    } catch (error) {
      console.error("Error fetching teacher data:", error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("teacherAuthTokens");
    toast.success("Logged out successfully!");
    navigate("/teachers/login");
  };

  const toggleIsActive = async (subjectId) => {
    try {
      // Get current location
      const getCurrentLocation = () => {
        return new Promise((resolve, reject) => {
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
              (position) => {
                resolve({
                  latitude: position.coords.latitude,
                  longitude: position.coords.longitude,
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
  
      const location = await getCurrentLocation();
  
      const response = await fetch(`${BASE_API_URL}/api/teachers/subjects/toggle/${subjectId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          current_location: `Lat: ${location.latitude}, Long: ${location.longitude}`,
        }),
      });
  
      if (response.ok) {
        toast.success("Subject status updated successfully!");
        fetchSubjects(teacherData); // Refresh the subject list
      } else {
        toast.error("Failed to update subject status.");
      }
    } catch (error) {
      console.error("Error fetching location or updating subject status:", error);
      toast.error("An error occurred while updating subject status.");
    }
  };
  

  useEffect(() => {
    fetchTeacherData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleCreateSubject = async () => {
    try {
      const response = await fetch(`${BASE_API_URL}/api/teachers/subjects/create/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...formData, teacher_id: teacherData.id }),
      });
      console.log(response)

      if (response.ok) {
        toast.success("Subject created successfully!");
        setShowModal(false);
        setFormData({ subject_code: "", subject_name: "", semester: "" });
        fetchSubjects(teacherData); // Refresh the subject list
        // fetchTeacherData();
      } else {
        const errorData = await response.json();
        toast.error(errorData.error || "Failed to create subject.");
      }
    } catch (error) {
      toast.error("An error occurred while creating the subject.");
    }
  };

  return (
    <div className="h-screen bg-gray-100">
      <div className="flex justify-between items-center px-6 py-4 bg-white shadow">
        <h1 className="text-xl font-bold">Teacher Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition duration-200"
        >
          Logout
        </button>
      </div>
      <div className="p-6">
        <h2 className="text-2xl font-semibold mb-4">Welcome {teacherData.name}</h2>
        <p className="text-gray-600 mb-6">Manage your account or access teacher resources here.</p>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
        >
          Add New Subject
        </button>
        <div className="mt-6">
          <h3 className="text-xl font-semibold mb-4">Subject List</h3>
          {subjects.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {subjects.map((subject) => (
                <div
                  key={subject.id}
                  className="bg-white p-4 rounded shadow-md border border-gray-200"
                >
                  <h4 className="text-lg font-bold mb-2">{subject.subject_name}</h4>
                  <p className="text-gray-600">Code: {subject.subject_code}</p>
                  <p className="text-gray-600">Semester: {subject.semester}</p>
                  <p className="text-gray-600">
                    Status: {subject.is_active ? "Active" : "Inactive"}
                  </p>
                  <div className="mt-4 flex justify-between">
                    <button
                      onClick={() => toggleIsActive(subject.id)}
                      className={`py-2 px-4 rounded transition duration-200 ${
                        subject.is_active
                          ? "bg-red-500 text-white hover:bg-red-600"
                          : "bg-green-500 text-white hover:bg-green-600"
                      }`}
                    >
                      {subject.is_active ? "Deactivate" : "Activate"}
                    </button>
                    <button
                      className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
                    >
                      View Attendance
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No subjects found.</p>
          )}
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-6 rounded shadow-lg w-96">
            <h2 className="text-xl font-semibold mb-4">Add New Subject</h2>
            <div className="mb-4">
              <label className="block text-gray-700">Subject Code</label>
              <input
                type="text"
                name="subject_code"
                value={formData.subject_code}
                onChange={handleInputChange}
                className="w-full border border-gray-300 rounded py-2 px-3"
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700">Subject Name</label>
              <input
                type="text"
                name="subject_name"
                value={formData.subject_name}
                onChange={handleInputChange}
                className="w-full border border-gray-300 rounded py-2 px-3"
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700">Semester</label>
              <input
                type="number"
                name="semester"
                value={formData.semester}
                onChange={handleInputChange}
                className="w-full border border-gray-300 rounded py-2 px-3"
              />
            </div>
            <div className="flex justify-end">
              <button
                onClick={() => setShowModal(false)}
                className="bg-gray-300 text-gray-700 py-2 px-4 rounded mr-2 hover:bg-gray-400 transition duration-200"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateSubject}
                className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherDashboard;
