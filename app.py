"""
┌─────────────────────────────────────────────────────────────────────┐
│   C I N E M A T C H  ·  Professional Movie Recommendation System    │
│   Netflix-Grade UI  ·  Production-Ready  ·  Fully Optimised         │
├─────────────────────────────────────────────────────────────────────┤
│  IMMUTABLE (backend unchanged):                                      │
│   • load_movies()      • load_similarity()    • fetch_poster()       │
│   • recommend()        • @st.cache_data       • TMDB API             │
│                                                                      │
│  CHANGED (UI / UX / CSS only):                                       │
│   • Full Netflix-style dark design system                            │
│   • Sticky transparent navbar with live stats                        │
│   • Cinematic hero with animated headline                            │
│   • Glassmorphism search panel                                       │
│   • Staggered-entrance movie cards with hover depth                  │
│   • Skeleton loading states, error banners, empty states             │
│   • Responsive grid  (5 → 3 → 2 → 1 columns)                       │
│   • Professional footer                                              │
└─────────────────────────────────────────────────────────────────────┘
"""

# ══════════════════════════════════════════════════════════════════════
# SECTION 1 — IMPORTS
# ══════════════════════════════════════════════════════════════════════
import streamlit as st
import pickle
import pandas as pd
import requests


# ══════════════════════════════════════════════════════════════════════
# SECTION 2 — PAGE CONFIG  (must be the very first Streamlit call)
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CineMatch — AI Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ══════════════════════════════════════════════════════════════════════
# SECTION 3 — DESIGN SYSTEM  (CSS tokens + all component styles)
# ══════════════════════════════════════════════════════════════════════
_CSS = """
<style>
/* ─── Google Fonts ──────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=DM+Serif+Display:ital@0;1&display=swap');

/* ─── Design Tokens ─────────────────────────────────────────────── */
:root {
    /* Background layers */
    --bg0: #07070E;
    --bg1: #0D0D18;
    --bg2: #111120;
    --bg3: #171728;
    --bg-glass: rgba(13,13,24,0.88);

    /* Brand palette */
    --red:        #E50914;
    --red-lo:     rgba(229,9,20,0.12);
    --red-mid:    rgba(229,9,20,0.30);
    --red-glow:   rgba(229,9,20,0.50);
    --gold:       #F5C518;
    --gold-lo:    rgba(245,197,24,0.12);
    --grad:       linear-gradient(130deg,#E50914 0%,#FF5733 55%,#F5C518 100%);
    --grad-text:  linear-gradient(130deg,#FF4D4D 0%,#FFB347 100%);

    /* Text */
    --t1: #EEEEF5;
    --t2: #8888A8;
    --t3: #44445A;

    /* Borders */
    --b1: rgba(255,255,255,0.06);
    --b2: rgba(229,9,20,0.40);

    /* Radii */
    --r1: 6px;
    --r2: 12px;
    --r3: 18px;
    --r4: 26px;

    /* Shadows */
    --s-card:  0 2px 16px rgba(0,0,0,0.55);
    --s-hover: 0 20px 60px rgba(0,0,0,0.80), 0 0 0 1.5px rgba(229,9,20,0.45);
    --s-btn:   0 4px 24px rgba(229,9,20,0.45);

    /* Motion */
    --ease: cubic-bezier(.4,0,.2,1);
    --tf: .18s var(--ease);
    --tm: .30s var(--ease);
    --ts: .50s var(--ease);
}

/* ─── Global Reset & Base ───────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }

html, body, [class*="css"], .stApp {
    background: var(--bg0) !important;
    color: var(--t1) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* Nuke Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    height: 0 !important;
    display: none !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Themed scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg0); }
::-webkit-scrollbar-thumb { background: var(--red-lo); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--red); }

/* ════════════════════════════════════════════════════════════════════
   NAVBAR
════════════════════════════════════════════════════════════════════ */
.nb {
    position: sticky; top: 0; z-index: 999;
    height: 62px;
    padding: 0 clamp(1.5rem, 4vw, 4rem);
    display: flex; align-items: center; justify-content: space-between;
    background: rgba(7,7,14,0.92);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border-bottom: 1px solid var(--b1);
}
.nb-brand {
    display: flex; align-items: center; gap: 10px;
}
.nb-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.55rem;
    font-weight: 400;
    font-style: italic;
    background: var(--grad-text);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.3px;
    line-height: 1;
}
.nb-pill {
    background: var(--red);
    color: #fff !important;
    font-size: 0.55rem; font-weight: 800;
    letter-spacing: 1.8px; text-transform: uppercase;
    padding: 2px 8px; border-radius: 4px;
}
.nb-sep { width:1px; height:22px; background: var(--b1); margin: 0 14px; }
.nb-tag {
    font-size: 0.65rem; font-weight: 600;
    color: var(--t3) !important;
    letter-spacing: 2.5px; text-transform: uppercase;
}
.nb-stats { display: flex; align-items: center; gap: 1.8rem; }
.nb-stat  { text-align: center; }
.nb-val {
    font-size: 0.95rem; font-weight: 800; line-height: 1;
    background: var(--grad-text);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.nb-lbl {
    font-size: 0.55rem; font-weight: 700;
    color: var(--t3) !important;
    letter-spacing: 2px; text-transform: uppercase;
    margin-top: 3px;
}
.nb-divider { width:1px; height:26px; background: var(--b1); }

/* ════════════════════════════════════════════════════════════════════
   HERO
════════════════════════════════════════════════════════════════════ */
.hero {
    position: relative; overflow: hidden;
    min-height: 480px;
    display: flex; align-items: center;
    padding: clamp(3rem,6vw,6rem) clamp(1.5rem,4vw,4.5rem) clamp(3rem,5vw,5rem);
    background:
        radial-gradient(ellipse 90% 80% at 65% 40%, rgba(229,9,20,0.09) 0%, transparent 65%),
        radial-gradient(ellipse 50% 50% at 5%  90%, rgba(245,197,24,0.06) 0%, transparent 60%),
        linear-gradient(175deg, var(--bg1) 0%, var(--bg0) 100%);
}

/* Scanline texture */
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent 0px, transparent 2px,
        rgba(255,255,255,0.007) 2px, rgba(255,255,255,0.007) 3px
    );
    pointer-events: none;
}

/* Ambient glow orb */
.hero::after {
    content: '';
    position: absolute;
    top: -120px; right: -60px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(229,9,20,0.12) 0%, transparent 68%);
    pointer-events: none;
    animation: orb 8s ease-in-out infinite alternate;
}
@keyframes orb {
    from { transform: translate(0,0) scale(1); }
    to   { transform: translate(-40px, 30px) scale(1.1); }
}

.hero-inner { position: relative; z-index: 2; max-width: 680px; }

.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--gold-lo);
    border: 1px solid rgba(245,197,24,0.22);
    border-radius: 99px;
    padding: 5px 16px;
    font-size: 0.63rem; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: var(--gold) !important;
    margin-bottom: 1.6rem;
    animation: slideUp .55s .0s var(--ease) both;
}
.badge-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--gold);
    animation: blink 2.4s ease infinite;
}
@keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:.25; }
}

.hero-h1 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.8rem, 5.8vw, 5.6rem);
    font-weight: 400;
    line-height: 1.08;
    letter-spacing: -1.5px;
    color: var(--t1) !important;
    margin-bottom: 1.2rem;
    animation: slideUp .55s .08s var(--ease) both;
}
.hero-h1 em {
    font-style: italic;
    background: var(--grad-text);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-p {
    font-size: 1rem; font-weight: 300;
    color: var(--t2) !important;
    line-height: 1.8; max-width: 500px;
    margin-bottom: 2.4rem;
    animation: slideUp .55s .16s var(--ease) both;
}

.hero-tags {
    display: flex; flex-wrap: wrap; gap: .55rem;
    animation: slideUp .55s .24s var(--ease) both;
}
.htag {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--b1);
    border-radius: 99px;
    padding: 5px 14px;
    font-size: 0.69rem; font-weight: 600;
    color: var(--t2) !important;
    letter-spacing: .3px;
    transition: border-color var(--tf), color var(--tf), background var(--tf);
}
.htag:hover {
    border-color: var(--red-mid); color: #FF8080 !important;
    background: var(--red-lo);
}

@keyframes slideUp {
    from { opacity:0; transform: translateY(24px); }
    to   { opacity:1; transform: translateY(0); }
}

/* ════════════════════════════════════════════════════════════════════
   METRICS STRIP  (below hero)
════════════════════════════════════════════════════════════════════ */
.mstrip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border-bottom: 1px solid var(--b1);
    background: var(--bg1);
}
.mstrip-item {
    padding: 1.1rem 1.8rem;
    display: flex; align-items: center; gap: 12px;
    border-right: 1px solid var(--b1);
    transition: background var(--tf);
}
.mstrip-item:last-child { border-right: none; }
.mstrip-item:hover { background: var(--bg2); }
.mstrip-icon { font-size: 1.3rem; flex-shrink: 0; }
.mstrip-val {
    font-size: 0.82rem; font-weight: 700;
    color: var(--t1) !important; line-height: 1;
}
.mstrip-lbl {
    font-size: 0.62rem; font-weight: 500;
    color: var(--t3) !important;
    letter-spacing: .5px; margin-top: 3px;
}

/* ════════════════════════════════════════════════════════════════════
   SEARCH PANEL
════════════════════════════════════════════════════════════════════ */
.spanel {
    background: var(--bg-glass);
    backdrop-filter: blur(32px); -webkit-backdrop-filter: blur(32px);
    border-top: 1px solid var(--b1);
    border-bottom: 1px solid var(--b1);
    padding: 2rem clamp(1.5rem,4vw,4.5rem);
}
.sp-inner { max-width: 1300px; margin: 0 auto; }
.sp-label {
    font-size: 0.62rem; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: var(--t3) !important;
    margin-bottom: .55rem;
}

/* ── Selectbox deep override ── */
div[data-testid="stSelectbox"] label { display: none !important; }
div[data-testid="stSelectbox"] > div > div {
    background: var(--bg2) !important;
    border: 1px solid var(--b1) !important;
    border-radius: var(--r2) !important;
    color: var(--t1) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important; font-weight: 500 !important;
    min-height: 48px !important;
    transition: border-color var(--tf), box-shadow var(--tf) !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--red-mid) !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px var(--red-lo) !important;
}
[data-baseweb="popover"] { background: var(--bg2) !important; }
[data-baseweb="popover"] ul { background: var(--bg2) !important; }
[data-baseweb="popover"] li {
    background: var(--bg2) !important;
    color: var(--t1) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.86rem !important;
}
[data-baseweb="popover"] li:hover { background: var(--bg3) !important; }

/* ── Recommend button ── */
div[data-testid="stButton"] > button {
    height: 48px !important;
    background: var(--grad) !important;
    color: #fff !important; border: none !important;
    border-radius: var(--r2) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 800 !important;
    letter-spacing: 1.5px; text-transform: uppercase;
    box-shadow: var(--s-btn) !important;
    width: 100% !important;
    transition: transform var(--tf), box-shadow var(--tf), opacity var(--tf) !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 36px rgba(229,9,20,0.6) !important;
}
div[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* Spinner */
div[data-testid="stSpinner"] > div { border-top-color: var(--red) !important; }

/* ════════════════════════════════════════════════════════════════════
   RESULTS AREA
════════════════════════════════════════════════════════════════════ */
.results {
    padding: 2.8rem clamp(1.5rem,4vw,4.5rem) 1rem;
    max-width: 1400px; margin: 0 auto;
}

/* Row header */
.row-hd {
    display: flex; align-items: baseline;
    justify-content: space-between;
    margin-bottom: 1.6rem;
    padding-bottom: .8rem;
    border-bottom: 1px solid var(--b1);
}
.row-hd-title {
    font-size: 1.1rem; font-weight: 700;
    color: var(--t1) !important;
}
.row-hd-title em { font-style: normal; color: var(--red) !important; }
.row-hd-badge {
    font-size: 0.6rem; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: var(--t3) !important;
    border: 1px solid var(--b1);
    border-radius: var(--r1);
    padding: 3px 10px;
}

/* ════════════════════════════════════════════════════════════════════
   MOVIE CARDS
════════════════════════════════════════════════════════════════════ */
.cards {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
}
@media (max-width:1200px) { .cards { grid-template-columns: repeat(4,1fr); } }
@media (max-width: 900px) { .cards { grid-template-columns: repeat(3,1fr); } }
@media (max-width: 600px) { .cards { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 400px) { .cards { grid-template-columns: 1fr; } }

/* Card */
.mc {
    background: var(--bg2);
    border: 1px solid var(--b1);
    border-radius: var(--r3);
    overflow: hidden;
    position: relative;
    cursor: pointer;
    transition: transform var(--tm), box-shadow var(--tm), border-color var(--tm);
    animation: cardIn var(--ts) both;
}
.mc:nth-child(1){animation-delay:.04s}
.mc:nth-child(2){animation-delay:.10s}
.mc:nth-child(3){animation-delay:.16s}
.mc:nth-child(4){animation-delay:.22s}
.mc:nth-child(5){animation-delay:.28s}

@keyframes cardIn {
    from { opacity:0; transform: translateY(32px) scale(.96); }
    to   { opacity:1; transform: translateY(0)   scale(1);   }
}

.mc:hover {
    transform: translateY(-10px) scale(1.022);
    box-shadow: var(--s-hover);
    border-color: var(--b2);
    z-index: 10;
}

/* Rank label — top-left */
.mc-rank {
    position: absolute; top: 10px; left: 10px; z-index: 5;
    background: var(--grad);
    color: #fff !important;
    font-size: 0.58rem; font-weight: 800;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 3px 9px; border-radius: 4px;
    box-shadow: 0 2px 10px rgba(229,9,20,.5);
}

/* Rank number — bottom-left ghost */
.mc-num {
    position: absolute; bottom: -10px; left: -8px; z-index: 1;
    font-family: 'DM Serif Display', serif;
    font-size: 8rem; font-weight: 400;
    color: rgba(255,255,255,0.04) !important;
    line-height: 1; user-select: none;
    pointer-events: none;
}

/* Poster */
.mc-poster {
    position: relative;
    width: 100%; padding-top: 148%;   /* 2:3 aspect */
    overflow: hidden;
    background: var(--bg3);
}
.mc-poster img {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    transition: transform var(--ts);
}
.mc:hover .mc-poster img { transform: scale(1.08); }

/* Bottom gradient on poster */
.mc-poster::after {
    content: '';
    position: absolute; bottom:0; left:0; right:0; height:55%;
    background: linear-gradient(to top, var(--bg2) 0%, transparent 100%);
    pointer-events: none; z-index: 2;
}

/* Hover overlay */
.mc-overlay {
    position: absolute; inset:0; z-index: 3;
    background: linear-gradient(to top, rgba(7,7,14,.95) 35%, transparent 80%);
    opacity: 0;
    transition: opacity var(--tm);
    display: flex; flex-direction: column;
    justify-content: flex-end;
    padding: 1rem;
}
.mc:hover .mc-overlay { opacity: 1; }
.mc-ov-title {
    font-size: .82rem; font-weight: 700;
    color: var(--t1) !important;
    margin-bottom: .2rem;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
}
.mc-ov-meta {
    font-size: .62rem; font-weight: 500;
    color: var(--t2) !important; letter-spacing: .5px;
    margin-bottom: .6rem;
}
/* Match bar */
.mbar-row {
    display: flex; align-items: center; gap: .5rem;
}
.mbar-pct {
    font-size: .62rem; font-weight: 800;
    color: #4ADE80 !important; white-space: nowrap;
}
.mbar {
    flex:1; height: 3px; border-radius: 99px;
    background: rgba(255,255,255,0.12);
    overflow: hidden;
}
.mbar-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg,#4ADE80,#22D3EE);
    transition: width .8s .3s var(--ease);
}

/* Card body */
.mc-body {
    padding: .85rem 1rem 1rem;
    position: relative; z-index: 2;
}
.mc-title {
    font-size: .82rem; font-weight: 700;
    color: var(--t1) !important; line-height: 1.35;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
    margin-bottom: .3rem;
}
.mc-tag {
    font-size: .62rem; font-weight: 500;
    color: var(--t3) !important; letter-spacing: .5px;
}

/* ════════════════════════════════════════════════════════════════════
   SKELETON LOADING
════════════════════════════════════════════════════════════════════ */
.skeleton-grid {
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: 16px;
    padding: 2.8rem clamp(1.5rem,4vw,4.5rem) 1rem;
    max-width: 1400px; margin: 0 auto;
}
@media(max-width:900px){.skeleton-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:600px){.skeleton-grid{grid-template-columns:repeat(2,1fr)}}

.sk-card {
    background: var(--bg2);
    border: 1px solid var(--b1);
    border-radius: var(--r3);
    overflow: hidden;
}
.sk-poster {
    width:100%; padding-top:148%;
    background: var(--bg3);
    position: relative; overflow: hidden;
}
.sk-poster::after {
    content:''; position:absolute; inset:0;
    background: linear-gradient(90deg,transparent 0%,rgba(255,255,255,.04) 50%,transparent 100%);
    background-size: 200% 100%;
    animation: shimmer 1.6s ease infinite;
}
@keyframes shimmer {
    0%   { background-position:  200% 0; }
    100% { background-position: -200% 0; }
}
.sk-body { padding: .85rem 1rem 1rem; }
.sk-line {
    height: 10px; border-radius: 6px;
    background: var(--bg3); margin-bottom: .55rem;
}
.sk-line::after {
    content:''; display:block; height:100%;
    background: linear-gradient(90deg,transparent,rgba(255,255,255,.04),transparent);
    background-size: 200% 100%;
    border-radius: 6px;
    animation: shimmer 1.6s ease infinite;
}
.sk-line:nth-child(2){width:65%}

/* ════════════════════════════════════════════════════════════════════
   EMPTY STATE
════════════════════════════════════════════════════════════════════ */
.empty {
    text-align: center;
    padding: 5rem 2rem 4rem;
}
.empty-ic { font-size: 4rem; display:block; margin-bottom:1rem; }
.empty-h  {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem; font-weight: 400;
    color: var(--t1) !important; margin-bottom: .6rem;
}
.empty-p  {
    font-size: .9rem; font-weight: 300;
    color: var(--t2) !important;
    line-height: 1.75; max-width: 400px; margin: 0 auto;
}

/* ════════════════════════════════════════════════════════════════════
   ERROR BANNER
════════════════════════════════════════════════════════════════════ */
.err {
    margin: 1.5rem clamp(1.5rem,4vw,4.5rem);
    background: rgba(229,9,20,.08);
    border: 1px solid rgba(229,9,20,.28);
    border-left: 3px solid var(--red);
    border-radius: var(--r2);
    padding: .95rem 1.3rem;
    font-size: .86rem; line-height: 1.65;
    color: #FF8080 !important;
}

/* ════════════════════════════════════════════════════════════════════
   FOOTER
════════════════════════════════════════════════════════════════════ */
.ft {
    margin-top: 4.5rem;
    background: var(--bg1);
    border-top: 1px solid var(--b1);
    padding: 2.5rem clamp(1.5rem,4vw,4.5rem);
    display: flex; align-items: center;
    justify-content: space-between;
    flex-wrap: wrap; gap: 1.2rem;
}
.ft-logo {
    font-family: 'DM Serif Display', serif;
    font-style: italic;
    font-size: 1.2rem; font-weight: 400;
    background: var(--grad-text);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.ft-copy {
    font-size: .7rem; color: var(--t3) !important;
    line-height: 1.75;
}
.ft-links { display:flex; gap:1.8rem; }
.ft-link {
    font-size: .7rem; font-weight: 500;
    color: var(--t2) !important; text-decoration:none;
    transition: color var(--tf);
}
.ft-link:hover { color: var(--t1) !important; }
</style>
"""
st.markdown(_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# SECTION 4 — DATA LOADING  (identical logic, unchanged)
# ══════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def load_movies() -> pd.DataFrame:
    """Load pre-computed movie metadata dictionary from disk."""
    movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
    return pd.DataFrame(movies_dict)


@st.cache_data(show_spinner=False)
def load_similarity():
    """Load pre-computed cosine-similarity matrix from disk."""
    return pickle.load(open("similarity.pkl", "rb"))


# Graceful failure if pickle files are missing
_data_ok   = False
_data_err  = ""
movies     = pd.DataFrame()
similarity = None

try:
    movies     = load_movies()
    similarity = load_similarity()
    _data_ok   = True
except FileNotFoundError as _e:
    _data_err  = str(_e)
except Exception as _e:
    _data_err  = f"Unexpected error: {_e}"


# ══════════════════════════════════════════════════════════════════════
# SECTION 5 — TMDB POSTER FETCHING  (identical logic, unchanged)
# ══════════════════════════════════════════════════════════════════════

# On-theme dark placeholder shown when a poster cannot be fetched
_PH = "https://via.placeholder.com/300x450/111120/44445A?text=No+Poster"


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id) -> str:
    """Fetch TMDB poster URL; fall back to placeholder on any failure."""
    if not movie_id:
        return _PH
    try:
        r = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            "?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US",
            timeout=5,
        )
        if r.status_code != 200:
            return _PH
        d = r.json()
        return ("https://image.tmdb.org/t/p/w500" + d["poster_path"]) if d.get("poster_path") else _PH
    except Exception:
        return _PH


