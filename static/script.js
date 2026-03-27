// =============================================
// SCHEME SAKHI - script.js
// Voice Input + API Call + Text to Speech
// =============================================

// Track if recognition is active for problem field
let problemRecognition = null;
let isListeningProblem = false;

// =============================================
// MAIN FUNCTION - Get Schemes from Flask
// =============================================
async function getSchemes() {
    const language = document.getElementById('language').value;
    const state    = document.getElementById('state').value.trim();
    const category = document.getElementById('category').value;
    const age      = document.getElementById('age').value.trim();
    const problem  = document.getElementById('problem').value.trim();

    // Validation
    if (!state) {
        alert('Please enter your state / कृपया अपना राज्य दर्ज करें');
        return;
    }
    if (!age) {
        alert('Please enter your age / कृपया अपनी आयु दर्ज करें');
        return;
    }
    if (!problem) {
        alert('Please describe your problem / कृपया अपनी समस्या बताएं');
        return;
    }

    // Show loading state
    const responseBox  = document.getElementById('response-box');
    const responseText = document.getElementById('response-text');
    const btnText      = document.getElementById('btn-text');
    const btnLoader    = document.getElementById('btn-loader');

    responseBox.style.display = 'block';
    responseText.innerHTML = '<div class="loading-text">🔄 Finding best schemes for you...<br>आपके लिए योजनाएं खोज रहे हैं...</div>';
    btnText.style.display  = 'none';
    btnLoader.style.display = 'inline';

    try {
        const response = await fetch('/get-schemes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language, state, category, age, problem })
        });

        const data = await response.json();
        responseText.innerHTML = data.response;

        // Scroll to response
        responseBox.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        responseText.innerHTML = '❌ Something went wrong. Please check your connection and try again.';
    } finally {
        btnText.style.display   = 'inline';
        btnLoader.style.display = 'none';
    }
}

// =============================================
// VOICE INPUT - State field (single word, easy)
// =============================================
function startVoice(fieldId) {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert('Please use Chrome browser for voice feature.\nVoice के लिए Chrome browser उपयोग करें।');
        return;
    }

    const language    = document.getElementById('language').value;
    const recognition = new SpeechRecognition();

    recognition.lang             = language === 'hindi' ? 'hi-IN' : 'en-IN';
    recognition.interimResults   = false;
    recognition.maxAlternatives  = 1;
    recognition.continuous       = false;

    recognition.start();

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById(fieldId).value = transcript;
    };

    recognition.onerror = function (event) {
        console.error('Voice error:', event.error);
        if (event.error !== 'no-speech') {
            alert('Could not hear clearly. Please try again.\nस्पष्ट रूप से बोलें और फिर कोशिश करें।');
        }
    };

    recognition.onend = function () {
        console.log('Recognition ended for', fieldId);
    };
}

// =============================================
// VOICE INPUT - Problem field (longer speech)
// Tap to START, tap again to STOP
// =============================================
function startVoiceProblem() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert('Please use Chrome browser for voice feature.\nVoice के लिए Chrome browser उपयोग करें।');
        return;
    }

    const micBtn = document.getElementById('problem-mic-btn');

    // If already listening — STOP
    if (isListeningProblem && problemRecognition) {
        problemRecognition.stop();
        isListeningProblem = false;
        micBtn.classList.remove('listening');
        micBtn.title = 'Speak your problem';
        return;
    }

    // START listening
    const language    = document.getElementById('language').value;
    problemRecognition = new SpeechRecognition();

    // continuous = true means it keeps listening until you tap stop
    problemRecognition.lang            = language === 'hindi' ? 'hi-IN' : 'en-IN';
    problemRecognition.interimResults  = true;
    problemRecognition.maxAlternatives = 1;
    problemRecognition.continuous      = true;

    problemRecognition.start();
    isListeningProblem = true;
    micBtn.classList.add('listening');
    micBtn.title = 'Tap to stop listening';

    let finalTranscript = '';

    problemRecognition.onresult = function (event) {
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        // Show live feedback in textarea
        const problemField = document.getElementById('problem');
        problemField.value = finalTranscript + interimTranscript;
    };

    problemRecognition.onerror = function (event) {
        console.error('Problem voice error:', event.error);
        isListeningProblem = false;
        micBtn.classList.remove('listening');
        micBtn.title = 'Speak your problem';

        if (event.error === 'not-allowed') {
            alert('Microphone permission denied.\nPlease allow microphone access in Chrome settings.\n\nChrome में microphone permission दें।');
        } else if (event.error !== 'no-speech') {
            alert('Voice error: ' + event.error + '\nPlease try again.');
        }
    };

    problemRecognition.onend = function () {
        isListeningProblem = false;
        micBtn.classList.remove('listening');
        micBtn.title = 'Speak your problem';
        console.log('Problem recognition ended');
    };
}

// =============================================
// TEXT TO SPEECH - Read response aloud
// =============================================
function speakResponse() {
    const text     = document.getElementById('response-text').innerText;
    const language = document.getElementById('language').value;

    if (!text || text.includes('Finding best schemes')) return;

    window.speechSynthesis.cancel();

    // Split into chunks to avoid browser TTS cutoff for long text
    const chunks = splitTextForSpeech(text);

    chunks.forEach(function (chunk, index) {
        const utterance  = new SpeechSynthesisUtterance(chunk);
        utterance.lang   = language === 'hindi' ? 'hi-IN' : 'en-IN';
        utterance.rate   = 0.85;
        utterance.pitch  = 1;
        utterance.volume = 1;
        window.speechSynthesis.speak(utterance);
    });
}

// Split text into chunks under 200 chars for reliable TTS
function splitTextForSpeech(text) {
    const sentences = text.split(/(?<=[।.!?])\s+/);
    const chunks    = [];
    let current     = '';

    sentences.forEach(function (sentence) {
        if ((current + sentence).length < 200) {
            current += sentence + ' ';
        } else {
            if (current) chunks.push(current.trim());
            current = sentence + ' ';
        }
    });

    if (current) chunks.push(current.trim());
    return chunks.length > 0 ? chunks : [text];
}

// =============================================
// STOP SPEECH
// =============================================
function stopSpeech() {
    window.speechSynthesis.cancel();
}
