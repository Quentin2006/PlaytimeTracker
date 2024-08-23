fetch("./data.json")
  .then((response) => response.json())
  .then((data) => {
    // Do something with the JavaScript object
    console.log(data);
    createImgs(data);
    showData(data);
  })
  .catch((error) => {
    console.error("Error fetching or parsing JSON:", error);
  });

// creates game icons
function createImgs(data) {
  const container = document.querySelector(".game-img-container");

  for (let i = 0; i < data["Game"].length; i++) {
    const content = document.createElement("img");
    content.src = data["Game"][i]["IconURL"];

    container.appendChild(content);
  }
}
function showData(data) {
  const container = document.querySelector(".game-data-container");

  for (let i = 0; i < data["Game"].length; i++) {
    // shows playtime
    const playtime = document.createElement("div");
    playtime.textContent = data["Game"][i]["Playtime"];
    container.appendChild(playtime);

    // shows recent playtime
    const currentDate = new Date();
    const formattedDate =
      currentDate.getFullYear() +
      "-" +
      String(currentDate.getMonth() + 1).padStart(2, "0") +
      "-" +
      String(currentDate.getDate()).padStart(2, "0");

    const recentPlaytime = document.createElement("div");
    if (formattedDate in data["Game"][i]) {
      recentPlaytime.textContent = data["Game"][i][formattedDate];
    } else recentPlaytime.textContent = "You havent played today";
    container.appendChild(recentPlaytime);
  }
}