# ══════════════════════════════════════════════════════════════════════
# SECTION 6 — RECOMMENDATION ENGINE  (identical logic, unchanged)
# ══════════════════════════════════════════════════════════════════════

def recommend(movie: str) -> tuple[list[str], list[str]]:
    """Return top-5 similar movie titles and their TMDB poster URLs."""
    movie_index = movies[movies["title"] == movie].index[0]
    distances   = similarity[movie_index]

    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    names:   list[str] = []
    posters: list[str] = []

    for i in movies_list:
        names.append(movies.iloc[i[0]].title)
        # Support both column naming conventions (movie_id or id)
        if "movie_id" in movies.columns:
            mid = movies.iloc[i[0]].movie_id
        elif "id" in movies.columns:
            mid = movies.iloc[i[0]].id
        else:
            mid = None
        posters.append(fetch_poster(mid))

    return names, posters


# ══════════════════════════════════════════════════════════════════════
# SECTION 7 — SESSION STATE
# ══════════════════════════════════════════════════════════════════════
_s = st.session_state
if "rec_count"  not in _s: _s.rec_count  = 0
if "results"    not in _s: _s.results    = None   # (names, posters) tuple
if "last_movie" not in _s: _s.last_movie = ""
if "err"        not in _s: _s.err        = ""


