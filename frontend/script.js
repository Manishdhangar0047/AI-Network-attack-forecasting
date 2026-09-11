// Ye file backend se baat karta hai aur result dikhata hai

const BACKEND_URL = "http://localhost:5000/predict";

async function uploadFile() {
  const fileInput = document.getElementById("fileInput");

  if (fileInput.files.length === 0) {
    alert("Pehle koi file select karo!");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Backend se error aaya");
    }

    const data = await response.json();
    showResult(data);

  } catch (error) {
    alert("Error: " + error.message + "\n(Check karo backend chal raha hai ya nahi - python app.py)");
  }
}

function showResult(data) {
  document.getElementById("result").style.display = "block";
  document.getElementById("filename").innerText = data.filename;
  document.getElementById("stage").innerText = data.predicted_stage;
  document.getElementById("features").innerText = data.top_features.join(", ");

  // Simple canvas graph - Member 5 baad mein Chart.js se aur behtar bana sakta hai
  const canvas = document.getElementById("probChart");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const probs = data.infiltration_probability;
  const stepWidth = canvas.width / probs.length;

  ctx.beginPath();
  ctx.moveTo(0, canvas.height - probs[0] * canvas.height);
  probs.forEach((p, i) => {
    ctx.lineTo(i * stepWidth, canvas.height - p * canvas.height);
  });
  ctx.strokeStyle = "#d85a30";
  ctx.lineWidth = 2;
  ctx.stroke();
}
