import React from 'react';
import ChatMessage from './ChatMessage';

interface ChatBoxProps {
  messages: { sender: boolean; message: string; avatar: string }[];
}

const ChatBox: React.FC<ChatBoxProps> = ({ messages }) => {
  return (
    <div className="chat-box">
      {messages.map((msg, index) => (
        <ChatMessage key={index} {...msg} />
      ))}
    </div>
  );
};

export default ChatBox;
