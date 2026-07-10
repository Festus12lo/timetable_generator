(function () {
  const DAYS = window.__DAYS__;
  const boardBody = document.getElementById("board-body");
  const regenBtn = document.getElementById("regenerate");
  const txtBtn = document.getElementById("download-txt");
  const printBtn = document.getElementById("print-view");
  let currentData = null;

  function cellFor(day, i) {
    return boardBody.children[i].querySelector(`[data-day="${CSS.escape(day)}"]`);
  }

  function render(data) {
    currentData = data;
    DAYS.forEach((day) => {
      (data[day] || []).forEach((l, i) => {
        const cell = cellFor(day, i);
        if (!cell) return;
        cell.innerHTML = `
          <div class="card tag-${l.tag}">
            <div class="subject">${l.subject}</div>
            <div class="meta">${l.faculty}<br>${l.room}</div>
          </div>`;
      });
    });
  }

  async function fetchAndRender() {
    regenBtn.disabled = true;
    try {
      const res = await fetch("/api/generate");
      render(await res.json());
    } catch (e) {
      alert("Couldn't reach the server. Is app.py still running?");
    } finally {
      regenBtn.disabled = false;
    }
  }

  function downloadTXT() {
    if (!currentData) return;
    const pad = (s, n) => (s.length >= n ? s.slice(0, n - 1) + " " : s + " ".repeat(n - s.length));
    let out = "WEEKLY TIMETABLE\n" + "=".repeat(70) + "\n\n";
    DAYS.forEach((day) => {
      out += day.toUpperCase() + "\n" + "-".repeat(70) + "\n";
      out += pad("Time", 13) + pad("Subject", 26) + pad("Faculty", 14) + "Room\n";
      (currentData[day] || []).forEach((l) => {
        out += pad(l.time, 13) + pad(l.subject, 26) + pad(l.faculty, 14) + l.room + "\n";
      });
      out += "\n";
    });
    const blob = new Blob([out], { type: "text/plain;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "timetable.txt";
    a.click();
    URL.revokeObjectURL(url);
  }

  regenBtn.addEventListener("click", fetchAndRender);
  txtBtn.addEventListener("click", downloadTXT);
  printBtn.addEventListener("click", () => window.print());

  fetchAndRender();
})();
