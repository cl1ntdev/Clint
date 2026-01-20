// CHANGE THIS: Replace with your specific Hugging Face Direct URL
// NOTE: Do NOT use "huggingface.co/spaces/..." Use the ".hf.space" domain.
const BASE_URL = "https://xlintz-clint.hf.space"; 

async function askBackend(message) {
    try {
        const response = await fetch(`${BASE_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });
        
        // Better error handling
        if (!response.ok) {
             const errorData = await response.json();
             throw new Error(errorData.detail || "Server Error");
        }
        
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        // Helpful message for users if the Space is "Sleeping"
        return { reply: "Error: Could not connect. The server might be waking up (this takes ~30s for free tier). Please try again." };
    }
}