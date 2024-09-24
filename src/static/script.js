let isMuted = false;

document.getElementById('start-button').addEventListener('click', function() {
    document.getElementById('start-page').classList.add('hidden');
    document.getElementById('meeting-page').classList.remove('hidden');

    // Start video stream
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            document.getElementById('video').srcObject = stream;
        })
        .catch(error => {
            console.error('Error accessing media devices.', error);
        });
});

document.getElementById('end-button').addEventListener('click', function() {
    document.getElementById('meeting-page').classList.add('hidden');
    document.getElementById('start-page').classList.remove('hidden');
    
    // Stop video stream
    let videoElement = document.getElementById('video');
    let stream = videoElement.srcObject;
    let tracks = stream.getTracks();

    tracks.forEach(function(track) {
        track.stop();
    });

    videoElement.srcObject = null;
});

document.getElementById('audio-button').addEventListener('click', function() {
    isMuted = !isMuted;
    const audioTracks = document.getElementById('video').srcObject.getAudioTracks();
    audioTracks.forEach(track => track.enabled = !isMuted);
    document.getElementById('audio-button').textContent = isMuted ? 'Unmute' : 'Mute';
});

document.getElementById('chat-toggle-button').addEventListener('click', function() {
    document.getElementById('chat-window').classList.toggle('hidden');
});

document.getElementById('send-button').addEventListener('click', function() {
    const message = document.getElementById('chat-input').value;
    if (message.trim() !== '') {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        document.getElementById('chat-messages').appendChild(messageElement);
        document.getElementById('chat-input').value = '';
    }
});

document.getElementById('chat-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('send-button').click();
    }
});