// Fetch the JSON file and handle the response
fetch("http://127.0.0.1:5000/data-json", { method: "GET" })
  .then((response) => response.json())
  .then((data) => {
    console.log(data); // Debugging purpose
    createImgs(data);
    showData(data);

    document.querySelector("#add-game").addEventListener("input", () => {
      addGame(data);
    });

    // checks if settings page should be launched
    document
      .querySelector(".game-container")
      .addEventListener("contextmenu", (event) => {
        if (
          event.target.tagName.toLowerCase() === "img" ||
          event.target.className === "placeholder"
        ) {
          // Get the immediate parent of the clicked image (the child of the .game-container)
          let immediateParent = event.target.parentElement;

          let gameSelected = immediateParent.className;

          // truns on settings page
          on(gameSelected);

          // all settings to check for

          document
            .querySelector(".remove-game")
            .addEventListener("click", () => {
              console.log(gameSelected);
              removeGame(data, gameSelected);
            });
          document
            .querySelector(".change-playtime")
            .addEventListener("click", () => {
              changePlaytime(data, gameSelected);
            });
          document
            .querySelector(".change-icon")
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
    const className = game["ExeName"].replace(/\s+/g, "-");

    const gameContainer = document.createElement("div");
    gameContainer.className = className;

    if (game["IconURL"] == "None" || game["IconURL"] == "") {
      const content = document.createElement("div");
      content.style.width = "235px";
      content.style.height = "352.5px";
      content.style.backgroundColor = "grey";
      content.textContent = className;
      content.src = game["IconURL"];
      content.className = "placeholder";
      gameContainer.appendChild(content);
    } else {
      const content = document.createElement("img");
      content.src = game["IconURL"];
      gameContainer.appendChild(content);
    }

    mainContainer.appendChild(gameContainer);
  });
}

// used to dispaly last played
function formatDate(dateString) {
  const date = new Date(dateString);

  const year = date.getFullYear();

  const monthNames = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  const month = monthNames[date.getMonth()];

  const day = date.getDate();

  const ordinalSuffix = (n) => {
    const s = ["th", "st", "nd", "rd"];
    const v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  };

  return `${month} ${ordinalSuffix(day)}`;
}

// Function to show additional game data like playtime
function showData(data) {
  data["Game"].forEach((game) => {
    const className = "." + game["ExeName"].replace(/\s+/g, "-");
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
      if (formattedDate in game)
        recentPlaytime.textContent = `Playtime Today: ${(
          game[formattedDate] / 60
        ).toFixed(0)} mins`;
      else {
        // -5 becuse there are three elemts after the recent playtime in the object
        let lastPlayed = Object.keys(game)[Object.keys(game).length - 5];

        if (lastPlayed != undefined)
          recentPlaytime.textContent = "Last played: " + formatDate(lastPlayed);
        else recentPlaytime.textContent = "Not yet played";
      }

      gameInfoContainer.appendChild(recentPlaytime);
      gameContainer.appendChild(gameInfoContainer);
    }
  });
}

function on(gameName) {
  document.getElementById("overlay").style.display = "block";
  document.querySelector(".title").textContent = gameName;
}

function off() {
  document.getElementById("overlay").style.display = "none";
}

// Event listener to detect clicks outside the overlay content
document.addEventListener("click", function (event) {
  const overlay = document.getElementById("overlay");
  const settingsContent = document.getElementById("text");

  // If the overlay is visible and the click is outside the settings content, close the overlay
  if (
    overlay.style.display === "block" &&
    !settingsContent.contains(event.target)
  ) {
    off();
  }
});

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

  location.reload();
}

function addGame(data) {
  let fileInput = document.getElementById("add-game");
  let fileName = fileInput.files[0].name;
  fileName = fileName.replace(".exe", "");
  let existingGame = false;

  data["Game"].forEach((game) => {
    if (fileName == game["ExeName"]) existingGame = true;
    console.log(fileName);
  });

  if (existingGame) {
    alert("Game already incuded");
  } else {
    let newData = {
      ExeName: fileName,
    };
    data.Game.push(newData);

    postData(data);
  }
}
function removeGame(data, gameName) {
  gameName = gameName.replace("-", " ");

  // Find the index of the game with the specified name
  let gameIndex = data.Game.findIndex((game) => game.Name === gameName);

  data.Game.splice(gameIndex, 1);

  postData(data);
}

function changePlaytime(data, gameName) {
  // Find the index of the game with the specified name
  let gameIndex = data.Game.findIndex((game) => game.ExeName === gameName);

  let newPlaytime = prompt("New playtime (hrs)") * 3600;

  data["Game"][gameIndex]["Playtime"] = newPlaytime;

  postData(data);
}

function changeIcon(data, gameName) {
  gameName = gameName.replace("-", " ");

  // Find the index of the game with the specified name
  let gameIndex = data.Game.findIndex((game) => game.Name === gameName);

  console.log(gameIndex);

  let newIcon = prompt("Select the url of the new icon you want");

  data["Game"][gameIndex]["IconURL"] = newIcon;

  postData(data);
}