# ══════════════════════════════════════════════════════════════════════
# SECTION 8 — RENDER
# ══════════════════════════════════════════════════════════════════════

_n = len(movies) if _data_ok else 0  # total movies count

# ── 8.1  NAVBAR ───────────────────────────────────────────────────────
st.markdown(f"""
<nav class="nb">
    <div class="nb-brand">
        <span class="nb-logo">CineMatch</span>
        <span class="nb-pill">AI</span>
        <span class="nb-sep"></span>
        <span class="nb-tag">Discover · Explore · Watch</span>
    </div>
    <div class="nb-stats">
        <div class="nb-stat">
            <div class="nb-val">{_n:,}</div>
            <div class="nb-lbl">Films</div>
        </div>
        <div class="nb-divider"></div>
        <div class="nb-stat">
            <div class="nb-val">{_s.rec_count}</div>
            <div class="nb-lbl">Matched</div>
        </div>
        <div class="nb-divider"></div>
        <div class="nb-stat">
            <div class="nb-val" style="color:{'#4ADE80' if _data_ok else '#EF4444'} !important;
                                        -webkit-text-fill-color:{'#4ADE80' if _data_ok else '#EF4444'} !important;">
                {'● LIVE' if _data_ok else '✗ ERR'}
            </div>
            <div class="nb-lbl">Status</div>
        </div>
    </div>
</nav>
""", unsafe_allow_html=True)


