// Fetch the JSON file and handle the response
fetch("http://127.0.0.1:5000/data-json", { method: "GET" })
  .then((response) => response.json())
  .then((data) => {
    console.log(data); // Debugging purpose
    createImgs(data);
    showData(data);

    // checks if settings page should be launched
    document
      .querySelector(".game-container")
      .addEventListener("click", (event) => {
        if (event.target.tagName.toLowerCase() === "img") {
          // Get the immediate parent of the clicked image (the child of the .game-container)
          let immediateParent = event.target.parentElement;

          let gameSelected = immediateParent.className;

          console.log(
            "Clicked on a grandchild image. Immediate parent class name:" +
              gameSelected
          );

          // truns on settings page
          on();

          // all settings to check for
          document
            .querySelector(".remove-game")
            .addEventListener("click", () => {
              removeGame(data, gameSelected);
            });
          document
            .querySelector("#change-playtime")
            .addEventListener("click", () => {
              changePlaytime(data, gameSelected);
            });
          document
            .querySelector("#change-icon")
            .addEventListener("click", () => {
              changeIcon(data, gameSelected);
            });
        }
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

function postData(data) {
  fetch("http://127.0.0.1:5000/update-json", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data); // Should log: {key: "value"}
    })
    .catch((error) => {
      console.error("Error:", error);
    });
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

    postData(data);
  }
}
function removeGame(data, gameName) {
  // Find the index of the game with the specified name
  let gameIndex = data.Game.findIndex((game) => game.Name === gameName);

  data.Game.splice(gameIndex, 1);

  postData(data);
}

function changePlaytime(data, gameName) {
  // Find the index of the game with the specified name
  let gameIndex = data.Game.findIndex((game) => game.Name === gameName);

  let newPlaytime = document.getElementById("change-playtime").value * 3600;

  data["Game"][gameIndex]["Playtime"] = newPlaytime;

  postData(data);
}

function changeIcon(data, gameName) {
  // Find the index of the game with the specified name
  let gameIndex = data.Game.findIndex((game) => game.Name === gameName);

  let newPlaytime = document.getElementById("change-icon").value;

  data["Game"][gameIndex]["IconURL"] = newPlaytime;

  postData(data);
}
