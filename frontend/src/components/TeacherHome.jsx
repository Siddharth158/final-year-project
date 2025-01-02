import React from "react";
import { Link, useNavigate } from "react-router-dom";

const TeacherHome = () => {
  const navigate = useNavigate();

  const handleMainHomeRedirect = () => {
    navigate("/");
  };

  return (
    <div className="h-screen bg-gray-100">
      <div className="flex justify-between items-center px-6 py-4 bg-white shadow">
        <h1 className="text-xl font-bold">Welcome Teachers!</h1>
        <button
          onClick={handleMainHomeRedirect}
          className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
        >
          Go to Main Home
        </button>
      </div>
      <div className="flex flex-col items-center justify-center h-[calc(100vh-4rem)]">
        <div className="bg-white p-8 rounded shadow-md w-full max-w-md text-center">
          <h1 className="text-3xl font-bold mb-6 text-gray-800">Welcome Teachers!</h1>
          <p className="text-gray-600 mb-6">
            Please login or register to access the teacher portal.
          </p>
          <div className="flex flex-col gap-4">
            <Link
              to="/teachers/login"
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
            >
              Teacher Login
            </Link>
            <Link
              to="/teachers/register"
              className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
            >
              Teacher Register
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeacherHome;
