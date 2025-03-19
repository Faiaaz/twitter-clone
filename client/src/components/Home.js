import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function Home() {
    const [tweets, setTweets] = useState([]);
    const [searchUsername, setSearchUsername] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        fetchAllTweets();
    }, []);

    const fetchAllTweets = () => {
        fetch("http://127.0.0.1:5000/api/tweets")
            .then((response) => response.json())
            .then((data) => setTweets(data.tweets))
            .catch((error) => console.error("Error fetching tweets:", error));
    };

    const handleSearchUser = () => {
        if (!searchUsername.trim()) {
            setError("Please enter a username.");
            return;
        }

        fetch(`http://127.0.0.1:5000/api/user/${searchUsername}/tweets`)
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    setError("User not found.");
                    setTweets([]);
                } else {
                    setError("");
                    setTweets(data.tweets);
                }
            })
            .catch(() => setError("Error searching for user."));
    };

    return (
        <div className="container">

            {/* ✅ Search User Input */}
            <div className="tweet-box">
                <input
                    type="text"
                    placeholder="Search user..."
                    value={searchUsername}
                    onChange={(e) => setSearchUsername(e.target.value)}
                />
                <button onClick={handleSearchUser}>Search</button>
                <button onClick={fetchAllTweets}>Clear</button>
            </div>

            {/* ✅ Show error message */}
            {error && <p style={{ color: "red" }}>{error}</p>}
            <h2>All Tweets</h2>

            {/* ✅ Ensure Tweets Do Not Overlap */}
            <div className="tweet-list">
                {tweets.map((tweet) => (
                    <div key={tweet.id} className="tweet-card">
                        <Link to={`/profile/${tweet.user}`}>
                            <strong>{tweet.user}</strong>
                        </Link>
                        <p>{tweet.content}</p>
                        <small>({tweet.timestamp})</small>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Home;
