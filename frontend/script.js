// ---------- Ambient network background ----------
(function initNetworkBackground() {
  const canvas = document.getElementById('netBg');
  const ctx = canvas.getContext('2d');
  let nodes = [];
  const NODE_COUNT = 50;
  const LINK_DIST = 130;
  const COLORS = ['47,217,242', '167,139,250']; // cyan, violet — alternate for vibrancy

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function makeNodes() {
    nodes = Array.from({ length: NODE_COUNT }, (_, i) => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
      color: COLORS[i % 2],
    }));
  }

  function step() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const n of nodes) {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < 0 || n.x > canvas.width) n.vx *= -1;
      if (n.y < 0 || n.y > canvas.height) n.vy *= -1;
    }

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < LINK_DIST) {
          ctx.strokeStyle = `rgba(${nodes[i].color}, ${0.12 * (1 - dist / LINK_DIST)})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }

    for (const n of nodes) {
      ctx.fillStyle = `rgba(${n.color}, 0.4)`;
      ctx.beginPath();
      ctx.arc(n.x, n.y, 1.6, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(step);
  }

  window.addEventListener('resize', () => { resize(); makeNodes(); });
  resize();
  makeNodes();
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    requestAnimationFrame(step);
  }
})();

// ---------- Threat-level badge ----------
function riskColor(score) {
  if (score >= 0.66) return '#FF4667'; // red — high
  if (score >= 0.33) return '#FDB833'; // amber — medium
  return '#2FD9F2'; // cyan — low
}

function renderThreatBadge(riskScore) {
  const badge = document.getElementById('threatBadge');
  const label = document.getElementById('threatLabel');
  const color = riskColor(riskScore);
  const text = riskScore >= 0.66 ? 'ELEVATED THREAT' : riskScore >= 0.33 ? 'MODERATE RISK' : 'NOMINAL';

  badge.style.color = color;
  badge.style.borderColor = color;
  badge.style.boxShadow = `0 0 14px ${color}33`;
  label.textContent = text;
}

// ---------- Live clock ----------
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent = now.toLocaleTimeString('en-GB');
}
setInterval(updateClock, 1000);
updateClock();

// ---------- Mock data per time range (replace with real /predict response later) ----------
// Member 4 ka backend jab ready ho, tab fetchForecast() ke andar fetch('http://localhost:5000/predict')
// laga dena aur RANGE_DATA ki jagah seedha API response use karna.
const RANGE_DATA = {
  '1h': {
    risk_score: 0.72,
    predicted_stage: "Lateral Movement",
    stage_probabilities: { 1: 0.10, 2: 0.18, 3: 0.52, 4: 0.15, 5: 0.05 },
    forecast_series: [0.12, 0.15, 0.22, 0.31, 0.40, 0.55, 0.61, 0.72, 0.68, 0.74],
    top_features: { flow_duration: 0.81, packet_rate: 0.64, dst_port_entropy: 0.47, byte_ratio: 0.33 },
    kpis: { threats: 7, packets: "12.4K", blocked: 138, confidence: "91%" }
  },
  '6h': {
    risk_score: 0.54,
    predicted_stage: "Initial Access",
    stage_probabilities: { 1: 0.22, 2: 0.41, 3: 0.20, 4: 0.11, 5: 0.06 },
    forecast_series: [0.30, 0.28, 0.35, 0.42, 0.38, 0.46, 0.50, 0.54, 0.49, 0.52],
    top_features: { packet_rate: 0.72, flow_duration: 0.58, byte_ratio: 0.41, dst_port_entropy: 0.29 },
    kpis: { threats: 19, packets: "9.8K", blocked: 402, confidence: "88%" }
  },
  '24h': {
    risk_score: 0.38,
    predicted_stage: "Reconnaissance",
    stage_probabilities: { 1: 0.48, 2: 0.24, 3: 0.15, 4: 0.08, 5: 0.05 },
    forecast_series: [0.20, 0.25, 0.31, 0.29, 0.34, 0.30, 0.36, 0.33, 0.38, 0.35],
    top_features: { dst_port_entropy: 0.63, flow_duration: 0.51, packet_rate: 0.40, byte_ratio: 0.22 },
    kpis: { threats: 41, packets: "7.1K", blocked: 1284, confidence: "84%" }
  },
  '7d': {
    risk_score: 0.61,
    predicted_stage: "Command & Control",
    stage_probabilities: { 1: 0.08, 2: 0.14, 3: 0.19, 4: 0.44, 5: 0.15 },
    forecast_series: [0.35, 0.40, 0.38, 0.45, 0.50, 0.55, 0.58, 0.61, 0.59, 0.63],
    top_features: { flow_duration: 0.69, dst_port_entropy: 0.55, byte_ratio: 0.48, packet_rate: 0.36 },
    kpis: { threats: 63, packets: "10.6K", blocked: 5710, confidence: "90%" }
  }
};

const MOCK_EVENT_POOL = [
  { severity: "high", msg: "Unusual outbound beacon pattern detected" },
  { severity: "high", msg: "Repeated auth failures from single host" },
  { severity: "med",  msg: "Port scan burst on subnet 192.168.1.0/24" },
  { severity: "med",  msg: "Unexpected DNS query volume spike" },
  { severity: "low",  msg: "New device joined network" },
  { severity: "low",  msg: "Routine outbound TLS session opened" },
  { severity: "med",  msg: "Large outbound transfer to unfamiliar host" },
  { severity: "high", msg: "Known C2 IP range contacted" }
];

const STAGE_ORDER = ["Reconnaissance", "Initial Access", "Lateral Movement", "Command & Control", "Exfiltration"];

let currentRange = '1h';
let feedEvents = [];

// ---------- Render: KPI strip ----------
function renderKpis(kpis) {
  document.getElementById('kpiThreats').textContent = kpis.threats;
  document.getElementById('kpiPackets').textContent = kpis.packets;
  document.getElementById('kpiBlocked').textContent = kpis.blocked.toLocaleString();
  document.getElementById('kpiConfidence').textContent = kpis.confidence;

  // Small mock deltas so the strip doesn't feel static
  setTrend('kpiThreatsTrend', -8, true);
  setTrend('kpiPacketsTrend', 4, false);
  setTrend('kpiBlockedTrend', 12, false);
  setTrend('kpiConfidenceTrend', 2, false);
}

function setTrend(id, pct, inverse) {
  const el = document.getElementById(id);
  const up = pct >= 0;
  const good = inverse ? !up : up;
  el.textContent = (up ? '▲ ' : '▼ ') + Math.abs(pct) + '%';
  el.classList.toggle('up', !good);
  el.classList.toggle('down', good);
}

// ---------- Render: stage pipeline (with kill-chain progress) ----------
function renderStages(stageProbabilities, predictedStageName) {
  const predictedIdx = STAGE_ORDER.indexOf(predictedStageName);

  document.querySelectorAll('.stage').forEach(li => {
    const stageNum = li.dataset.stage;
    const idx = Number(stageNum) - 1;
    const prob = stageProbabilities[stageNum] ?? 0;
    const probEl = li.querySelector('.stage-prob');
    probEl.textContent = (prob * 100).toFixed(0) + '%';

    li.classList.remove('active', 'passed');
    if (idx < predictedIdx) li.classList.add('passed');
    else if (idx === predictedIdx) li.classList.add('active');
  });
}

// ---------- Render: risk readout (animated gauge + count-up) ----------
const GAUGE_CIRCUMFERENCE = 377; // 2 * PI * r(60), matches stroke-dasharray in CSS

function renderRisk(riskScore, predictedStage) {
  document.getElementById('predictedStage').textContent = predictedStage;
  document.getElementById('lastUpdated').textContent = 'Updated just now';

  const fill = document.getElementById('gaugeFill');
  const valueEl = document.getElementById('riskScore');
  const color = riskColor(riskScore);
  fill.style.stroke = color;

  const targetOffset = GAUGE_CIRCUMFERENCE * (1 - riskScore);
  requestAnimationFrame(() => {
    fill.style.strokeDashoffset = targetOffset;
  });

  const duration = 1100;
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    valueEl.textContent = (riskScore * eased).toFixed(2);
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ---------- Render: explainability bars ----------
function renderFeatures(topFeatures) {
  const rows = document.querySelectorAll('#featureList .feature-row');
  const entries = Object.entries(topFeatures);
  rows.forEach((row, i) => {
    if (!entries[i]) return;
    const [name, value] = entries[i];
    row.querySelector('.feature-name').textContent = name;
    row.querySelector('.feature-val').textContent = (value * 100).toFixed(0) + '%';
    row.querySelector('.feature-fill').style.width = (value * 100).toFixed(0) + '%';
  });
}

// ---------- Render: alert feed (with search filter + severity counts) ----------
function renderFeed() {
  const feedList = document.getElementById('feedList');
  const query = document.getElementById('feedSearch').value.trim().toLowerCase();

  const visible = query
    ? feedEvents.filter(ev => ev.msg.toLowerCase().includes(query) || ev.severity.includes(query))
    : feedEvents;

  if (visible.length === 0) {
    feedList.innerHTML = `<p class="empty-state">No matching events.</p>`;
  } else {
    feedList.innerHTML = visible.map(ev => `
      <div class="feed-row sev-border-${ev.severity}">
        <span class="feed-time">${ev.time}</span>
        <span class="sev-${ev.severity}">[${ev.severity.toUpperCase()}]</span>
        <span class="feed-msg">${ev.msg}</span>
      </div>
    `).join('');
  }

  const counts = { high: 0, med: 0, low: 0 };
  feedEvents.forEach(ev => counts[ev.severity]++);
  document.getElementById('countHigh').textContent = counts.high;
  document.getElementById('countMed').textContent = counts.med;
  document.getElementById('countLow').textContent = counts.low;
}

document.getElementById('feedSearch').addEventListener('input', renderFeed);

// Simulate a live feed: push a new mock event periodically
function pushLiveEvent() {
  const pick = MOCK_EVENT_POOL[Math.floor(Math.random() * MOCK_EVENT_POOL.length)];
  const time = new Date().toLocaleTimeString('en-GB');
  feedEvents.unshift({ time, severity: pick.severity, msg: pick.msg });
  feedEvents = feedEvents.slice(0, 8); // cap the feed
  renderFeed();
}

// ---------- Chart.js forecast chart ----------
let forecastChart;
function renderChart(seriesData, riskScore) {
  const ctx = document.getElementById('forecastChart').getContext('2d');
  const labels = seriesData.map((_, i) => `t+${i}`);
  const color = riskColor(riskScore ?? seriesData[seriesData.length - 1]);
  const fillColor = color + '22';

  if (forecastChart) {
    forecastChart.data.labels = labels;
    forecastChart.data.datasets[0].data = seriesData;
    forecastChart.data.datasets[0].borderColor = color;
    forecastChart.data.datasets[0].backgroundColor = fillColor;
    forecastChart.update();
    return;
  }

  forecastChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Attack Probability',
        data: seriesData,
        borderColor: color,
        backgroundColor: fillColor,
        tension: 0.35,
        fill: true,
        pointRadius: 2,
        pointBackgroundColor: color
      }]
    },
    options: {
      responsive: true,
      animation: { duration: 500 },
      scales: {
        y: { min: 0, max: 1, ticks: { color: '#8592AA' }, grid: { color: '#1A2438' } },
        x: { ticks: { color: '#8592AA' }, grid: { display: false } }
      },
      plugins: { legend: { labels: { color: '#E7ECF6', font: { family: 'IBM Plex Mono', size: 11 } } } }
    }
  });
}

// ---------- Time-range chip switching ----------
document.getElementById('rangeChips').addEventListener('click', (e) => {
  const btn = e.target.closest('.chip');
  if (!btn) return;
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
  currentRange = btn.dataset.range;
  applyRange(currentRange);
});

function applyRange(range) {
  const data = RANGE_DATA[range];
  renderStages(data.stage_probabilities, data.predicted_stage);
  renderRisk(data.risk_score, data.predicted_stage);
  renderThreatBadge(data.risk_score);
  renderFeatures(data.top_features);
  renderChart(data.forecast_series, data.risk_score);
  renderKpis(data.kpis);
}

// ---------- Export snapshot ----------
document.getElementById('exportBtn').addEventListener('click', () => {
  const data = RANGE_DATA[currentRange];
  const snapshot = {
    exported_at: new Date().toISOString(),
    range: currentRange,
    ...data,
    recent_events: feedEvents
  };
  const blob = new Blob([JSON.stringify(snapshot, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `attack-forecast-snapshot-${currentRange}-${Date.now()}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

// ---------- Main: fetch prediction and render everything ----------
// Abhi mock data use ho raha hai. Jab backend ka /predict endpoint ready ho jaye,
// applyRange() ke andar fetch('http://localhost:5000/predict') se real data laga dena.
async function applyRealData(data) {
  renderStages(data.stage_probabilities, data.predicted_stage);
  renderRisk(data.risk_score, data.predicted_stage);
  renderThreatBadge(data.risk_score);
  renderFeatures(data.top_features);
  renderChart(data.forecast_series, data.risk_score);
  renderKpis(data.kpis);
}

async function fetchForecast() {
  try {
    const res = await fetch('http://localhost:5000/predict', { method: 'POST' });
    const data = await res.json();
    applyRealData(data);
  } catch (err) {
    console.error('Backend se connect nahi ho paaya, mock data dikha rahe hain:', err);
    applyRange(currentRange);
  }

  // Seed the feed with a couple of starting events
  pushLiveEvent();
  pushLiveEvent();
  pushLiveEvent();
  setInterval(pushLiveEvent, 6000);

  // Har 5 second mein naya real prediction fetch karo (live feel ke liye)
  setInterval(async () => {
    try {
      const res = await fetch('http://localhost:5000/predict', { method: 'POST' });
      const data = await res.json();
      applyRealData(data);
    } catch (err) {
      console.error('Live update fetch failed:', err);
    }
  }, 5000);
}

fetchForecast();
