import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css'
import SendButton from './assets/SendButton.svg';
import userLogo from './assets/userlogo.svg';
import botLogo from './assets/botlogo.svg';

const ChatInterface = ({ disabled, newUpload }) => {
    const msgEnd = useRef(null)
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);

    const [answering, setAnswering] = useState(false);

    useEffect(() => {
        msgEnd.current.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        setMessages([]);
    }, [newUpload])

    const handleSendMessage = async () => {
        if (input === '' || disabled || answering) return;

        const query = input;
        setInput('');

        setMessages(prevMessages => [...prevMessages, { text: query, sender: 'user' }])

        setAnswering(true)

        try {
            const response = await fetch('http://127.0.0.1:8000/handle-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: query })
            });

            if (response.ok) {
                const data = await response.json();
                setMessages(prevMessages => [...prevMessages, { text: data.answer, sender: 'bot' }])

            } else {
                throw new Error('Failed to get response from server');
            }
        } catch (error) {
            console.error('Error handling query:', error);
            setMessages(prevMessages => [...prevMessages, { text: 'Error: Please try again!', sender: 'bot' }]);
        } finally {
            setAnswering(false);
        }

        // setMessages([...messages, { text: query, sender: 'user' }]);
        // const res = await sendMsgtoLLAMA(query);
        // const res = 'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Deleniti voluptates esse temporibus voluptatibus, laborum optio adipisci! Expedita natus vitae necessitatibus. Doloremque vero eos impedit perferendis dolores harum suscipit unde placeat?';
        // console.log(res);
    };

    const handleEnter = async (e) => {
        if (e.key === 'Enter') await handleSendMessage();
    }

    return (
        <div className="chat-interface">
            <div className="messages">
                {messages.map((message, index) => (
                    <div key={index} className={message.sender === 'user' ? 'user-message' : 'bot-message'}>
                        <img className='messageImg' src={message.sender === 'user' ? userLogo : botLogo} alt="messageImg" />
                        <p className='txt'>{message.text}</p>
                    </div>
                ))}
                <div ref={msgEnd} />
            </div>
            <div className="input-field">
                <div className="inp">
                    <input type="text" placeholder="Send a message..." value={input} onKeyDown={handleEnter} onChange={(e) => { setInput(e.target.value) }} />
                    <button className='send' onClick={() => handleSendMessage()}><img src={SendButton} alt="Send" /></button>
                </div>
            </div>
        </div>
    );
};

export default ChatInterface;