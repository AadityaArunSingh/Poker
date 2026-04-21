import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import date, datetime
import calendar

st.set_page_config(
    page_title="🎰 Free Buy-in Wheel",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Local imports ──────────────────────────────────────────────────────────────
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import CSS
from data import load_data

st.markdown(CSS, unsafe_allow_html=True)

# ── Back button ────────────────────────────────────────────────────────────────
if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="suit-row">♠ ♥ ♦ ♣</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🎰 FREE BUY-IN WHEEL</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Spin to win · ₹200 on the house</div>', unsafe_allow_html=True)
st.markdown('<hr class="red-divider">', unsafe_allow_html=True)

# ── Get eligible players (>5 sessions this month) ──────────────────────────────
df = load_data()
today = date.today()
month_start = date(today.year, today.month, 1)

df_month = df[
    (df["Date"].dt.date >= month_start) &
    (df["Date"].dt.date <= today)
]
sessions_this_month = df_month.groupby("Name")["Date"].nunique()
eligible = sorted(sessions_this_month[sessions_this_month > 5].index.tolist())

if len(eligible) < 2:
    st.markdown("""
    <div style="text-align:center;padding:3rem;font-family:'DM Mono',monospace;color:#666;">
        <div style="font-size:3rem">🃏</div>
        <div style="font-size:1rem;letter-spacing:0.1em;text-transform:uppercase;margin-top:1rem">
            Not enough eligible players yet this month
        </div>
        <div style="font-size:0.75rem;color:#444;margin-top:0.5rem">
            Players need more than 5 sessions to appear on the wheel
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Countdown target: last day of month at 17:30 IST (12:00 UTC) ──────────────
last_day = calendar.monthrange(today.year, today.month)[1]
target   = datetime(today.year, today.month, last_day, 12, 0, 0)  # 17:30 IST = 12:00 UTC
target_ms = int(target.timestamp() * 1000)

# ── Build wheel ────────────────────────────────────────────────────────────────
players_js = str(eligible)

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: transparent;
    font-family: 'DM Mono', monospace;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    padding: 2rem 1rem;
  }}

  /* ── Countdown ── */
  #countdown-wrap {{
    text-align: center;
  }}
  #countdown-label {{
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 0.4rem;
  }}
  #countdown {{
    font-size: 2rem;
    color: #cc0000;
    letter-spacing: 0.1em;
  }}
  #countdown.done {{
    color: #2ecc71;
    font-size: 1.4rem;
  }}

  /* ── Wheel container ── */
  #wheel-wrap {{
    position: relative;
    width: 420px;
    height: 420px;
  }}
  canvas {{
    border-radius: 50%;
    box-shadow: 0 0 40px rgba(204,0,0,0.4);
  }}
  /* pointer arrow */
  #pointer {{
    position: absolute;
    top: 50%;
    right: -24px;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-top: 16px solid transparent;
    border-bottom: 16px solid transparent;
    border-right: 32px solid #cc0000;
    filter: drop-shadow(0 0 6px rgba(204,0,0,0.8));
  }}

  /* ── Spin button ── */
  #spin-btn {{
    background: linear-gradient(135deg, #8b0000, #cc0000);
    color: white;
    border: none;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 1rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.8rem 3rem;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(204,0,0,0.4);
    transition: opacity 0.2s, transform 0.1s;
  }}
  #spin-btn:hover {{ opacity: 0.85; }}
  #spin-btn:active {{ transform: scale(0.97); }}
  #spin-btn:disabled {{ opacity: 0.4; cursor: not-allowed; }}

  /* ── Winner banner ── */
  #winner {{
    display: none;
    text-align: center;
    animation: fadeIn 0.5s ease;
  }}
  #winner-label {{
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #666;
  }}
  #winner-name {{
    font-size: 2.8rem;
    color: #cc0000;
    font-weight: bold;
    margin: 0.3rem 0;
    text-shadow: 0 0 30px rgba(204,0,0,0.6);
  }}
  #winner-sub {{
    font-size: 0.8rem;
    color: #888;
    letter-spacing: 0.1em;
  }}
  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
</style>
</head>
<body>

<!-- Countdown -->
<div id="countdown-wrap">
  <div id="countdown-label">🎰 Next spin in</div>
  <div id="countdown">--:--:--</div>
</div>

<!-- Wheel -->
<div id="wheel-wrap">
  <canvas id="wheel" width="420" height="420"></canvas>
  <div id="pointer"></div>
</div>

<!-- Spin button -->
<button id="spin-btn" onclick="spin()">SPIN THE WHEEL</button>

<!-- Winner -->
<div id="winner">
  <div id="winner-label">🎉 Free buy-in goes to</div>
  <div id="winner-name"></div>
  <div id="winner-sub">₹200 on the house — don't waste it 🃏</div>
</div>

<script>
const players = {players_js};
const numSegments = players.length;
const arc = (2 * Math.PI) / numSegments;

const COLOURS = [
  "#1a0000","#2a0000","#3a0000","#4a0000",
  "#5a0000","#6a0000","#7a0000","#8a0000",
  "#cc0000","#1a0505",
];

const canvas  = document.getElementById("wheel");
const ctx     = canvas.getContext("2d");
const cx      = canvas.width  / 2;
const cy      = canvas.height / 2;
const radius  = cx - 10;

let currentAngle = 0;
let spinning     = false;

function drawWheel(angle) {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < numSegments; i++) {{
    const start = angle + i * arc;
    const end   = start + arc;

    // Segment
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, radius, start, end);
    ctx.closePath();
    ctx.fillStyle = COLOURS[i % COLOURS.length];
    ctx.fill();
    ctx.strokeStyle = "#cc0000";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Label
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(start + arc / 2);
    ctx.textAlign = "right";
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 13px 'DM Mono', monospace";
    ctx.fillText(players[i], radius - 12, 5);
    ctx.restore();
  }}

  // Centre circle
  ctx.beginPath();
  ctx.arc(cx, cy, 24, 0, 2 * Math.PI);
  ctx.fillStyle = "#0a0a0a";
  ctx.fill();
  ctx.strokeStyle = "#cc0000";
  ctx.lineWidth = 3;
  ctx.stroke();

  // Centre suit
  ctx.fillStyle = "#cc0000";
  ctx.font = "18px serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("♠", cx, cy);
}}

function spin() {{
  if (spinning) return;
  spinning = true;
  document.getElementById("spin-btn").disabled = true;
  document.getElementById("winner").style.display = "none";

  // Random winner index
  const winnerIdx  = Math.floor(Math.random() * numSegments);
  // Total rotation: several full spins + land on winner
  const totalSpins = 6 + Math.random() * 4;
  const targetAngle = (2 * Math.PI * totalSpins)
    - (winnerIdx * arc)
    - (arc / 2)
    - currentAngle;

  const duration  = 5000;
  const startTime = performance.now();
  const startAngle = currentAngle;

  function easeOut(t) {{
    return 1 - Math.pow(1 - t, 4);
  }}

  function animate(now) {{
    const elapsed  = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    currentAngle   = startAngle + targetAngle * easeOut(progress);
    drawWheel(currentAngle);

    if (progress < 1) {{
      requestAnimationFrame(animate);
    }} else {{
      spinning = false;
      document.getElementById("spin-btn").disabled = false;
      document.getElementById("winner-name").textContent = players[winnerIdx];
      document.getElementById("winner").style.display = "block";
    }}
  }}
  requestAnimationFrame(animate);
}}

// Initial draw
drawWheel(currentAngle);

// ── Countdown ──────────────────────────────────────────────────────────────────
const targetMs = {target_ms};
const countdownEl = document.getElementById("countdown");

function updateCountdown() {{
  const now  = Date.now();
  const diff = targetMs - now;
  if (diff <= 0) {{
    countdownEl.textContent = "🎰 Time to Spin!";
    countdownEl.classList.add("done");
    return;
  }}
  const h = Math.floor(diff / 3600000);
  const m = Math.floor((diff % 3600000) / 60000);
  const s = Math.floor((diff % 60000) / 1000);
  const pad = n => String(n).padStart(2, "0");
  const days = Math.floor(diff / 86400000);
  if (days > 0) {{
    countdownEl.textContent = days + "d " + pad(h % 24) + "h " + pad(m) + "m " + pad(s) + "s";
  }} else {{
    countdownEl.textContent = pad(h) + ":" + pad(m) + ":" + pad(s);
  }}
}}
updateCountdown();
setInterval(updateCountdown, 1000);
</script>
</body>
</html>
""", height=780)
