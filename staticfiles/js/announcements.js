const SHEET_CSV_URL =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHj9y0LOWqSLoZfmPmJ3wJFM-Lic2JZJRGjfkYcSoZMu0KME20EReWW2OZSZ-C-jkz42oGBbWAk9a4/pub?gid=0&single=true&output=csv";

fetch(SHEET_CSV_URL)
  .then(res => res.text())
  .then(csv => {
    const rows = csv.trim().split("\n");
    rows.shift(); // remove header row

    const container = document.getElementById("announcementsList");
    container.innerHTML = ""; // clear loading

    rows.reverse().forEach(row => {
      const cols = row.split(",");

      const date = cols[0] || "";
      const title = cols[1] || "";
      const message = cols[2] || "";

      const card = document.createElement("div");
      card.className = "announcement-card";

      card.innerHTML = `
        <div class="icon">📅</div>
        <div>
          <span class="date">${date}</span>
          <h4>${title}</h4>
          <p>${message}</p>
        </div>
      `;

      container.appendChild(card);
    });
  })
  .catch(err => {
    console.error("Error loading sheet:", err);
    document.getElementById("announcementsList").innerHTML =
      "<p style='color:#ff6666'>Unable to load announcements.</p>";
  });
