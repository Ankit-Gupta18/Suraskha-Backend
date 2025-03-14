import { useEffect, useState } from "react";

interface ChatMessage {
  sender_id: number;
  message: string;
  timestamp: string;
}

const useWebSocket = (senderId: number, receiverId: number | null) => {
  const [messages, setMessages] = useState<{ sender: boolean; message: string; avatar: string }[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (!receiverId) return; // Don't connect if no receiver selected

    console.log("Initializing WebSocket connection for", senderId, receiverId);
    const socket = new WebSocket(`ws://localhost:8000/ws/chat/${senderId}/${receiverId}`);

    socket.onopen = () => {
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.history) {
        console.log("Received chat history", data.history);
        setMessages(
          data.history.map((msg: ChatMessage) => ({
            sender: msg.sender_id === senderId,
            message: msg.message,
            avatar: "https://via.placeholder.com/40"
          }))
        );
      } else if (data.sender_id && data.message) {
        console.log("Received message", data);
        setMessages((prev) => [
          ...prev,
          {
            sender: data.sender_id === senderId,
            message: data.message,
            avatar: "https://via.placeholder.com/40"
          }
        ]);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket disconnected");
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    setWs(socket);

    return () => {
      console.log("Closing WebSocket connection");
      socket.close();
    };
  }, [senderId, receiverId]);

  const sendMessage = (message: string) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      console.log("Sending message:", message);
      ws.send(message);
      setMessages((prev) => [
        ...prev,
        {
          sender: true,
          message,
          avatar: "https://via.placeholder.com/40"
        }
      ]);
    }
  };

  return { messages, sendMessage };
};

export default useWebSocket;
