import React, { useEffect, useRef, useState } from 'react';

const AudioPlayer = ({ audioSrc }) => {
    const audioRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);

    useEffect(() => {
        const audio = audioRef.current;

        const updateCurrentTime = () => {
            setCurrentTime(audio.currentTime);
        };

        audio.addEventListener('timeupdate', updateCurrentTime);
        audio.addEventListener('loadedmetadata', () => {
            setDuration(audio.duration);
        });

        return () => {
            audio.removeEventListener('timeupdate', updateCurrentTime);
        };
    }, []);

    const togglePlayback = () => {
        const audio = audioRef.current;
        if (isPlaying) {
            audio.pause();
        } else {
            audio.play();
        }
        setIsPlaying(!isPlaying);
    };

    const handleSeek = (event) => {
        const seekTime = (event.target.value / 100) * duration;
        audioRef.current.currentTime = seekTime;
    };

    return (
        <div>
            <audio ref={audioRef} src={audioSrc} />
            <button onClick={togglePlayback}>
                {isPlaying ? 'Pause' : 'Play'}
            </button>
            <input
                type="range"
                value={(currentTime / duration) * 100 || 0}
                onChange={handleSeek}
                disabled={duration === 0}
            />
            <div>
                {Math.floor(currentTime)} / {Math.floor(duration)} seconds
            </div>
        </div>
    );
};

export default AudioPlayer;