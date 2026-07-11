import { useState } from 'react'
import './App.css'
import { ChatInput } from './components/ChatInput'
import { sendPrompt } from './api/chat';
import { ChatWindow } from './components/ChatWindow';
import type { Message } from './types/chat';


function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(prompt: string) {

    setMessages((previous) => [
        ...previous,
        {
            role: "user",
            content: prompt,
        }
    ]);

    setLoading(true);

    try {
        const response = await sendPrompt({ prompt });

        setMessages((previous) => [
            ...previous,
            {
                role: "assistant",
                content: response.model_response,
            }
        ]);
    } finally {
        setLoading(false);
    }
  }

  return (
    <>
      <div>
        <div> HATCH </div>
      </div>
      <section id="center">
        <ChatWindow 
          messages={messages}
          loading={loading}
        />

        <ChatInput onSend={handleSend}></ChatInput> 
      </section>

    </>
  )
}

export default App;