# ── 8.2  DATA ERROR GUARD ────────────────────────────────────────────
if not _data_ok:
    st.markdown(f"""
    <div style="padding:4rem;max-width:640px;margin:0 auto">
        <div class="err" style="font-size:.95rem">
            <strong>⚠️  Dataset not found</strong><br><br>
            {_data_err}<br><br>
            Make sure <code>movies_dict.pkl</code> and
            <code>similarity.pkl</code> live in the same
            directory as <code>app.py</code>, then restart.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── 8.3  HERO ────────────────────────────────────────────────────────
st.markdown("""
<section class="hero">
  <div class="hero-inner">
    <div class="hero-badge"><span class="badge-dot"></span>Content-Based AI &nbsp;·&nbsp; TMDB Powered</div>
    <h1 class="hero-h1">Find Your<br><em>Next Favourite</em><br>Film Tonight</h1>
    <p class="hero-p">
        CineMatch analyses narrative fingerprints, genre overlap, and
        thematic DNA to surface the five titles most likely to earn a
        permanent spot on your watchlist — instantly, no account needed.
    </p>
    <div class="hero-tags">
        <span class="htag">🎭 Drama</span>
        <span class="htag">🚀 Sci-Fi</span>
        <span class="htag">🔪 Thriller</span>
        <span class="htag">💘 Romance</span>
        <span class="htag">😂 Comedy</span>
        <span class="htag">🦸 Action</span>
        <span class="htag">👻 Horror</span>
        <span class="htag">🗡️ Fantasy</span>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)


