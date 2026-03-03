const modelOrder = [
  "qwen3_32b",
  "gemini2.5_flash_lite",
  "llama4_maverick",
  "nvidia_nemotron_12b",
  "llama3.2_11b",
  "gemma3_12b",
  "internVL"
];

let modelsData = {};
let transcriptsData = {};
let aggregatedData = [];
let currentSort = { key: "total", asc: false };

function colorize(value, max) {
  const ratio = value / max;
  const bg = d3.interpolateRdYlGn(ratio);

  // TEXT COLOR RULE:
  // White only if 81% and above
  const text = ratio >= 0.81 ? "white" : "black";

  return `
    background-color:${bg};
    color:${text};
    font-weight:600;
    border:2px solid #2e333b;
  `;
}

async function loadData() {

  for (const model of modelOrder) {
    const res = await fetch(`evaluation_results/${model}.json`);
    modelsData[model] = await res.json();
  }

  for (const model of modelOrder) {
    const res = await fetch(`${model}_direct.json`);
    transcriptsData[model] = await res.json();
  }

  computeAggregates();
  renderAggregatedTable();
  renderStripLeaderboard();
  renderModelTables();
}

function computeAggregates() {
  aggregatedData = modelOrder.map(model => {
    const data = modelsData[model];
    let word = 0, speaker = 0, panel = 0, halluc = 0;

    data.forEach(entry => {
      word += entry.scores.word_accuracy;
      speaker += entry.scores.speaker_accuracy;
      panel += entry.scores.panel_structure;
      halluc += entry.scores.hallucination;
    });

    const n = data.length;

    return {
      name: model,
      total: (word + speaker + panel + halluc) / n,
      word: word / n,
      speaker: speaker / n,
      panel: panel / n,
      halluc: halluc / n
    };
  });
}

function getSortIcon(key) {
  if (currentSort.key !== key) return "⇅";
  return currentSort.asc ? "▲" : "▼";
}

window.sortAggregated = function (key) {
  if (currentSort.key === key) currentSort.asc = !currentSort.asc;
  else {
    currentSort.key = key;
    currentSort.asc = false;
  }
  renderAggregatedTable();
};

function renderAggregatedTable() {

  const sorted = [...aggregatedData].sort((a, b) => {
    if (a[currentSort.key] < b[currentSort.key]) return currentSort.asc ? -1 : 1;
    if (a[currentSort.key] > b[currentSort.key]) return currentSort.asc ? 1 : -1;
    return 0;
  });

  let html = `
    <table class="table table-bordered text-center fw-semibold">
      <thead>
        <tr>
          <th class="sortable" onclick="sortAggregated('name')">Model ${getSortIcon("name")}</th>
          <th class="sortable" onclick="sortAggregated('total')">Overall ${getSortIcon("total")}</th>
          <th class="sortable" onclick="sortAggregated('word')">Word (40) ${getSortIcon("word")}</th>
          <th class="sortable" onclick="sortAggregated('speaker')">Speaker (25) ${getSortIcon("speaker")}</th>
          <th class="sortable" onclick="sortAggregated('panel')">Panel (20) ${getSortIcon("panel")}</th>
          <th class="sortable" onclick="sortAggregated('halluc')">Halluc (15) ${getSortIcon("halluc")}</th>
        </tr>
      </thead>
      <tbody>
  `;

  sorted.forEach(row => {
    html += `
      <tr>
        <td>${row.name}</td>
        <td style="${colorize(row.total, 100)}">${row.total.toFixed(1)}%</td>
        <td style="${colorize(row.word, 40)}">${row.word.toFixed(1)}</td>
        <td style="${colorize(row.speaker, 25)}">${row.speaker.toFixed(1)}</td>
        <td style="${colorize(row.panel, 20)}">${row.panel.toFixed(1)}</td>
        <td style="${colorize(row.halluc, 15)}">${row.halluc.toFixed(1)}</td>
      </tr>
    `;
  });

  html += "</tbody></table>";
  document.getElementById("aggregatedTable").innerHTML = html;
}

