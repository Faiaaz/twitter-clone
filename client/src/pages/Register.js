import React, { useState } from "react";
import "../styles.css"; // Ensure styles are applied

function Register({ onRegister }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const handleRegister = (e) => {
        e.preventDefault();

        fetch("http://127.0.0.1:5000/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.message) {
                setMessage("Registration successful! You can now log in.");
                setUsername("");
                setPassword("");
                onRegister(); // Call parent function to switch to login page
            } else {
                setMessage(data.error || "Error registering user.");
            }
        })
        .catch(() => setMessage("Error registering user."));
    };

    return (
        <div className="register-box">
            <h2>Register</h2>
            {message && <p style={{ color: "green" }}>{message}</p>}
            <form onSubmit={handleRegister}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default Register;
