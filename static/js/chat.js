document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    function addMessage(username, message, time) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `
            <strong>${username}</strong> <span class="time">${time}</span>: ${message}
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            socket.emit('message', { message: message });
            messageInput.value = '';
        }
    });
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
    
    socket.on('message', function(data) {
        addMessage(data.username, data.message, data.time);
    });
});