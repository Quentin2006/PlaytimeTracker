// Fetch the JSON file and handle the response

addInput = document.querySelector("#add-game");

fetch("./data.json")
  .then((response) => response.json())
  .then((data) => {
    console.log(data); // Debugging purpose
    createImgs(data);
    showData(data);

    addInput.addEventListener("input", () => {
      addGame(data);
    });
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

function addGame(data) {
  let fileName = document.getElementById("add-game").files[0].name;
  fileName = fileName.replace(".exe", "");
  let alreadyGame = false;

  data["Game"].forEach((game) => {
    if (fileName == game["Name"]) alreadyGame = true;
    console.log(fileName);
  });

  if (alreadyGame) {
    alert("Game already incuded");
  } else {
    let newData = {
      Name: fileName,
    };
    data.Game.push(newData);

    let fileToSave = new Blob([JSON.stringify(data)], {
      type: "application/json",
    });
    //  not a fan of this
    saveAs(fileToSave, "data.json");
  }
}
