import React, { useState } from "react";
import axios from "axios";
import "./ServiceManual.css";

function ServiceManual() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(""); // State to store the response
  const [isLoading, setIsLoading] = useState(false); // State to show loading indicator
  const [error, setError] = useState(""); // State to show error message

  React.useEffect(() => {
    document.title = "Aprilia STX 150 Service Manual";
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent default form submission
    setIsLoading(true); // Show loading indicator

    try {
      // Make a POST request to your endpoint with the message data
      const response = await axios.post("http://localhost:8000/query", {
        query: message,
      });

      // Set the response to be displayed
      console.log(response.data.answer);
      setResponse(response.data.answer);
      setError(""); // Clear any previous error
    } catch (error) {
      console.error("Error sending message:", error);
      setError("Failed to send message. Please try again.");
    } finally {
      setIsLoading(false); // Hide loading indicator
    }

    setMessage("");
  };

  return (
    <div className="container">
      <h1>Aprilia STX 150 Service Manual</h1>

      <form onSubmit={handleSubmit} className="form">
        <label className="label">
          Message:
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Enter your message"
            className="input"
          />
        </label>
        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? "Sending..." : "Send"}
        </button>
      </form>

      {/* Display Response */}
      {response && (
        <div className="response">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}

      {/* Display Error Message */}
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default ServiceManual;
