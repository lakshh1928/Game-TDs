/* TDS Game Logic - 3-Tier Production Version */

document.addEventListener("DOMContentLoaded", () => {
    
    // --- Configuration ---
    const API_URL = "/api/players"; 
    let players = []; 

    // --- Select Elements ---
    const playerInput = document.getElementById("player-input");
    const addPlayerBtn = document.getElementById("add-player");
    const playerListDiv = document.getElementById("players-list");
    const spinBtn = document.getElementById("spin-btn");
    const wheel = document.getElementById("wheel");

    // --- 1. CORE API FUNCTIONS ---

    // GET: Fetch players from Database
    async function fetchPlayers() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error("Backend unreachable");
            players = await response.json();
            return true;
        } catch (error) {
            console.error("API Error:", error);
            return false;
        }
    }

    // POST: Add player to Database
    async function handleAddPlayer() {
        if (!playerInput) return;
        const name = playerInput.value.trim();
        
        if (name === "") return alert("Please enter a name!");
        if (players.includes(name)) return alert("Player already exists!");

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name })
            });
            
            if (response.ok) {
                playerInput.value = "";
                await refreshUI();
            }
        } catch (error) {
            alert("Failed to add player. Is the Backend running?");
        }
    }

    // DELETE: Remove player from Database
    window.removePlayer = async (name) => {
        try {
            const response = await fetch(`${API_URL}/${name}`, { method: 'DELETE' });
            if (response.ok) await refreshUI();
        } catch (error) {
            console.error("Delete failed:", error);
        }
    };

    // --- 2. UI RENDERING ---

    async function refreshUI() {
        await fetchPlayers();
        if (!playerListDiv) return;
        
        playerListDiv.innerHTML = ""; 
        if (players.length === 0) {
            playerListDiv.innerHTML = "<p style='color: #ccc; font-size: 0.9rem;'>No players added yet.</p>";
            return;
        }

        players.forEach((player, index) => {
            const div = document.createElement("div");
            div.style.cssText = `
                background: rgba(255,255,255,0.1); 
                margin: 5px 0; padding: 10px; border-radius: 5px; 
                display: flex; justify-content: space-between;
                align-items: center; border: 1px solid rgba(255,255,255,0.2);
            `;
            div.innerHTML = `
                <span style="color: white; font-weight: bold;">${index + 1}. ${player}</span>
                <button onclick="removePlayer('${player}')" style="background:red; border:none; color:white; border-radius:50%; width:25px; height:25px; cursor:pointer;">&times;</button>
            `;
            playerListDiv.appendChild(div);
        });
    }

    // --- 3. PAGE LOGIC ---

    // PAGE: Setup (game.html)
    if (playerListDiv) {
        refreshUI(); 

        if (addPlayerBtn) addPlayerBtn.addEventListener("click", handleAddPlayer);
        if (playerInput) {
            playerInput.addEventListener("keypress", (e) => {
                if (e.key === "Enter") handleAddPlayer();
            });
        }

        const startBtn = document.getElementById("start-game");
        if (startBtn) {
            startBtn.addEventListener("click", () => {
                if (players.length < 2) {
                    alert("You need at least 2 players to start!");
                } else {
                    window.location.href = "spin.html";
                }
            });
        }
    }

    // PAGE: Spin Wheel (spin.html)
    if (wheel) {
        let currentRotation = 0;
        let isSpinning = false;

        async function initWheel() {
            const success = await fetchPlayers();
            if (!success || players.length === 0) {
                alert("No players found! Returning to setup.");
                window.location.href = "game.html";
                return;
            }
            setupWheel();
        }

        initWheel();

        if (spinBtn) {
            spinBtn.addEventListener("click", () => {
                if (isSpinning) return;
                isSpinning = true;
                spinBtn.disabled = true;
                spinBtn.innerText = "Spinning...";

                const randomDegree = Math.floor(3600 + Math.random() * 360); 
                currentRotation += randomDegree;

                wheel.style.transition = "transform 4s cubic-bezier(0.25, 0.1, 0.25, 1)";
                wheel.style.transform = `rotate(${currentRotation}deg)`;

                setTimeout(() => {
                    isSpinning = false;
                    spinBtn.disabled = false;
                    spinBtn.innerText = "SPIN!";
                    determineWinner(currentRotation);
                }, 4000);
            });
        }
    }

    // --- 4. WHEEL UTILITIES ---

    function setupWheel() {
        const sliceSize = 360 / players.length;
        let gradientString = "";
        const colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#FF
