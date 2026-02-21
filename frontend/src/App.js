import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { text: "Hello! I am your medical assistant. Ask me anything from the Medical Book.", sender: "bot" }
  ]);
  const [loading, setLoading] = useState(false);
  
  // Ref to automatically scroll to the bottom
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages(prev => [...prev, userMessage]);
    const userQuestion = input;
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/chat", {
        question: userQuestion
      });

      setMessages(prev => [...prev, { text: response.data.answer, sender: "bot" }]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages(prev => [...prev, { text: "Error: Could not connect to the server.", sender: "bot" }]);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <div className="chat-box">
        <header className="header">
          <h2>Medical Chatbot</h2>
        </header>
        
        <div className="messages-container">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
          {loading && <div className="loading">Bot is thinking...</div>}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask a medical question..."
          />
          <button className="send-button" onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;