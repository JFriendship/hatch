import { ChatMessage } from "./ChatMessage";
import type { Message } from "../types/chat";
import "./ChatWindow.css"

interface ChatWindowProps {
    messages: Message[];
    loading: boolean;
}

export function ChatWindow({
    messages,
    loading,
}: ChatWindowProps) {
    return (
        <div className="chat-window" id="chat-window">
            {messages.map((message, index) => (
                <ChatMessage
                    key={index}
                    message={message}
                />
            ))}

            {loading && (
                <p>Language Model is thinking...</p>
            )}
        </div>
    );
}