function renderStripLeaderboard() {

  const dates = modelsData[modelOrder[0]].map(d => d.date);

  let html = `
    <table class="table table-bordered text-center fw-semibold">
      <thead>
        <tr>
          <th>Date</th>
          ${modelOrder.map(m => `<th>${m}</th>`).join("")}
          <th>Average</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
  `;

  dates.forEach(date => {

    let rowTotal = 0;

    html += `<tr><td>${date}</td>`;

    modelOrder.forEach(model => {
      const entry = modelsData[model].find(d => d.date === date);
      const total =
        entry.scores.word_accuracy +
        entry.scores.speaker_accuracy +
        entry.scores.panel_structure +
        entry.scores.hallucination;

      rowTotal += total;

      html += `<td style="${colorize(total, 100)}">${total.toFixed(1)}%</td>`;
    });

    const avg = rowTotal / modelOrder.length;

    html += `
      <td style="${colorize(avg, 100)}"><strong>${avg.toFixed(1)}%</strong></td>
      <td>
        <button class="btn btn-primary fw-bold"
          onclick="openDetails('${date}')">
          Details
        </button>
      </td>
    </tr>`;
  });

  html += "</tbody></table>";

  document.getElementById("stripLeaderboard").innerHTML = html;
}

window.openDetails = function (date) {

  document.getElementById("detailModalTitle").innerText = `Strip: ${date}`;

  const year = date.split("-")[0];

  document.getElementById("modalImage").src =
    `strip_previews/${year}/${date}.gif`;

  let html = "";

  modelOrder.forEach(model => {

    const entry = transcriptsData[model].find(d => d.date === date);
    if (!entry) return;

    html += `<div class="transcript-block">
      <h6 class="fw-bold">${model}</h6>`;

    entry.prediction.panels.forEach(panel => {
      html += `<div><strong>Panel ${panel.panel_number}</strong></div>`;
      panel.dialogue.forEach(line => {
        html += `<div>${line.speaker}: "${line.text}"</div>`;
      });
    });

    html += `</div>`;
  });

  document.getElementById("modalOutputs").innerHTML = html;

  const modal = new bootstrap.Modal(document.getElementById("detailModal"));
  modal.show();
};

function renderModelTables() {

  let html = "";

  modelOrder.forEach(model => {

    const data = modelsData[model];

    html += `
      <div class="card mb-4">
        <div class="card-header model-title">${model}</div>
        <div class="card-body p-0">
          <table class="table table-bordered text-center fw-semibold mb-0">
            <thead>
              <tr>
                <th>Date</th>
                <th>Word</th>
                <th>Speaker</th>
                <th>Panel</th>
                <th>Halluc</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
    `;

    data.forEach((entry, i) => {

      const total =
        entry.scores.word_accuracy +
        entry.scores.speaker_accuracy +
        entry.scores.panel_structure +
        entry.scores.hallucination;

      const hidden = i >= 5 ? "style='display:none' class='extra'" : "";

      html += `
        <tr ${hidden}>
          <td>${entry.date}</td>
          <td style="${colorize(entry.scores.word_accuracy,40)}">${entry.scores.word_accuracy}</td>
          <td style="${colorize(entry.scores.speaker_accuracy,25)}">${entry.scores.speaker_accuracy}</td>
          <td style="${colorize(entry.scores.panel_structure,20)}">${entry.scores.panel_structure}</td>
          <td style="${colorize(entry.scores.hallucination,15)}">${entry.scores.hallucination}</td>
          <td style="${colorize(total,100)}">${total.toFixed(1)}%</td>
        </tr>
      `;
    });

    html += `
          </tbody>
          </table>
          <div class="p-3 text-center">
            <button class="btn btn-outline-secondary fw-bold"
              onclick="toggleRows(this)">
              Show More
            </button>
          </div>
        </div>
      </div>
    `;
  });

  document.getElementById("modelTables").innerHTML = html;
}

window.toggleRows = function (btn) {
  const rows = btn.closest(".card").querySelectorAll(".extra");
  rows.forEach(row => {
    row.style.display = row.style.display === "none" ? "table-row" : "none";
  });
  btn.innerText = btn.innerText === "Show More" ? "Show Less" : "Show More";
};

loadData();