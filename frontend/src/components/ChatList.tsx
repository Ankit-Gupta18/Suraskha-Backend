import React from 'react';

interface ChatUser {
  id: number;
  name: string;
  avatar: string;
}

interface ChatListProps {
  users: ChatUser[];
  onSelectUser: (userId: number) => void;
}

const ChatList: React.FC<ChatListProps> = ({ users, onSelectUser }) => {
  return (
    <ul className="chat-list">
      {users.map((user) => (
        <li key={user.id} onClick={() => onSelectUser(user.id)}>
          <img src={user.avatar} alt={user.name} className="avatar" />
          <span>{user.name}</span>
        </li>
      ))}
    </ul>
  );
};

export default ChatList;
