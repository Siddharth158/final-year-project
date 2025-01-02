import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Home from "./components/Home";
import Register from "./components/Register";
import Login from "./components/Login";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Dashboard from "./components/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import TeacherRegister from "./components/TeacherRegister";
import TeacherLogin from "./components/TeacherLogin";
import TeacherDashboard from "./components/TeacherDashboard";
import TeacherHome from "./components/TeacherHome";
import FaceVerification from "./components/FaceVerification";
import AttendanceCapture from "./components/AttendanceCapture";

const App = () => {
  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/attendance-capture" element={<AttendanceCapture />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route path="/teachers/home" element={<TeacherHome />} />
            
            <Route path="/teachers/register" element={<TeacherRegister />} />
            <Route path="/teachers/login" element={<TeacherLogin />} />
            <Route path="/teachers/dashboard" element={<TeacherDashboard />} />
            <Route path="/verify-face" element={<FaceVerification />} />
          </Routes>
        </Router>
      </AuthProvider>
    </>
  );
};

export default App;
