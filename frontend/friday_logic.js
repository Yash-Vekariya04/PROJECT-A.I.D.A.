const core = document.getElementById('friday-core');
const initBtn = document.getElementById('init-btn');
const statusText = document.getElementById('status-text');
        
let ws;
let audioContext;
let analyser;
let microphone;

// 1. Establish the WebSocket Connection
function connectServer() {
    ws = new WebSocket("ws://127.0.0.1:8000/ws/friday");
    ws.onopen = () => { statusText.innerText = "Connected to Local Server. Awaiting Audio Context."; };
    ws.onclose = () => { 
        statusText.innerText = "Connection lost. Reconnecting..."; 
        setTimeout(connectServer, 2000); // Exponential backoff simulation
    };
}

// 2. Initialize the Audio Engine (Requires User Click)
initBtn.addEventListener('click', async () => {
    initBtn.style.display = 'none'; // Hide the button
    statusText.innerText = "Requesting microphone access...";

    try {
        // Request microphone permissions
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                
        // Set up the Web Audio API
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        
        // Connect the microphone to the analyzer
        microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);

        statusText.innerText = "F.R.I.D.A.Y. Audio Matrix Online.";
                
        // Start the animation loop
        animateHologram();
                
        // 1. Set up the Media Recorder
        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        // 2. The Event Listener: What to do when a chunk of audio is ready
        mediaRecorder.ondataavailable = (event) => {
            // If we actually recorded sound, and the WebSocket is open
            if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
                // Fire the raw binary audio chunk down the tunnel to Python!
                ws.send(event.data); 
            }
        };

        // 3. Start recording, and chop the audio into 500-millisecond chunks
        mediaRecorder.start(500); 

        statusText.innerText = "F.R.I.D.A.Y. Audio Matrix Online. Streaming Voice...";

        } catch (err) {
            statusText.innerText = "Error: Microphone access denied.";
            console.error(err);
        }
});

// 3. The Real-Time Animation Loop
function animateHologram() {
    // Read the current volume level (0 to 255)
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(dataArray);
            
    // Calculate average volume
    let sum = 0;
    for(let i = 0; i < dataArray.length; i++) { sum += dataArray[i]; }
    let averageVolume = sum / dataArray.length;

    // Math: Map the volume to a CSS scale value (1.0 to 1.5)
    let scale = 1 + (averageVolume / 150);
    let glow = 50 + averageVolume;

    // Apply the math physically to the HTML element
    core.style.transform = `scale(${scale})`;
    core.style.boxShadow = `0 0 ${glow}px #00ffcc, inset 0 0 30px #ffffff`;

    // Call this function again before the next screen repaint (60fps)
    requestAnimationFrame(animateHologram);
}

// Boot the connection script
connectServer();