import React, { useState } from "react";

interface ConnectionFormProps {
  setUserId: (id: number) => void;
  setReceiverId: (id: number) => void;
  setConnected: (connected: boolean) => void;
}

const ConnectionForm: React.FC<ConnectionFormProps> = ({ setUserId, setReceiverId, setConnected }) => {
  const [sender, setSender] = useState<string>("");
  const [receiver, setReceiver] = useState<string>("");

  const handleConnect = () => {
    const senderId = parseInt(sender);
    const receiverId = parseInt(receiver);
    if (isNaN(senderId) || isNaN(receiverId)) {
      alert("Please enter valid user IDs.");
      return;
    }
    setUserId(senderId);
    setReceiverId(receiverId);
    setConnected(true);
  };

  return (
    <div className="connection-form">
      <input type="number" placeholder="Your User ID" value={sender} onChange={(e) => setSender(e.target.value)} />
      <input type="number" placeholder="Receiver User ID" value={receiver} onChange={(e) => setReceiver(e.target.value)} />
      <button onClick={handleConnect}>Connect</button>
    </div>
  );
};

export default ConnectionForm;
