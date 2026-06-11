"""
╔══════════════════════════════════════════════════════════╗
║         🎬 CineMatch — Movie Recommendation System       ║
║         UI/UX Redesign  |  Production-Ready              ║
╚══════════════════════════════════════════════════════════╝

Architecture:
  - All backend / ML logic is unchanged from original.
  - Only UI, CSS, layout, and presentation layers are modified.
  - Sections are clearly delimited for maintainability.
"""

import streamlit as st
import pickle
import pandas as pd
import requests

# ══════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION  (must be the very first Streamlit call)
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CineMatch — Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# 2. GLOBAL CSS  — dark cinema theme + glassmorphism + animations
# ══════════════════════════════════════════════════════════════
GLOBAL_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── CSS Tokens ── */
:root {
    --bg-base:      #0A0A0F;
    --bg-surface:   #12121A;
    --bg-card:      #1A1A28;
    --bg-glass:     rgba(26, 26, 40, 0.72);
    --accent-red:   #E50914;
    --accent-gold:  #F5A623;
    --accent-grad:  linear-gradient(135deg, #E50914 0%, #F5A623 100%);
    --text-primary: #FFFFFF;
    --text-muted:   #A0A0B0;
    --border:       rgba(255,255,255,0.07);
    --radius-card:  14px;
    --radius-btn:   8px;
    --shadow-card:  0 8px 32px rgba(0,0,0,0.55);
    --transition:   0.28s cubic-bezier(.4,0,.2,1);
}

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 1400px; }

/* ══════════════════════════
   SIDEBAR
══════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

.sidebar-brand {
    text-align: center;
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sidebar-brand h1 {
    font-family: 'Bebas Neue', cursive;
    font-size: 2.4rem;
    letter-spacing: 3px;
    background: var(--accent-grad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.25rem 0 0;
    line-height: 1;
}
.sidebar-brand p {
    font-size: 0.72rem;
    color: var(--text-muted) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.35rem;
}

/* Stat cards in sidebar */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 1rem 1.2rem;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    transition: border-color var(--transition);
}
.stat-card:hover { border-color: rgba(229,9,20,0.45); }
.stat-icon { font-size: 1.6rem; flex-shrink: 0; }
.stat-value {
    font-size: 1.35rem;
    font-weight: 700;
    line-height: 1;
}
.stat-label {
    font-size: 0.7rem;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 0.2rem;
}

/* ══════════════════════════
   HERO SECTION
══════════════════════════ */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #0D0D1A 0%, #1A0A12 50%, #0A0A15 100%);
    border-radius: 20px;
    padding: 4rem 3.5rem;
    margin: 2rem 0 2.5rem;
    border: 1px solid var(--border);
}

/* film-strip accent lines */
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 38px,
            rgba(229,9,20,0.06) 38px,
            rgba(229,9,20,0.06) 40px
        );
    pointer-events: none;
}
/* ambient glow */
.hero::after {
    content: '';
    position: absolute;
    top: -60px; right: -80px;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(229,9,20,0.18) 0%, transparent 70%);
    pointer-events: none;
}

.hero-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent-gold);
    margin-bottom: 0.9rem;
    font-weight: 600;
}
.hero-title {
    font-family: 'Bebas Neue', cursive;
    font-size: clamp(3rem, 6vw, 5.5rem);
    line-height: 0.95;
    letter-spacing: 3px;
    background: var(--accent-grad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.6rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--text-muted);
    max-width: 520px;
    line-height: 1.6;
    font-weight: 300;
}

/* ══════════════════════════
   SELECTOR AREA
══════════════════════════ */
.selector-wrapper {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 2.5rem;
}
.selector-label {
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
    font-weight: 600;
}

/* Streamlit selectbox override */
div[data-testid="stSelectbox"] label { display: none; }
div[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-btn) !important;
    color: var(--text-primary) !important;
    font-size: 1rem !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent-red) !important;
    box-shadow: 0 0 0 2px rgba(229,9,20,0.25) !important;
}

/* ── Recommend button ── */
div[data-testid="stButton"] > button {
    background: var(--accent-grad) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-btn) !important;
    padding: 0.65rem 2.2rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    transition: opacity var(--transition), transform var(--transition) !important;
    box-shadow: 0 4px 16px rgba(229,9,20,0.35) !important;
    width: 100%;
    cursor: pointer;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ══════════════════════════
   SECTION HEADING
══════════════════════════ */
.section-heading {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0 0 1.5rem;
}
.section-heading span {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.65rem;
    letter-spacing: 2px;
}
.heading-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ══════════════════════════
   MOVIE CARDS
══════════════════════════ */
.movie-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    overflow: hidden;
    transition: transform var(--transition), border-color var(--transition), box-shadow var(--transition);
    cursor: pointer;
    position: relative;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-8px) scale(1.015);
    border-color: rgba(229,9,20,0.55);
    box-shadow: 0 20px 48px rgba(229,9,20,0.2), var(--shadow-card);
}

