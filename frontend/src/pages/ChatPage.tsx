import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import ChatList from "../components/ChatList";
import ChatBox from "../components/ChatBox";
import ChatInput from "../components/ChatInput";
import useWebSocket from "../hooks/useWebSocket";

// Sample user data (Replace this with actual user authentication)
const currentUser = { id: 1, name: "You", avatar: "https://via.placeholder.com/40" };

const users = [
  { id: 1, name: "Alice", avatar: "https://via.placeholder.com/40" },
  { id: 2, name: "Bob", avatar: "https://via.placeholder.com/40" },
  { id: 3, name: "You", avatar: "https://via.placeholder.com/40" }
];

const ChatPage: React.FC = () => {
  const [filteredUsers, setFilteredUsers] = useState(users);
  const [selectedUser, setSelectedUser] = useState<number | null>(null);

  // Avoid connecting if no user is selected
  const { messages, sendMessage } = useWebSocket(currentUser.id, selectedUser);

  return (
    <div className="chat-container">
      <div className="sidebar">
        {/* Pass users & filtered results handler */}
        <SearchBar users={users} onSearchResults={setFilteredUsers} />
        <ChatList users={filteredUsers} onSelectUser={setSelectedUser} />
      </div>
      <div className="chat-main">
        {selectedUser ? (
          <>
            <ChatBox messages={messages} />
            <ChatInput onSend={sendMessage} />
          </>
        ) : (
          <p>Select a user to start chatting</p>
        )}
      </div>
    </div>
  );
};

export default ChatPage;
