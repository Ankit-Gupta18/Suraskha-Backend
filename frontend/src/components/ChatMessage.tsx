import React from 'react';

interface ChatMessageProps {
  message: string;
  sender: boolean;
  avatar: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, sender, avatar }) => {
  return (
    <div className={`chat-message ${sender ? 'sent' : 'received'}`}>
      {!sender && <img src={avatar} alt="Profile" className="message-avatar" />}
      <p>{message}</p>
    </div>
  );
};

export default ChatMessage;
