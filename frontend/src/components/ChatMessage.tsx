import type { Message } from "../types/chat";
import "./ChatMessage.css";

interface ChatMessageProps {
    message: Message;
}

export function ChatMessage({
    message,
}: ChatMessageProps) {
    return (
        <div className={`message ${message.role}`}>
            <div className="message-text">{message.content}</div>
        </div>
    );
}