/* rank badge */
.rank-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: var(--accent-grad);
    color: #fff;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 20px;
    z-index: 2;
    box-shadow: 0 2px 8px rgba(229,9,20,0.45);
}

.card-poster-wrap {
    position: relative;
    width: 100%;
    padding-top: 150%;   /* 2:3 aspect ratio */
    overflow: hidden;
    background: var(--bg-surface);
}
.card-poster-wrap img {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    transition: transform 0.45s ease;
}
.movie-card:hover .card-poster-wrap img {
    transform: scale(1.07);
}

/* gradient overlay at bottom of poster */
.card-poster-wrap::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 55%;
    background: linear-gradient(to top, var(--bg-card) 0%, transparent 100%);
    pointer-events: none;
}

.card-body {
    padding: 0.85rem 1rem 1rem;
}
.card-title {
    font-size: 0.9rem;
    font-weight: 600;
    line-height: 1.35;
    margin-bottom: 0.3rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.card-meta {
    font-size: 0.68rem;
    color: var(--text-muted);
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

/* ══════════════════════════
   ERROR / EMPTY STATE
══════════════════════════ */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}
.empty-state .icon { font-size: 3.5rem; margin-bottom: 0.8rem; }
.empty-state p { font-size: 1rem; line-height: 1.6; }

.error-banner {
    background: rgba(229,9,20,0.12);
    border: 1px solid rgba(229,9,20,0.35);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
    font-size: 0.88rem;
    color: #FF6B6B;
}

/* ══════════════════════════
   SPINNER override
══════════════════════════ */
div[data-testid="stSpinner"] > div {
    border-top-color: var(--accent-red) !important;
}

/* ══════════════════════════
   FOOTER
══════════════════════════ */
.footer {
    border-top: 1px solid var(--border);
    padding: 2rem 0 1rem;
    margin-top: 3.5rem;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78rem;
    letter-spacing: 0.5px;
    line-height: 1.8;
}
.footer strong { color: var(--text-primary); }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 3. DATA LOADING  (logic unchanged from original)
# ══════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def load_movies() -> pd.DataFrame:
    """Load the pre-computed movie metadata dictionary from disk."""
    movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
    return pd.DataFrame(movies_dict)


@st.cache_data(show_spinner=False)
def load_similarity():
    """Load the pre-computed cosine-similarity matrix from disk."""
    return pickle.load(open("similarity.pkl", "rb"))


# Attempt to load data; surface a friendly error if files are missing
try:
    movies = load_movies()
    similarity = load_similarity()
    data_loaded = True
except FileNotFoundError as exc:
    data_loaded = False
    load_error = str(exc)
except Exception as exc:
    data_loaded = False
    load_error = f"Unexpected error loading data: {exc}"


# ══════════════════════════════════════════════════════════════
# 4. TMDB API  (logic unchanged from original)
# ══════════════════════════════════════════════════════════════

PLACEHOLDER_POSTER = "https://via.placeholder.com/300x450/1A1A28/A0A0B0?text=No+Poster"


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id: int) -> str:
    """
    Fetch a movie poster URL from the TMDB API.
    Falls back to a placeholder on any failure.
    """
    if not movie_id:
        return PLACEHOLDER_POSTER
    try:
        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            "?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return PLACEHOLDER_POSTER
        data = response.json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
        return PLACEHOLDER_POSTER
    except Exception:
        return PLACEHOLDER_POSTER


# ══════════════════════════════════════════════════════════════
# 5. RECOMMENDATION ENGINE  (logic unchanged from original)
# ══════════════════════════════════════════════════════════════

def recommend(movie: str) -> tuple[list[str], list[str]]:
    """
    Return the top-5 most similar movies and their poster URLs.
    Handles missing movie_id / id columns gracefully.
    """
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        enumerate(distances), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies: list[str] = []
    recommended_posters: list[str] = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

        # Resolve the TMDB id column (supports both naming conventions)
        if "movie_id" in movies.columns:
            movie_id = movies.iloc[i[0]].movie_id
        elif "id" in movies.columns:
            movie_id = movies.iloc[i[0]].id
        else:
            movie_id = None

        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ══════════════════════════════════════════════════════════════
# 6. SESSION STATE  — track generated recommendations count
# ══════════════════════════════════════════════════════════════
if "rec_count" not in st.session_state:
    st.session_state.rec_count = 0
if "results" not in st.session_state:
    st.session_state.results = None      # (names, posters) tuple or None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = ""


