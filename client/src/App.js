import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import "./styles/styles.css";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Home from "./pages/Home";

function App() {
    const [user, setUser] = useState(localStorage.getItem("user") || null);

    const handleLogout = () => {
        setUser(null);
        localStorage.removeItem("user");
    };

    return (
        <Router>
            <div className="app-container">
                {/* ✅ Fixed Navigation Bar */}
                <nav className="navbar">
                    <h1>Flask Twitter Clone</h1>
                    <div className="nav-links">
                        {user ? (
                            <>
                                <p>Welcome, <Link to={`/profile/${user}`}>{user}</Link>!</p>
                                <button className="logout-btn" onClick={handleLogout}>Logout</button>
                                <Link to="/">
                                    <button>Homepage</button>
                                </Link>
                            </>
                        ) : (
                            <>
                                <Link to="/login">
                                    <button>Login</button>
                                </Link>
                                <Link to="/register">
                                    <button>Register</button>
                                </Link>
                            </>
                        )}
                    </div>
                </nav>

                {/* ✅ Fixed Content Wrapper */}
                <div className="container">
                    <Routes>
                        {!user ? (
                            <>
                                <Route path="/login" element={<Login onLogin={setUser} />} />
                                <Route path="/register" element={<Register onRegister={() => setUser(null)} />} />
                                <Route path="*" element={<Navigate to="/login" />} />
                            </>
                        ) : (
                            <>
                                <Route path="/" element={<Home />} />
                                <Route path="/profile/:username" element={<Profile />} />
                                <Route path="*" element={<Navigate to="/" />} />
                            </>
                        )}
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;
