// Fetch the JSON file and handle the response
fetch("./data.json")
  .then((response) => response.json())
  .then((data) => {
    console.log(data); // Debugging purpose
    createImgs(data);
    showData(data);
  })
  .catch((error) => {
    console.error("Error fetching or parsing JSON:", error);
  });

// Function to create game icons
function createImgs(data) {
  const mainContainer = document.querySelector(".game-container");

  // Loop through each game in the JSON data
  data["Game"].forEach((game) => {
    // Sanitize class names (replace spaces with hyphens)
    const className = game["Name"].replace(/\s+/g, "-");

    const gameContainer = document.createElement("div");
    gameContainer.className = className;

    const content = document.createElement("img");
    content.src = game["IconURL"];

    gameContainer.appendChild(content);
    mainContainer.appendChild(gameContainer);
  });
}

// Function to show additional game data like playtime
function showData(data) {
  data["Game"].forEach((game) => {
    const className = "." + game["Name"].replace(/\s+/g, "-");
    const gameContainer = document.querySelector(className);

    if (gameContainer) {
      const gameInfoContainer = document.createElement("div");
      gameInfoContainer.className = "gameInfoContainer";

      const playtime = document.createElement("div");
      playtime.textContent = `Total Playtime: ${(
        game["Playtime"] / 3600
      ).toFixed(1)} hrs`;
      gameInfoContainer.appendChild(playtime);

      const currentDate = new Date();
      const formattedDate =
        currentDate.getFullYear() +
        "-" +
        String(currentDate.getMonth() + 1).padStart(2, "0") +
        "-" +
        String(currentDate.getDate()).padStart(2, "0");

      const recentPlaytime = document.createElement("div");
      recentPlaytime.textContent =
        formattedDate in game
          ? `Total Playtime Today: ${(game[formattedDate] / 60).toFixed(
              0
            )} mins`
          : "You haven't played today";

      console.log("Recent Playtime Text:", recentPlaytime.textContent);

      gameInfoContainer.appendChild(recentPlaytime);
      gameContainer.appendChild(gameInfoContainer);
    } else {
      console.error(`Could not find element with class: ${className}`);
    }
  });
}

function on() {
  document.getElementById("overlay").style.display = "block";
}

function off() {
  document.getElementById("overlay").style.display = "none";
}

function removeGame() {
  document
    .getElementById("add-game")
    .addEventListener("change", function (event) {
      const file = event.target.files[0]; // Get the first file

      // Check if a file is selected
      if (file) {
        fileName = file.name; // Display the file name
        return fileName;
      } else {
        fileName = "No file selected";
        return fileName;
      }
    });
}

console.log(removeGame());
