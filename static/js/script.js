document.addEventListener("DOMContentLoaded", function () {
    // Theme Toggle (exists on all pages)
    const themeBtn = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    
    if (themeBtn && themeIcon) {
        const currentTheme = localStorage.getItem("theme") || "light";
        document.documentElement.setAttribute("data-theme", currentTheme);
        themeIcon.className = currentTheme === "dark" ? "fas fa-sun" : "fas fa-moon";

        themeBtn.addEventListener("click", () => {
            const theme =
                document.documentElement.getAttribute("data-theme") === "dark"
                ? "light"
                : "dark";
            document.documentElement.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);
            themeIcon.className = theme === "dark" ? "fas fa-sun" : "fas fa-moon";
        });
    }
    
    // Navigation active state handling
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    // Remove active class from all links
    navLinks.forEach(link => {
        link.classList.remove('active');
        
        // Add active class to current page link
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || 
            (linkPath === '/' && currentPath === '') || 
            (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
    
    // Home page specific elements
    const toggleButton = document.getElementById("toggle-button");
    const videoStream = document.getElementById("video-stream");
    const speakButton = document.getElementById("speak-button");
    const clearButton = document.getElementById("clear-button");
    const deleteButton = document.getElementById("deleteButton");
    const videoStatusIndicator = document.getElementById("video-status-indicator");
    const toggleIcon = document.getElementById("toggle-icon");
    const loadingOverlay = document.getElementById("loading-overlay");
    
  
    
    // Only run this code if we're on the home page (these elements exist)
    if (toggleButton && videoStream && videoStatusIndicator) {
        // Set initial state to active
        let isStreaming = true;
        videoStatusIndicator.classList.add("active");
        videoStatusIndicator.querySelector("span").textContent = "Active";
        toggleIcon.className = "fas fa-pause";
        document.getElementById("toggle-text").textContent = "Pause Recognition";

        // Toggle video streaming
        toggleButton.addEventListener("click", () => {
            isStreaming = !isStreaming;
            
            if (isStreaming) {
                videoStream.src = "/video_feed";  // Restart streaming
                videoStatusIndicator.classList.add("active");
                videoStatusIndicator.querySelector("span").textContent = "Active";
                toggleIcon.className = "fas fa-pause";
                document.getElementById("toggle-text").textContent = "Pause Recognition";
                
                // Simulate loading
                loadingOverlay.classList.add("active");
                setTimeout(() => {
                    loadingOverlay.classList.remove("active");
                }, 1500);
            } else {
                videoStream.src = "";  // Stop streaming
                videoStatusIndicator.classList.remove("active");
                videoStatusIndicator.querySelector("span").textContent = "Inactive";
                toggleIcon.className = "fas fa-play";
                document.getElementById("toggle-text").textContent = "Start Recognition";
            }
        });
        
        

        // Fetch detected sentence from the server
        async function fetchSentence() {
            try {
                const response = await fetch("/get_sentence");
                if (!response.ok) throw new Error("Network error");

                const data = await response.json();
                if (data.sentence) {
                    const sentenceInput = document.getElementById("sentence-input");
                    sentenceInput.value = data.sentence;
                    sentenceInput.scrollTop = sentenceInput.scrollHeight;
                }
            } catch (error) {
                console.error("Error fetching sentence:", error);
                document.getElementById("sentence-input").placeholder = "Error fetching sentence...";
            }
        }

        // Fetch sentence every second
        setInterval(fetchSentence, 1000);

        // Trigger text-to-speech when microphone button is clicked
        if (speakButton) {
            speakButton.addEventListener("click", async () => {
                try {
                    const response = await fetch("/speak", { method: "POST" });
                    const data = await response.json();

                    if (data.status === "success") {
                        console.log("Speaking...");
                        const audio = new Audio("/static/audio/speech.mp3"); // Play generated speech
                        audio.play();
                    } else {
                        alert("No sentence to speak!");
                    }
                } catch (error) {
                    console.error("Error triggering speech:", error);
                }
            });
        }

        if (clearButton) {
            clearButton.addEventListener("click", async () => {
                try {
                    const response = await fetch("/clear_sentence", { method: "POST" });
                    const data = await response.json();
            
                    if (data.status === "success") {
                        document.getElementById("sentence-input").value = ""; // Clear text box
                        console.log("Sentence cleared");
                    }
                } catch (error) {
                    console.error("Error clearing sentence:", error);
                }
            });
        }
        
        if (deleteButton) {
            deleteButton.addEventListener("click", async () => {
                try {
                    const response = await fetch("/delete_last_character", { method: "POST" });
                    if (!response.ok) throw new Error("Network error");
            
                    const data = await response.json();
                    if (data.sentence !== undefined) {
                        document.getElementById("sentence-input").value = data.sentence;
                    }
                } catch (error) {
                    console.error("Error deleting last character:", error);
                }
            });
        }
    }
});