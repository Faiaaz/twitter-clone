import React from "react";

function UserSearch({ searchUsername, setSearchUsername, onSearch, onClear }) {
  return (
    <div className="tweet-box">
      <input
        type="text"
        placeholder="Search user..."
        value={searchUsername}
        onChange={(e) => setSearchUsername(e.target.value)}
      />
      <button onClick={onSearch}>Search</button>
      <button onClick={onClear}>Clear</button>
    </div>
  );
}

export default UserSearch;