# ══════════════════════════════════════════════════════════════
# 7. SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Branding ──
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size:2.5rem">🎬</div>
        <h1>CINEMATCH</h1>
        <p>AI Movie Recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats cards ──
    total_movies = len(movies) if data_loaded else 0

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">🎞️</div>
        <div>
            <div class="stat-value">{total_movies:,}</div>
            <div class="stat-label">Movies in Library</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">✨</div>
        <div>
            <div class="stat-value">{st.session_state.rec_count}</div>
            <div class="stat-label">Recommendations Given</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">💾</div>
        <div>
            <div class="stat-value">{'✓' if data_loaded else '✗'}</div>
            <div class="stat-label">Dataset Loaded</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── About blurb ──
    st.markdown("""
    <p style="font-size:0.78rem; color:#A0A0B0; line-height:1.7; padding:0 0.2rem;">
        CineMatch uses content-based filtering and a pre-computed
        cosine-similarity matrix to surface movies most likely to
        match your taste. Posters are sourced via the TMDB API.
    </p>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 8. MAIN CONTENT AREA
# ══════════════════════════════════════════════════════════════

# ── 8a. Data error guard ──
if not data_loaded:
    st.markdown(f"""
    <div class="error-banner">
        ⚠️ <strong>Could not load dataset.</strong><br>
        {load_error}<br>
        Make sure <code>movies_dict.pkl</code> and <code>similarity.pkl</code>
        exist in the same directory as this script.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── 8b. Hero section ──
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🍿 Powered by Content-Based Filtering</div>
    <div class="hero-title">Find Your<br>Next Favourite Film</div>
    <p class="hero-sub">
        Pick any movie from our library and CineMatch will surface five
        titles with the closest narrative and stylistic DNA — no ratings,
        no popularity bias, just genuine similarity.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 8c. Movie selector ──
st.markdown('<div class="selector-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="selector-label">🎬 Choose a movie you love</div>', unsafe_allow_html=True)

col_select, col_btn = st.columns([4, 1], gap="medium")

with col_select:
    selected_movie = st.selectbox(
        label="Movie selector",     # hidden via CSS
        options=movies["title"].values,
        label_visibility="collapsed",
    )

with col_btn:
    # Vertical centering hack — empty label creates matching top offset
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    recommend_clicked = st.button("🎯 Recommend", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── 8d. Run recommendation on button click ──
if recommend_clicked:
    st.session_state.error_msg = ""
    with st.spinner("Scanning the film library…"):
        try:
            names, posters = recommend(selected_movie)
            st.session_state.results = (names, posters)
            st.session_state.rec_count += 1
        except IndexError:
            st.session_state.error_msg = (
                f"Could not find **{selected_movie}** in the similarity matrix. "
                "The dataset may have been updated. Please try a different title."
            )
            st.session_state.results = None
        except Exception as exc:
            st.session_state.error_msg = f"An unexpected error occurred: {exc}"
            st.session_state.results = None

# ── 8e. Surface any errors ──
if st.session_state.error_msg:
    st.markdown(
        f'<div class="error-banner">⚠️ {st.session_state.error_msg}</div>',
        unsafe_allow_html=True,
    )

# ── 8f. Render recommendation cards ──
if st.session_state.results:
    names, posters = st.session_state.results

    # Section heading
    st.markdown(f"""
    <div class="section-heading">
        <span>Because You Liked <em style="color:#E50914">{selected_movie}</em></span>
        <div class="heading-line"></div>
        <span style="font-size:0.8rem; color:#A0A0B0; letter-spacing:1px; font-family:'Inter',sans-serif;">
            TOP 5 PICKS
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Five cards in equal columns
    cols = st.columns(5, gap="small")
    rank_labels = ["#1 Pick", "#2 Pick", "#3 Pick", "#4 Pick", "#5 Pick"]

    for idx, col in enumerate(cols):
        with col:
            title   = names[idx]   if idx < len(names)   else "Unknown"
            poster  = posters[idx] if idx < len(posters) else PLACEHOLDER_POSTER
            rank    = rank_labels[idx]

            st.markdown(f"""
            <div class="movie-card">
                <div class="rank-badge">{rank}</div>
                <div class="card-poster-wrap">
                    <img src="{poster}"
                         alt="{title} poster"
                         loading="lazy"
                         onerror="this.src='{PLACEHOLDER_POSTER}'" />
                </div>
                <div class="card-body">
                    <div class="card-title">{title}</div>
                    <div class="card-meta">Similar Match</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

else:
    # Empty / initial state
    if not recommend_clicked:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🎬</div>
            <p>Select a movie above and hit <strong>Recommend</strong><br>
            to discover your next favourite film.</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 9. FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    <strong>CineMatch</strong> — Content-Based Movie Recommendation System<br>
    Poster data provided by <strong>The Movie Database (TMDB)</strong> &nbsp;·&nbsp;
    Built with <strong>Streamlit</strong> &amp; <strong>scikit-learn</strong>
    <br><br>
    <span style="opacity:0.45">
        This product uses the TMDB API but is not endorsed or certified by TMDB.
    </span>
</div>
""", unsafe_allow_html=True)