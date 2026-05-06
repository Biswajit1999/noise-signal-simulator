const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const noiseSlider = document.getElementById("noiseLevel");
const smoothSlider = document.getElementById("smoothWindow");
const freqSlider = document.getElementById("frequency");

const noiseValue = document.getElementById("noiseValue");
const smoothValue = document.getElementById("smoothValue");
const freqValue = document.getElementById("freqValue");

const snrValue = document.getElementById("snrValue");
const noiseRegime = document.getElementById("noiseRegime");

const N = 600;

function seededNoise(i) {
  const x = Math.sin(i * 12.9898 + 78.233) * 43758.5453;
  return (x - Math.floor(x)) * 2 - 1;
}

function trueSignal(x, frequency) {
  return Math.sin(2 * Math.PI * frequency * x) * Math.exp(-0.18 * x);
}

function movingAverage(values, windowSize) {
  const half = Math.floor(windowSize / 2);
  const smoothed = [];

  for (let i = 0; i < values.length; i++) {
    let sum = 0;
    let count = 0;

    for (let j = i - half; j <= i + half; j++) {
      if (j >= 0 && j < values.length) {
        sum += values[j];
        count++;
      }
    }

    smoothed.push(sum / count);
  }

  return smoothed;
}

function std(values) {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance = values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length;
  return Math.sqrt(variance);
}

function mapX(i) {
  return 70 + (i / (N - 1)) * 910;
}

function mapY(value) {
  return 315 - value * 115;
}

function drawBackground() {
  ctx.fillStyle = "#020617";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < 140; i++) {
    ctx.fillStyle = `rgba(255,255,255,${Math.random() * 0.45})`;
    ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 1, 1);
  }
}

function drawAxes() {
  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 2;

  ctx.beginPath();
  ctx.moveTo(70, 500);
  ctx.lineTo(980, 500);
  ctx.moveTo(70, 95);
  ctx.lineTo(70, 500);
  ctx.stroke();

  ctx.fillStyle = "#cbd5e1";
  ctx.font = "15px Arial";
  ctx.fillText("Time / sample index", 450, 555);

  ctx.save();
  ctx.translate(28, 340);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText("Signal amplitude", 0, 0);
  ctx.restore();

  ctx.strokeStyle = "rgba(148,163,184,0.18)";
  ctx.lineWidth = 1;

  for (let y = 140; y <= 500; y += 60) {
    ctx.beginPath();
    ctx.moveTo(70, y);
    ctx.lineTo(980, y);
    ctx.stroke();
  }

  for (let x = 70; x <= 980; x += 130) {
    ctx.beginPath();
    ctx.moveTo(x, 95);
    ctx.lineTo(x, 500);
    ctx.stroke();
  }
}

function drawLine(values, colour, width, alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = colour;
  ctx.lineWidth = width;
  ctx.beginPath();

  values.forEach((v, i) => {
    const x = mapX(i);
    const y = mapY(v);

    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });

  ctx.stroke();
  ctx.restore();
}

function drawLegend() {
  const x = 735;
  const y = 115;

  ctx.fillStyle = "rgba(2,6,23,0.78)";
  ctx.strokeStyle = "rgba(148,163,184,0.35)";
  ctx.lineWidth = 1;

  ctx.beginPath();
  ctx.roundRect(x - 18, y - 35, 225, 120, 14);
  ctx.fill();
  ctx.stroke();

  const items = [
    { label: "True signal", colour: "#22c55e" },
    { label: "Noisy observation", colour: "#94a3b8" },
    { label: "Smoothed recovery", colour: "#38bdf8" }
  ];

  ctx.font = "14px Arial";

  items.forEach((item, i) => {
    const yy = y + i * 30;

    ctx.strokeStyle = item.colour;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(x, yy);
    ctx.lineTo(x + 36, yy);
    ctx.stroke();

    ctx.fillStyle = "#e2e8f0";
    ctx.fillText(item.label, x + 48, yy + 5);
  });
}

function update() {
  const noiseLevel = Number(noiseSlider.value);
  const smoothWindow = Number(smoothSlider.value);
  const frequency = Number(freqSlider.value);

  noiseValue.textContent = noiseLevel.toFixed(2);
  smoothValue.textContent = smoothWindow;
  freqValue.textContent = frequency.toFixed(2);

  const signal = [];
  const noise = [];
  const noisy = [];

  for (let i = 0; i < N; i++) {
    const x = (i / (N - 1)) * 10;
    const s = trueSignal(x, frequency);
    const n = seededNoise(i) * noiseLevel;

    signal.push(s);
    noise.push(n);
    noisy.push(s + n);
  }

  const smoothed = movingAverage(noisy, smoothWindow);

  const snr = std(signal) / Math.max(std(noise), 1e-9);

  snrValue.textContent = snr.toFixed(2);

  if (snr > 3) {
    noiseRegime.textContent = "Clear detection";
  } else if (snr > 1.2) {
    noiseRegime.textContent = "Moderate noise";
  } else {
    noiseRegime.textContent = "Noise dominated";
  }

  drawBackground();
  drawAxes();

  drawLine(noisy, "#94a3b8", 1.5, 0.55);
  drawLine(signal, "#22c55e", 3, 0.95);
  drawLine(smoothed, "#38bdf8", 4, 0.95);

  drawLegend();

  ctx.fillStyle = "#e2e8f0";
  ctx.font = "17px Arial";
  ctx.fillText("Weak signal recovery from noisy observation", 70, 55);
}

document.querySelectorAll("button[data-mode]").forEach(button => {
  button.addEventListener("click", () => {
    const mode = button.dataset.mode;

    if (mode === "low") noiseSlider.value = 0.12;
    if (mode === "medium") noiseSlider.value = 0.35;
    if (mode === "high") noiseSlider.value = 0.80;

    update();
  });
});

noiseSlider.addEventListener("input", update);
smoothSlider.addEventListener("input", update);
freqSlider.addEventListener("input", update);

update();
