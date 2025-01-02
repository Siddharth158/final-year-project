import React, { useContext } from "react";
import AuthContext from "../context/AuthContext";

const Logout = () => {
  const { logout } = useContext(AuthContext);

  return (
    <button onClick={logout} className="bg-red-500 text-white py-2 px-4 rounded">
      Logout
    </button>
  );
};

export default Logout;
