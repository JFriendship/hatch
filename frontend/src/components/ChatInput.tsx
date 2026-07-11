import { useState } from "react";
import "./ChatInput.css"

export function ChatInput({ onSend }) {

    const [text, setText] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();

        if (!text.trim()) return; 

        const prompt = text;

        setText("");
        await onSend(prompt);
        
    }

    return (
        <form className="input-container" onSubmit={handleSubmit}>
            <input 
                className="chat-input"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Chat here..."
            />
            <button  className="submit-text-button">
                Submit
            </button>  
        </form>
    );
}
