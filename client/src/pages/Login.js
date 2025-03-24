import React, { useState } from "react";
import "../styles/styles.css";

function Login({ onLogin }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

   const handleLogin = (event) => {
    event.preventDefault();

    fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    })
    .then((response) => response.json()) // Convert response to JSON
    .then((data) => {
        if (data.message === "Login successful") {
            localStorage.setItem("user", username); // ✅ Save user after login
            onLogin(username); // ✅ Update React state
        } else {
            setError("Invalid credentials"); // ✅ Now using setError properly
        }
    })
    .catch((error) => alert("Error logging in: " + error.message));
};


    return (
        <div className="login-box">
            <h2>Login</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleLogin}>
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
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;
