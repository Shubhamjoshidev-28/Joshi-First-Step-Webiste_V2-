const SHEET_URL =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5_dEOssprdox5kp_mGKepSSYopvbKtrIy21HcwFqHnz-hFjcxfNeSzRRUNSyejTvl5cF0eoalxCXN/pub?gid=0&single=true&output=csv";

const grid = document.getElementById("galleryGrid");

if (!grid) {
  console.error("galleryGrid not found");
}

/* FETCH DATA FROM GOOGLE SHEET */
fetch(SHEET_URL)
  .then(res => res.text())
  .then(csv => {
    const rows = csv.trim().split("\n").slice(1);

    rows.forEach(row => {
      if (!row.trim()) return;

      // CSV-safe parsing
      const parts = row.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g);
      if (!parts || parts.length < 2) return;

      const title = parts[0]?.replace(/"/g, "").trim();
      const cover = parts[parts.length - 1]?.replace(/"/g, "").trim();
      const date  = parts.length > 2
        ? parts[1]?.replace(/"/g, "").trim()
        : "";

      if (!title || !cover) return;

      const card = document.createElement("div");
      card.className = "gallery-card";

      card.innerHTML = `
        <div class="image-wrapper">
          <img src="${encodeURI(cover)}" alt="${title}" loading="lazy">
        </div>
        <div class="card-info">
          <h3>${title}</h3>
          ${date ? `<span>${date}</span>` : ""}
        </div>
      `;

      grid.appendChild(card);
    });
  })
  .catch(err => {
    console.error("Failed to load activities data", err);
  });
