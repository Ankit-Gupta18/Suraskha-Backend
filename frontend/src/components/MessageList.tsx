import React from "react";

interface MessageListProps {
  messages: { sender: string; text: string; timestamp: string }[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="messages">
      {messages.map((msg, index) => (
        <p key={index}>
          <span className={msg.sender === "You" ? "sender" : msg.sender === "Receiver" ? "receiver" : "system"}>
            {msg.sender}:
          </span>{" "}
          {msg.text} [{new Date(msg.timestamp).toLocaleTimeString()}]
        </p>
      ))}
    </div>
  );
};

export default MessageList;
