const BASE_URL = "http://127.0.0.1:5000/api"; // or use process.env.REACT_APP_API_URL

export async function fetchAllTweets() {
  const res = await fetch(`${BASE_URL}/tweets`);
  const data = await res.json();
  return data.tweets;
}

export async function fetchUserTweets(username) {
  const res = await fetch(`${BASE_URL}/user/${username}/tweets`);
  const data = await res.json();
  return data;
}
