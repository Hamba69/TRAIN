import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api'; // Adjust the base URL as needed

export const uploadAudio = async (audioFile: File) => {
    const formData = new FormData();
    formData.append('audio', audioFile);

    try {
        const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error uploading audio:', error);
        throw error;
    }
};

export const getTranscription = async (audioId: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/transcriptions/${audioId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching transcription:', error);
        throw error;
    }
};

export const sendMessageToAI = async (message: string) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/ai/message`, { message });
        return response.data;
    } catch (error) {
        console.error('Error sending message to AI:', error);
        throw error;
    }
};

export const fetchRecordings = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/recordings`);
        return response.data;
    } catch (error) {
        console.error('Error fetching recordings:', error);
        throw error;
    }
};