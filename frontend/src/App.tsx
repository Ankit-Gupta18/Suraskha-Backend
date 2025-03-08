import React, { useState } from "react";
import ConnectionForm from "./components/ConnectionForm";
import Chat from "./components/Chat";

const App: React.FC = () => {
  const [userId, setUserId] = useState<number | null>(null);
  const [receiverId, setReceiverId] = useState<number | null>(null);
  const [connected, setConnected] = useState<boolean>(false);

  return (
    <div className="chat-container">
      <h2>One-to-One Chat</h2>
      {!connected ? (
        <ConnectionForm
          setUserId={setUserId}
          setReceiverId={setReceiverId}
          setConnected={setConnected}
        />
      ) : (
        <Chat userId={userId!} receiverId={receiverId!} setConnected={setConnected} />
      )}
    </div>
  );
};

export default App;
