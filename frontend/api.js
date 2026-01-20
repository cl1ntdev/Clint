const BASE_URL = "http://127.0.0.1:8080";

// 1. Function to Ask the AI
async function askBackend(message) {
    try {
        const response = await fetch(`${BASE_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) throw new Error("Server Error");
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return { reply: "Error: Could not connect to the AI server." };
    }
}

// 2. Function to Load Data (Trigger the /load-txt endpoint)
async function loadBackendData() {
    try {
        const response = await fetch(`${BASE_URL}/load-txt`, {
            method: "POST"
        });
        return await response.json();
    } catch (error) {
        console.error("Load Data Error:", error);
        return { message: "Failed to load data." };
    }
}