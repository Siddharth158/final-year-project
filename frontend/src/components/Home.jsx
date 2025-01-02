import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleTeacherHomeRedirect = () => {
    navigate("/teachers/home");
  };

  return (
    <div className="h-screen bg-gray-100">
      <div className="flex justify-between items-center px-6 py-4 bg-white shadow">
        <h1 className="text-xl font-bold">Welcome to Our Platform!</h1>
        <button
          onClick={handleTeacherHomeRedirect}
          className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
        >
          Go to Teacher Home
        </button>
      </div>
      <div className="flex flex-col items-center justify-center h-[calc(100vh-4rem)]">
        <div className="bg-white p-8 rounded shadow-md w-full max-w-md text-center">
          <h1 className="text-3xl font-bold mb-6 text-gray-800">Welcome to Our Platform!</h1>
          <p className="text-gray-600 mb-6">
            Please login or register to access your account.
          </p>
          <div className="flex flex-col gap-4">
            <Link
              to="/login"
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
            >
              Register
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
