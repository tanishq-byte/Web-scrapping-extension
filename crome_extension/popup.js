document.addEventListener("DOMContentLoaded", () => {
    const urlInput = document.getElementById("urlInput");
    const scrapeBtn = document.getElementById("scrapeBtn");
    const reportBtn = document.getElementById("reportBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const output = document.getElementById("output");
  
    // Initial state
    reportBtn.disabled = true;
    downloadBtn.disabled = true;
  
    // ==============================
    // SCRAPE WEBSITE
    // ==============================
    scrapeBtn.addEventListener("click", async () => {
      const url = urlInput.value.trim();
  
      if (!url) {
        output.textContent = "❌ Please enter a URL.";
        return;
      }
  
      output.textContent = "⏳ Scraping website (BeautifulSoup raw HTML)...";
      reportBtn.disabled = true;
      downloadBtn.disabled = true;
  
      try {
        const response = await fetch("http://localhost:8000/scrape", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ url })
        });
  
        const result = await response.json();
  
        if (result.status === "success") {
          output.textContent = result.raw_output;
          reportBtn.disabled = false;
        } else {
          output.textContent = "❌ Error: " + result.message;
        }
  
      } catch (err) {
        output.textContent =
          "❌ Backend not reachable. Make sure app.py is running.";
      }
    });
  
    // ==============================
    // GENERATE REPORT
    // ==============================
    reportBtn.addEventListener("click", async () => {
      output.textContent = "📊 Generating market report...";
  
      try {
        const response = await fetch("http://localhost:8000/report");
        const result = await response.json();
  
        if (result.status === "success") {
            output.textContent = result.report;
            downloadBtn.disabled = false;
          
            // Show graph image
            const graphImg = document.getElementById("graphImg");
            graphImg.src = "http://localhost:8000/graph?ts=" + new Date().getTime();
            graphImg.style.display = "block";
          }
          else {
          output.textContent = "❌ Error: " + result.message;
        }
  
      } catch (err) {
        output.textContent =
          "❌ Failed to generate report. Backend error.";
      }
    });
  
    // ==============================
    // DOWNLOAD REPORT + GRAPH
    // ==============================
    downloadBtn.addEventListener("click", () => {
      window.open("http://localhost:8000/download", "_blank");
    });
  });
  