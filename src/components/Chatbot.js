import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';
import { getTextSelectionContext, getSelectionLocation } from './TextSelectionHelper';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    // Add user message to the chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get selected text and context using our helper
      const selectionContext = getTextSelectionContext();
      const locationContext = getSelectionLocation();

      // Prepare the request payload
      const requestBody = {
        message: inputValue,
        session_id: sessionId || null,
        selected_text: selectionContext?.selectedText || null,
        context_text: selectionContext?.contextText || null,
        location_info: locationContext,
        history: messages.map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      };

      // Call the backend API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID if new one was returned
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
      }

      // Add assistant response to the chat
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        sources: data.sources,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={`chatbot-container ${isOpen ? 'open' : ''}`}>
      {!isOpen ? (
        <button className="chatbot-toggle" onClick={toggleChat}>
          <span role="img" aria-label="chat">💬</span> AI Book Assistant
        </button>
      ) : (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>AI Book Assistant</h3>
            <button className="chatbot-close" onClick={toggleChat}>
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your AI assistant for the AI/Spec-Driven Book.</p>
                <p>Ask me anything about the book content, or select text and ask questions about it!</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`chatbot-message ${message.role}`}
                >
                  <div className="message-content">
                    {message.content}
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <details>
                        <summary>Sources</summary>
                        <ul>
                          {message.sources.slice(0, 3).map((source, index) => (
                            <li key={index}>
                              <strong>Chapter:</strong> {source.chapter_id}
                              {source.section_title && ` - ${source.section_title}`}
                            </li>
                          ))}
                        </ul>
                      </details>
                    </div>
                  )}
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the book..."
              rows="2"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;