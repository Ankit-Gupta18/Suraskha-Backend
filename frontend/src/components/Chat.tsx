import React, { useEffect, useState } from "react";
import MessageList from "./MessageList";

interface ChatProps {
  userId: number;
  receiverId: number;
  setConnected: (connected: boolean) => void;
}

const Chat: React.FC<ChatProps> = ({ userId, receiverId, setConnected }) => {
  const [messages, setMessages] = useState<{ sender: string; text: string; timestamp: string }[]>([]);
  const [message, setMessage] = useState<string>("");
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    console.log("Initializing WebSocket connection for", userId, receiverId);
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${userId}/${receiverId}`);

    ws.onopen = () => {
      console.log("WebSocket connected");
      addMessage("System", "Connected to chat.");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.history) {
        data.history.forEach((msg: { sender_id: number; message: string; timestamp: string }) => {
          addMessage(msg.sender_id === userId ? "You" : "Receiver", msg.message, msg.timestamp);
        });
      } else if (data.sender_id && data.message) {
        addMessage("Receiver", data.message, new Date().toISOString());
      } else if (data.system) {
        addMessage("System", data.system);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
      addMessage("System", "Disconnected from chat.");
      setConnected(false);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      alert("WebSocket error. Check console for details.");
    };

    setWebsocket(ws);

    return () => {
      ws.close();
    };
  }, [userId, receiverId]);

  const addMessage = (sender: string, text: string, timestamp: string = new Date().toISOString()) => {
    setMessages((prev) => [...prev, { sender, text, timestamp }]);
  };

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && websocket?.readyState === WebSocket.OPEN) {
      websocket.send(message);
      addMessage("You", message);
      setMessage("");
    }
  };

  return (
    <div className="chat-box">
      <MessageList messages={messages} />
      <form className="send-form" onSubmit={sendMessage}>
        <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Type your message..." autoComplete="off" />
        <button type="submit" disabled={!message.trim()}>Send</button>
      </form>
      <button onClick={() => setConnected(false)}>Disconnect</button>
    </div>
  );
};

export default Chat;
