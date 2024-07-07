playtime = '10hrs'
document.getElementById("playtime-ghost").textContent = 'Playtime: ' + playtime;

fetch('/game_info')
    .then(response => response.json())
    .then(data => {
        const games = data.games;
        // Update the HTML with JSON data
        document.getElementById("playtime-ghost").textContent = `Playtime: ${Math.round(games[0].playtime/60/60*10)/10} hrs`;

        if (games[0].recent_playtime == NaN)
            document.getElementById("recent-playtime-ghost").textContent = `Recently Played: ${Math.round(games[0].recent_playtime/60*10)/10} mins`;
        else
            document.getElementById("recent-playtime-ghost").textContent = `Last Played: ${games[0].last_played} `;


        if (games[0].recent_playtime == NaN)
            document.getElementById("recent-playtime-forza").textContent = `Recently Played: ${Math.round(games[1].recent_playtime/60*10)/10} mins`;
        else
            document.getElementById("recent-playtime-forza").textContent = `Last Played: ${games[1].last_played}`;

    })
    .catch(error => console.error('Error fetching JSON:', error));
