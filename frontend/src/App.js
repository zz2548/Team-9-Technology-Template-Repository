import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  // Fetch messages from the backend
  useEffect(() => {
    const fetchMessages = async () => {
      const response = await axios.get("http://localhost:5000/messages");
      setMessages(response.data);
    };
    fetchMessages();
  }, []);

  // Handle sending a message
  const sendMessage = async () => {
    if (username && message) {
      await axios.post("http://localhost:5000/messages", {
        username,
        content: message,
      });
      setMessage(""); // Clear input field after sending
      // Refresh messages after sending
      const response = await axios.get("http://localhost:5000/messages");
      setMessages(response.data);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Chat Application</h1>
      <div>
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <br />
        <textarea
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        ></textarea>
        <br />
        <button onClick={sendMessage}>Send</button>
      </div>
      <div style={{ marginTop: "20px" }}>
        <h2>Messages:</h2>
        {messages.map((msg, index) => (
          <p key={index}>
            <strong>{msg.user}:</strong> {msg.content}
          </p>
        ))}
      </div>
    </div>
  );
};

export default App;