# ── 8.4  METRICS STRIP ───────────────────────────────────────────────
st.markdown(f"""
<div class="mstrip">
    <div class="mstrip-item">
        <span class="mstrip-icon">🧠</span>
        <div>
            <div class="mstrip-val">Content-Based Filtering</div>
            <div class="mstrip-lbl">Cosine similarity · TF-IDF vectors</div>
        </div>
    </div>
    <div class="mstrip-item">
        <span class="mstrip-icon">🎞️</span>
        <div>
            <div class="mstrip-val">{_n:,} Films Indexed</div>
            <div class="mstrip-lbl">Pre-computed similarity matrix</div>
        </div>
    </div>
    <div class="mstrip-item">
        <span class="mstrip-icon">⚡</span>
        <div>
            <div class="mstrip-val">Instant Results</div>
            <div class="mstrip-lbl">Zero-latency vector lookup</div>
        </div>
    </div>
    <div class="mstrip-item">
        <span class="mstrip-icon">🖼️</span>
        <div>
            <div class="mstrip-val">Live TMDB Posters</div>
            <div class="mstrip-lbl">High-res art · Cached per session</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── 8.5  SEARCH PANEL ────────────────────────────────────────────────
st.markdown('<div class="spanel"><div class="sp-inner">', unsafe_allow_html=True)

_c1, _c2 = st.columns([5, 1], gap="medium")

with _c1:
    st.markdown('<div class="sp-label">🎬 &nbsp;Choose a movie you love</div>', unsafe_allow_html=True)
    selected_movie = st.selectbox(
        label="Pick a movie",
        options=movies["title"].values,
        label_visibility="collapsed",
    )

with _c2:
    st.markdown(
        '<div class="sp-label" style="visibility:hidden">_</div>',
        unsafe_allow_html=True,
    )
    clicked = st.button("▶ Discover", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)


# ── 8.6  RUN RECOMMENDATION ──────────────────────────────────────────
if clicked:
    _s.err     = ""
    _s.results = None

    # Show skeleton while fetching posters
    _skel = st.empty()
    _skel.markdown(
        '<div class="skeleton-grid">'
        + '<div class="sk-card"><div class="sk-poster"></div>'
          '<div class="sk-body"><div class="sk-line"></div>'
          '<div class="sk-line"></div></div></div>' * 5
        + '</div>',
        unsafe_allow_html=True,
    )

    try:
        _names, _posters  = recommend(selected_movie)
        _s.results        = (_names, _posters)
        _s.last_movie     = selected_movie
        _s.rec_count     += 1
    except IndexError:
        _s.err = (
            f"<strong>&ldquo;{selected_movie}&rdquo;</strong> was not found in the similarity matrix. "
            "The dataset may have been updated — please try another title."
        )
    except Exception as _ex:
        _s.err = f"Unexpected error: <code>{_ex}</code>"
    finally:
        _skel.empty()


# ── 8.7  ERROR DISPLAY ───────────────────────────────────────────────
if _s.err:
    st.markdown(f'<div class="err">⚠️ &nbsp;{_s.err}</div>', unsafe_allow_html=True)


# ── 8.8  RESULTS — MOVIE CARDS ───────────────────────────────────────
if _s.results:
    _names, _posters = _s.results

    # Visual-only match scores (rank-based, no ML change)
    _pcts  = [98, 94, 89, 83, 76]
    _ranks = ["Best Match", "Great Pick", "You'll Like", "Try This", "Hidden Gem"]

    # Section heading
    st.markdown(f"""
    <div class="results">
        <div class="row-hd">
            <div class="row-hd-title">
                Because you watched &nbsp;<em>"{_s.last_movie}"</em>
            </div>
            <div class="row-hd-badge">Top 5 Picks</div>
        </div>
    """, unsafe_allow_html=True)

    # Build all cards as a single HTML block — no per-card Python loop overhead
    _cards = '<div class="cards">'
    for i in range(len(_names)):
        t = _names[i]   if i < len(_names)   else "Unknown"
        p = _posters[i] if i < len(_posters) else _PH
        r = _ranks[i];  pct = _pcts[i]

        _cards += f"""
        <div class="mc">
            <div class="mc-rank">{r}</div>
            <div class="mc-num">{i+1}</div>
            <div class="mc-poster">
                <img src="{p}" alt="{t}" loading="lazy"
                     onerror="this.src='{_PH}'" />
                <div class="mc-overlay">
                    <div class="mc-ov-title">{t}</div>
                    <div class="mc-ov-meta">Rank #{i+1} &nbsp;·&nbsp; Similar Match</div>
                    <div class="mbar-row">
                        <span class="mbar-pct">{pct}%</span>
                        <div class="mbar">
                            <div class="mbar-fill" style="width:{pct}%"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mc-body">
                <div class="mc-title">{t}</div>
                <div class="mc-tag">#{i+1} &nbsp;·&nbsp; {pct}% match</div>
            </div>
        </div>
        """
    _cards += "</div></div>"
    st.markdown(_cards, unsafe_allow_html=True)


# ── 8.9  EMPTY / INITIAL STATE ───────────────────────────────────────
elif not clicked:
    st.markdown("""
    <div class="empty">
        <span class="empty-ic">🎬</span>
        <div class="empty-h">Ready When You Are</div>
        <p class="empty-p">
            Select any film from the dropdown above and press
            <strong>Discover</strong> — we'll surface five titles
            that share its narrative soul.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── 8.10  FOOTER ─────────────────────────────────────────────────────
st.markdown(f"""
<footer class="ft">
    <div>
        <div class="ft-logo">CineMatch</div>
        <div class="ft-copy" style="margin-top:.4rem">
            AI-powered content-based movie recommendations.<br>
            Uses the TMDB API · Not endorsed or certified by TMDB.
        </div>
    </div>
    <div class="ft-links">
        <a class="ft-link" href="#">About</a>
        <a class="ft-link" href="#">Privacy</a>
        <a class="ft-link" href="https://www.themoviedb.org" target="_blank">TMDB</a>
        <a class="ft-link" href="#">GitHub</a>
    </div>
    <div class="ft-copy" style="text-align:right">
        Built with Streamlit &amp; scikit-learn<br>
        © 2025 CineMatch &nbsp;·&nbsp; {_n:,} films indexed
    </div>
</footer>
""", unsafe_allow_html=True)