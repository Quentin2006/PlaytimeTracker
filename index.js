// Fetch the JSON file and handle the response

fetch("./data.json")
  .then((response) => response.json())
  .then((data) => {
    console.log(data); // Debugging purpose
    createImgs(data);
    showData(data);

    document.querySelector("#add-game").addEventListener("input", () => {
      addGame(data);
    });
    document.querySelector("#remove-game").addEventListener("input", () => {
      removeGame(data);
    });
    document.querySelector("#change-playtime").addEventListener("input", () => {
      changePlaytime(data);
    });
    document.querySelector("#change-icon").addEventListener("input", () => {
      changeIcon(data);
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
  let existingGame = false;

  data["Game"].forEach((game) => {
    if (fileName == game["Name"]) existingGame = true;
    console.log(fileName);
  });

  if (existingGame) {
    alert("Game already incuded");
  } else {
    let newData = {
      Name: fileName,
      IconURL: "",
      Playtime: 0,
    };
    data.Game.push(newData);

    let fileToSave = new Blob([JSON.stringify(data)], {
      type: "application/json",
    });
    // not a fan of this
    saveAs(fileToSave, "data.json");
  }
}
function removeGame(data) {
  let fileName = document.getElementById("remove-game").files[0].name;
  fileName = fileName.replace(".exe", "");
  let existingGame = false;

  data["Game"].forEach((game) => {
    if (fileName == game["Name"]) existingGame = true;
    console.log(fileName);
  });

  if (!existingGame) {
    alert("Game was never added");
  } else {
    // Find the index of the game with the specified name
    let gameIndex = data.Game.findIndex((game) => game.Name === fileName);

    data.Game.splice(gameIndex, 1);

    let fileToSave = new Blob([JSON.stringify(data)], {
      type: "application/json",
    });
    // not a fan of this
    saveAs(fileToSave, "data.json");
  }
}
function changePlaytime(data) {
  let fileName = document.getElementById("change-playtime").files[0].name;
  fileName = fileName.replace(".exe", "");
  let existingGame = false;

  data["Game"].forEach((game) => {
    if (fileName == game["Name"]) existingGame = true;
    console.log(fileName);
  });

  if (!existingGame) {
    alert("Need to add game to change playtime");
  } else {
    // Find the index of the game with the specified name
    let gameIndex = data.Game.findIndex((game) => game.Name === fileName);

    let newPlaytime = prompt("How many hours do you have?") * 60 * 60;

    data["Game"][gameIndex]["Playtime"] = newPlaytime;

    let fileToSave = new Blob([JSON.stringify(data)], {
      type: "application/json",
    });

    // not a fan of this
    saveAs(fileToSave, "data.json");
  }
}

function changeIcon(data) {
  let fileName = document.getElementById("change-icon").files[0].name;
  fileName = fileName.replace(".exe", "");
  let existingGame = false;

  data["Game"].forEach((game) => {
    if (fileName == game["Name"]) existingGame = true;
    console.log(fileName);
  });

  if (!existingGame) {
    alert("Need to add game to change playtime");
  } else {
    // Find the index of the game with the specified name
    let gameIndex = data.Game.findIndex((game) => game.Name === fileName);

    let newIconURL = prompt("What is the img url?");

    data["Game"][gameIndex]["IconURL"] = newIconURL;

    let fileToSave = new Blob([JSON.stringify(data)], {
      type: "application/json",
    });

    // not a fan of this
    saveAs(fileToSave, "data.json");
  }
}
