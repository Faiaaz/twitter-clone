import React, { useState, useEffect } from "react";
import TweetCard from "../components/TweetCard";
import UserSearch from "../components/UserSearch";
import { fetchAllTweets, fetchUserTweets } from "../api/api";

function Home() {
  const [tweets, setTweets] = useState([]);
  const [searchUsername, setSearchUsername] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    getAllTweets();
  }, []);

  const getAllTweets = async () => {
    try {
      const tweets = await fetchAllTweets();
      setTweets(tweets);
    } catch (err) {
      console.error("Error fetching tweets:", err);
    }
  };

  const handleSearchUser = async () => {
    if (!searchUsername.trim()) {
      setError("Please enter a username.");
      return;
    }

    try {
      const data = await fetchUserTweets(searchUsername);
      if (data.error) {
        setError("User not found.");
        setTweets([]);
      } else {
        setError("");
        setTweets(data.tweets);
      }
    } catch (err) {
      setError("Error searching for user.");
    }
  };

  return (
    <div className="container">
      <UserSearch
        searchUsername={searchUsername}
        setSearchUsername={setSearchUsername}
        onSearch={handleSearchUser}
        onClear={getAllTweets}
      />

      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

      <h2 style={{ textAlign: "center", marginTop: "20px" }}>All Tweets</h2>

      <div className="tweet-list" style={{ marginTop: "20px" }}>
        {tweets.map((tweet) => (
          <TweetCard key={tweet.id} tweet={tweet} />
        ))}
      </div>
    </div>
  );
}

export default Home;
