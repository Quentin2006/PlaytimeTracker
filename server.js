
const fs = require("fs");

let name = "data.json";

console.log(JSON.parse(fs.readFileSync(name, "utf8")));

export function addGame() {
  console.log("adding game");
}