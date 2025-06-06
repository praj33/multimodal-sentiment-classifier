const API_URL = "http://127.0.0.1:8000"; // Change to your deployed URL when live

// DOM references
const modeSelect = document.getElementById("mode");
const textInput = document.getElementById("text-input");
const fileInput = document.getElementById("file-input");
const darkToggle = document.getElementById("darkToggle");
const toast = document.getElementById("toast");
const resultBox = document.getElementById("result");
const loader = document.getElementById("loader");
const bar = document.getElementById("bar");
const barFill = document.getElementById("bar-fill");
const confLabel = document.getElementById("conf-label");

// Handle mode change
modeSelect.addEventListener("change", () => {
  const mode = modeSelect.value;
  textInput.style.display = mode === "text" ? "block" : "none";
  fileInput.style.display = mode !== "text" ? "block" : "none";
});

// Dark mode toggle
darkToggle.addEventListener("click", () => {
  document.documentElement.classList.toggle("dark");
});

// Toast utility
function showToast(message, success = true) {
  toast.textContent = message;
  toast.className = `fixed top-4 right-4 px-4 py-2 rounded shadow transition text-white ${success ? "bg-green-600" : "bg-red-600"}`;
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 3000);
}

// Loader toggle
function setLoading(isLoading) {
  loader.style.display = isLoading ? "inline-block" : "none";
}

// Analyze sentiment function
async function analyze() {
  const mode = modeSelect.value;
  const text = document.getElementById("text").value.trim();
  const file = document.getElementById("file").files[0];

  // Reset UI
  setLoading(true);
  resultBox.innerHTML = "⏳ Analyzing...";
  bar.style.display = "none";
  barFill.style.width = "0%";
  confLabel.textContent = "";

  try {
    let response;

    if (mode === "text") {
      if (!text) {
        setLoading(false);
        showToast("⚠️ Please enter text", false);
        return;
      }

      response = await fetch(`${API_URL}/predict/text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      });
    } else {
      if (!file) {
        setLoading(false);
        showToast("⚠️ Please upload a file", false);
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      response = await fetch(`${API_URL}/predict/${mode}`, {
        method: "POST",
        body: formData
      });
    }

    const data = await response.json();
    setLoading(false);

    if (data.error) {
      resultBox.innerHTML = "<span class='text-red-500'>❌ " + data.error + "</span>";
      showToast("Analysis failed", false);
      return;
    }

    const sentiment = data.fused_sentiment || data.sentiment;
    const confidence = data.confidence || 0;

    const emoji = sentiment === "positive" ? "😊" :
                  sentiment === "negative" ? "😞" : "😐";

    const color = sentiment === "positive" ? "text-green-600" :
                  sentiment === "negative" ? "text-red-600" : "text-gray-600";

    resultBox.innerHTML =
      "<div class='text-xl font-bold " + color + "'>" +
        emoji + " " + sentiment.toUpperCase() +
      "</div>" +
      "<div class='text-sm'>Confidence: " + (confidence * 100).toFixed(2) + "%</div>";

    // Animate confidence bar
    bar.style.display = "block";
    setTimeout(() => {
      barFill.style.transition = "width 0.5s ease";
      barFill.style.width = (confidence * 100) + "%";
      confLabel.textContent = (confidence * 100).toFixed(1) + "%";
    }, 100);

    showToast("✅ Sentiment analyzed");

  } catch (err) {
    setLoading(false);
    resultBox.innerHTML = "<span class='text-red-500'>❌ " + err.message + "</span>";
    showToast("Unexpected error", false);
  }
}