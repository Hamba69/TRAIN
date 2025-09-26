import React, { useState, useEffect, useRef } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { VoiceRecorder } from './VoiceRecorder';
import { AudioPlayer } from './AudioPlayer';

interface ChatInterfaceProps {
    conversationId: string;
    userId: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ conversationId, userId }) => {
    const [messages, setMessages] = useState<any[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [voiceMode, setVoiceMode] = useState(false);
    const wsRef = useRef<WebSocket | null>(null);
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        connectWebSocket();
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
                wsRef.current = null;
            }
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [conversationId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const connectWebSocket = () => {
        wsRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}`);
        wsRef.current.onopen = () => {
            setIsConnected(true);
        };
        wsRef.current.onmessage = (event) => {        import React, { useState, useEffect, useRef } from 'react';
        import { MessageList } from './MessageList';
        import { MessageInput } from './MessageInput';
        import { VoiceRecorder } from './VoiceRecorder';
        import { AudioPlayer } from './AudioPlayer';
        
        interface ChatInterfaceProps {
            conversationId: string;
            userId: string;
        }
        
        const ChatInterface: React.FC<ChatInterfaceProps> = ({ conversationId, userId }) => {
            const [messages, setMessages] = useState<any[]>([]);
            const [isConnected, setIsConnected] = useState(false);
            const [isTyping, setIsTyping] = useState(false);
            const [voiceMode, setVoiceMode] = useState(false);
            const wsRef = useRef<WebSocket | null>(null);
            const messagesEndRef = useRef<HTMLDivElement | null>(null);
        
            useEffect(() => {
                connectWebSocket();
                return () => {
                    if (wsRef.current) {
                        wsRef.current.close();
                        wsRef.current = null;
                    }
                };
                // eslint-disable-next-line react-hooks/exhaustive-deps
            }, [conversationId]);
        
            useEffect(() => {
                scrollToBottom();
            }, [messages]);
        
            const connectWebSocket = () => {
                wsRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}`);
                wsRef.current.onopen = () => {
                    setIsConnected(true);
                };
                wsRef.current.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    setMessages((prevMessages) => [...prevMessages, data]);
                    setIsTyping(false);
                };
                wsRef.current.onclose = () => {
                    setIsConnected(false);
                };
            };
        
            const handleWebSocketMessage = (data: any) => {
                if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                    wsRef.current.send(JSON.stringify(data));
                }
            };
        
            const sendMessage = (content: string, type = 'text') => {
                const message = { content, type, userId };
                handleWebSocketMessage(message);
                setMessages((prevMessages) => [...prevMessages, message]);
            };
        
            const sendVoiceMessage = (audioBlob: Blob, transcribedText: string) => {
                const message = { content: transcribedText, type: 'voice', userId, audioBlob };
                handleWebSocketMessage(message);
                setMessages((prevMessages) => [...prevMessages, message]);
            };
        
            const scrollToBottom = () => {
                messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            };
        
            const handleFeedback = (messageId: string, rating: number, feedbackText = '') => {
                // Handle feedback submission logic here
            };
        
            return (
                <div className="chat-interface">
                    <MessageList messages={messages} isTyping={isTyping} onFeedback={handleFeedback} />
                    <MessageInput onSendMessage={sendMessage} onSendVoiceMessage={sendVoiceMessage} />
                    <AudioPlayer />
                    {/* Optionally render VoiceRecorder if voiceMode is enabled */}
                    {voiceMode && <VoiceRecorder onSendVoiceMessage={sendVoiceMessage} />}
                    <div ref={messagesEndRef} />
                </div>
            );
        };
        
        export default ChatInterface;        import React, { useState, useEffect, useRef } from 'react';
        import { MessageList } from './MessageList';
        import { MessageInput } from './MessageInput';
        import { VoiceRecorder } from './VoiceRecorder';
        import { AudioPlayer } from './AudioPlayer';
        
        interface ChatInterfaceProps {
            conversationId: string;
            userId: string;
        }
        
        const ChatInterface: React.FC<ChatInterfaceProps> = ({ conversationId, userId }) => {
            const [messages, setMessages] = useState<any[]>([]);
            const [isConnected, setIsConnected] = useState(false);
            const [isTyping, setIsTyping] = useState(false);
            const [voiceMode, setVoiceMode] = useState(false);
            const wsRef = useRef<WebSocket | null>(null);
            const messagesEndRef = useRef<HTMLDivElement | null>(null);
        
            useEffect(() => {
                connectWebSocket();
                return () => {
                    if (wsRef.current) {
                        wsRef.current.close();
                        wsRef.current = null;
                    }
                };
                // eslint-disable-next-line react-hooks/exhaustive-deps
            }, [conversationId]);
        
            useEffect(() => {
                scrollToBottom();
            }, [messages]);
        
            const connectWebSocket = () => {
                wsRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}`);
                wsRef.current.onopen = () => {
                    setIsConnected(true);
                };
                wsRef.current.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    setMessages((prevMessages) => [...prevMessages, data]);
                    setIsTyping(false);
                };
                wsRef.current.onclose = () => {
                    setIsConnected(false);
                };
            };
        
            const handleWebSocketMessage = (data: any) => {
                if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                    wsRef.current.send(JSON.stringify(data));
                }
            };
        
            const sendMessage = (content: string, type = 'text') => {
                const message = { content, type, userId };
                handleWebSocketMessage(message);
                setMessages((prevMessages) => [...prevMessages, message]);
            };
        
            const sendVoiceMessage = (audioBlob: Blob, transcribedText: string) => {
                const message = { content: transcribedText, type: 'voice', userId, audioBlob };
                handleWebSocketMessage(message);
                setMessages((prevMessages) => [...prevMessages, message]);
            };
        
            const scrollToBottom = () => {
                messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            };
        
            const handleFeedback = (messageId: string, rating: number, feedbackText = '') => {
                // Handle feedback submission logic here
            };
        
            return (
                <div className="chat-interface">
                    <MessageList messages={messages} isTyping={isTyping} onFeedback={handleFeedback} />
                    <MessageInput onSendMessage={sendMessage} onSendVoiceMessage={sendVoiceMessage} />
                    <AudioPlayer />
                    {/* Optionally render VoiceRecorder if voiceMode is enabled */}
                    {voiceMode && <VoiceRecorder onSendVoiceMessage={sendVoiceMessage} />}
                    <div ref={messagesEndRef} />
                </div>
            );
        };
        
        export default ChatInterface;
            const data = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, data]);
            setIsTyping(false);
        };
        wsRef.current.onclose = () => {
            setIsConnected(false);
        };
    };

    const handleWebSocketMessage = (data: any) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(data));
        }
    };

    const sendMessage = (content: string, type = 'text') => {
        const message = { content, type, userId };
        handleWebSocketMessage(message);
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const sendVoiceMessage = (audioBlob: Blob, transcribedText: string) => {
        const message = { content: transcribedText, type: 'voice', userId, audioBlob };
        handleWebSocketMessage(message);
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleFeedback = (messageId: string, rating: number, feedbackText = '') => {
        // Handle feedback submission logic here
    };

    return (
        <div className="chat-interface">
            <MessageList messages={messages} isTyping={isTyping} onFeedback={handleFeedback} />
            <MessageInput onSendMessage={sendMessage} onSendVoiceMessage={sendVoiceMessage} />
            <AudioPlayer />
            {/* Optionally render VoiceRecorder if voiceMode is enabled */}
            {voiceMode && <VoiceRecorder onSendVoiceMessage={sendVoiceMessage} />}
            <div ref={messagesEndRef} />
        </div>
    );
};

export default ChatInterface;import React, { useState, useEffect, useRef } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { VoiceRecorder } from './VoiceRecorder';
import { AudioPlayer } from './AudioPlayer';

const ChatInterface = ({ conversationId, userId }) => {
    const [messages, setMessages] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [voiceMode, setVoiceMode] = useState(false);
    const wsRef = useRef(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        connectWebSocket();
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [conversationId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const connectWebSocket = () => {
        wsRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${conversationId}`);
        wsRef.current.onopen = () => {
            setIsConnected(true);
        };
        wsRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, data]);
            setIsTyping(false);
        };
        wsRef.current.onclose = () => {
            setIsConnected(false);
        };
    };

    const handleWebSocketMessage = (data) => {
        if (wsRef.current) {
            wsRef.current.send(JSON.stringify(data));
        }
    };

    const sendMessage = (content, type = 'text') => {
        const message = { content, type, userId };
        handleWebSocketMessage(message);
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const sendVoiceMessage = (audioBlob, transcribedText) => {
        const message = { content: transcribedText, type: 'voice', userId, audioBlob };
        handleWebSocketMessage(message);
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleFeedback = (messageId, rating, feedbackText = '') => {
        // Handle feedback submission logic here
    };

    return (
        <div className="chat-interface">
            <MessageList messages={messages} isTyping={isTyping} onFeedback={handleFeedback} />
            <MessageInput onSendMessage={sendMessage} onSendVoiceMessage={sendVoiceMessage} />
            <AudioPlayer />
            <div ref={messagesEndRef} />
        </div>
    );
};

export default ChatInterface;