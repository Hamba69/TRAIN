import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import VoiceRecorder from './components/VoiceRecorder';
import ChatInterface from './components/ChatInterface';
import AudioPlayer from './components/AudioPlayer';

const App: React.FC = () => {
    return (
        <Router>
            <div>
                <h1>Voice AI Demo</h1>
                <Switch>
                    <Route path="/recorder" component={VoiceRecorder} />
                    <Route path="/chat" component={ChatInterface} />
                    <Route path="/player" component={AudioPlayer} />
                    <Route path="/" exact>
                        <h2>Welcome to the Voice AI Demo</h2>
                        <p>Select a feature from the menu.</p>
                    </Route>
                </Switch>
            </div>
        </Router>
    );
};

export default App;