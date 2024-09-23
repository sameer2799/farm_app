import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8001', // Backend service URL
});

export default instance;