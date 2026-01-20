document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatFeed = document.getElementById('chat-feed');
    const loadBtn = document.getElementById('load-data-btn');

    // DEBUG: Check if button exists
        if (sendBtn) {
            console.log("✅ Send Button found!");
            sendBtn.addEventListener('click', handleChat);
        } else {
            console.error("❌ Send Button NOT found. Check HTML ID matches 'send-btn'");
        }
    // --- Event Listeners ---

    // Send on Button Click
    sendBtn.addEventListener('click', handleChat);

    // Send on Enter Key (prevent new line)
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleChat();
        }
    });

    // Load Data Button
    if(loadBtn) {
        loadBtn.addEventListener('click', async () => {
            loadBtn.innerText = "Loading...";
            const result = await loadBackendData(); // from api.js
            alert(result.message);
            loadBtn.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
                Data Loaded
            `;
        });
    }

    // --- Main Logic ---

    let canSend = true;
    
    const pauseQuery = () => {
      let sendPause = setInterval(()=>{
        canSend = true;
        clearInterval(sendPause)
      },2000)  
    }
    
    
    
    async function handleChat() {
        if(!canSend){
          alert("Please Wait 2 seconds for the next query")
          return;
        }
        canSend = false;
        console.log('chat')
        const message = userInput.value.trim();
        if (!message) return;

        // 1. Add User Message to UI
        appendMessage(message, 'user');
        userInput.value = ''; // Clear input
        resizeTextarea(userInput); // Reset height

        // 2. Show Loading State
        const loadingId = appendLoading();

        // 3. Call API
        const data = await askBackend(message); // from api.js

        // 4. Remove Loading and Add AI Response
        removeLoading(loadingId);
        appendMessage(data.reply, 'ai');
        pauseQuery() // para ni dili ma spam goy

    }

    // --- UI Helper Functions ---

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        
        // Convert newlines to breaks for display
        msgDiv.innerText = text; 
        
        chatFeed.appendChild(msgDiv);
        chatFeed.scrollTop = chatFeed.scrollHeight; // Auto scroll to bottom
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', 'ai', 'loading');
        msgDiv.id = id;
        msgDiv.innerText = "...";
        chatFeed.appendChild(msgDiv);
        return id;
    }

    function removeLoading(id) {
        const element = document.getElementById(id);
        if (element) element.remove();
    }

    function resizeTextarea(el) {
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
    }
});