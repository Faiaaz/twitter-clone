import React from "react";
import { Link } from "react-router-dom";

function TweetCard({ tweet }) {
  return (
    <div className="tweet-card" style={{
      border: "1px solid #ccc",
      padding: "10px",
      marginBottom: "10px",
      borderRadius: "8px",
      backgroundColor: "#f9f9f9"
    }}>
      <Link to={`/profile/${tweet.user}`} style={{ textDecoration: "none", color: "#333" }}>
        <strong>{tweet.user}</strong>
      </Link>
      <p>{tweet.content}</p>
      <small style={{ color: "#888" }}>{tweet.timestamp}</small>
    </div>
  );
}

export default TweetCard;
