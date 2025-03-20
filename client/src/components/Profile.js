import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../styles.css"; // Ensure styles are applied

function Profile() {
    const { username } = useParams();
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState("");
    const [editingTweet, setEditingTweet] = useState(null);
    const [newContent, setNewContent] = useState("");
    const [tweetContent, setTweetContent] = useState(""); // New state for posting tweets

    const loggedInUser = localStorage.getItem("user");

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/api/user/${username}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    setError(data.error);
                } else {
                    setUserData(data);
                }
            })
            .catch(() => setError("Error fetching user profile"));
    }, [username]);

    const handlePostTweet = (e) => {
        e.preventDefault();

        if (!tweetContent.trim()) return;

        fetch("http://127.0.0.1:5000/api/tweets", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: loggedInUser, content: tweetContent }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.message) {
                setTweetContent("");
                setUserData({
                    ...userData,
                    tweets: [{ id: data.tweet.id, user: loggedInUser, content: tweetContent, timestamp: data.tweet.timestamp }, ...userData.tweets]
                });
            }
        })
        .catch(() => setError("Error posting tweet"));
    };

    const handleEditTweet = (tweet) => {
        setEditingTweet(tweet.id);
        setNewContent(tweet.content);
    };

    const handleSaveEdit = (tweetId) => {
        fetch(`http://127.0.0.1:5000/api/tweet/${tweetId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: loggedInUser, content: newContent }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.message) {
                setUserData({
                    ...userData,
                    tweets: userData.tweets.map((tweet) =>
                        tweet.id === tweetId ? { ...tweet, content: newContent } : tweet
                    ),
                });
                setEditingTweet(null);
            }
        })
        .catch(() => setError("Error updating tweet"));
    };

    const handleDeleteTweet = (tweetId) => {
        fetch(`http://127.0.0.1:5000/api/tweet/${tweetId}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: loggedInUser }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.message) {
                setUserData({
                    ...userData,
                    tweets: userData.tweets.filter((tweet) => tweet.id !== tweetId),
                });
            }
        })
        .catch(() => setError("Error deleting tweet"));
    };

    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    if (!userData) {
        return <p>Loading profile...</p>;
    }

    return (
        <div className="profile-container">
            <h2>{userData.username}'s Profile</h2>

            {/* ✅ Show post tweet box only for the logged-in user */}
            {loggedInUser === username && (
                <div className="tweet-box">
                    <h3>Post a Tweet</h3>
                    <form onSubmit={handlePostTweet}>
                        <input
                            type="text"
                            placeholder="What's happening?"
                            value={tweetContent}
                            onChange={(e) => setTweetContent(e.target.value)}
                            required
                        />
                        <button type="submit">Tweet</button>
                    </form>
                </div>
            )}

            <h3>Tweets</h3>
            <ul className="tweet-list">
                {userData.tweets.map((tweet) => (
                    <li key={tweet.id} className="tweet-card">
                        {editingTweet === tweet.id ? (
                            <div className="edit-box">
                                <input
                                    type="text"
                                    value={newContent}
                                    onChange={(e) => setNewContent(e.target.value)}
                                />
                                <button onClick={() => handleSaveEdit(tweet.id)}>Save</button>
                                <button onClick={() => setEditingTweet(null)}>Cancel</button>
                            </div>
                        ) : (
                            <div className="tweet-content">
                                <p>{tweet.content}</p>
                                <small>({tweet.timestamp})</small>
                                {loggedInUser === userData.username && (
                                    <div className="tweet-actions">
                                        <button onClick={() => handleEditTweet(tweet)}>Edit</button>
                                        <button className="delete-btn" onClick={() => handleDeleteTweet(tweet.id)}>Delete</button>
                                    </div>
                                )}
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Profile;
