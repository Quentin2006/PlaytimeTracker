// Function to fetch game list from Flask backend
async function fetchGameList() {
    const response = await fetch('/get_game_list'); // Fetch from Flask route
    const data = await response.json(); // Parse JSON response
    return data.games; // Return the list of games
}

// Function to process and use the fetched game list
async function createGameDivs() {
    const container = document.getElementById("gameList");
    const gamesList = await fetchGameList(); // Await the result of the fetchGameList function

    // Iterate over the list of values
    gamesList.forEach(game => {
        // Create a new div element
        const newDiv = document.createElement("div");
        
        // Set the content of the div
        newDiv.textContent = game;
        
        // Optionally, you can set other attributes or styles
        newDiv.className = "dynamic-div";
        
        // Append the new div to the container
        container.appendChild(newDiv);
    });
}

async function fetchGamePlaytime() {
    const response = await fetch('/get_playtime_list'); // Fetch from Flask route
    const data = await response.json(); // Parse JSON response
    return data.playtimes; // Return the list of games
}

async function createPlaytimeDivs() {
    const container = document.getElementById("playtimeList");
    const playtimeList = await fetchGamePlaytime(); // Await the result of the fetchGameList function

    // Iterate over the list of values
    playtimeList.forEach(playtime => {
        // Create a new div element
        const newDiv = document.createElement("div");
        
        // Set the content of the div
        newDiv.textContent = playtime;
        
        // Optionally, you can set other attributes or styles
        newDiv.className = "dynamic-div";
        
        // Append the new div to the container
        container.appendChild(newDiv);
    });
}

// Call the createGameDivs function
createGameDivs();
createPlaytimeDivs();