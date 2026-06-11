<div align="center">

# 🎬 CineMatch
### AI-Powered Movie Recommendation System

*Discover your next favorite film with the power of Machine Learning*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br>

**[🚀 View Live Demo](https://movie-recommender-systems-4odx.onrender.com/)** &nbsp;•&nbsp;
**[📖 Documentation](#-machine-learning-pipeline)** &nbsp;•&nbsp;
**[🐛 Report Bug](https://github.com/vikashkumarsingh21/movie-recommender-system/issues)** &nbsp;•&nbsp;
**[✨ Request Feature](https://github.com/vikashkumarsingh21/movie-recommender-system/issues)**

<br>

![CineMatch Demo](https://via.placeholder.com/900x400/1a1a2e/e94560?text=CineMatch+%7C+AI+Movie+Recommendation+System)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Technology Stack](#-technology-stack)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Installation](#-installation)
- [Local Setup](#-local-setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Integration](#-api-integration)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

**CineMatch** is an intelligent movie recommendation system that leverages **Content-Based Filtering** and **Cosine Similarity** to suggest films tailored to your taste. Built with a professional Netflix-inspired UI using Streamlit, CineMatch analyzes movie metadata — genres, cast, crew, keywords, and plot overviews — to find films that are most similar to the one you love.

Whether you're a casual moviegoer or a cinephile, CineMatch helps you cut through the noise and find exactly what to watch next.

> 💡 *"Tell me one movie you love, and I'll find five more you'll adore."*

---

## 🌐 Live Demo

🔗 **[https://movie-recommender-systems-4odx.onrender.com/](https://movie-recommender-systems-4odx.onrender.com/)**

> **Note:** The app is hosted on Render's free tier. It may take **15–30 seconds** to wake up on the first visit. Subsequent loads are fast.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Smart Recommendations** | Get 5 highly relevant movie suggestions instantly |
| 🧠 **Content-Based Filtering** | Recommendations based on movie metadata & semantics |
| 📐 **Cosine Similarity** | Advanced ML algorithm for accurate similarity scoring |
| 🖼️ **Live Poster Fetching** | Real-time movie posters via TMDB API |
| ⚡ **Fast Performance** | Cached data loading for near-instant results |
| 🎨 **Netflix-Style UI** | Clean, dark-themed, responsive interface |
| 📱 **Responsive Design** | Works seamlessly on desktop and mobile |
| 🔄 **Real-Time Processing** | Instant recommendation generation on selection |

---

## 📸 Screenshots

> **Add your screenshots here by replacing the placeholders below.**

<div align="center">

**Homepage — Movie Selection**

![Homepage Screenshot](https://via.placeholder.com/800x450/1a1a2e/ffffff?text=Screenshot+1%3A+Homepage)

<br>

**Recommendations View — Posters & Titles**

![Recommendations Screenshot](https://via.placeholder.com/800x450/1a1a2e/ffffff?text=Screenshot+2%3A+Recommendations)

<br>

**Mobile View**

![Mobile Screenshot](https://via.placeholder.com/400x700/1a1a2e/ffffff?text=Screenshot+3%3A+Mobile+View)

</div>

---

## 🛠️ Technology Stack

### Core Technologies

| Category | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core development language |
| **Web Framework** | Streamlit | Interactive web UI |
| **Data Processing** | Pandas, NumPy | Data manipulation & analysis |
| **Machine Learning** | Scikit-Learn | Vectorization & similarity computation |
| **External API** | TMDB API | Movie posters & metadata |
| **Serialization** | Pickle | Model & data persistence |
| **Deployment** | Render | Cloud hosting platform |

### ML & NLP Libraries

```
scikit-learn  →  CountVectorizer, cosine_similarity
pandas        →  DataFrame operations, data wrangling
numpy         →  Numerical computations
ast           →  Safe literal evaluation for nested data
```

---

## 🤖 Machine Learning Pipeline

CineMatch follows a structured ML workflow from raw data to live recommendations:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CineMatch ML Pipeline                           │
├──────────┬──────────┬────────────┬────────────┬─────────┬──────────┤
│  Stage 1 │  Stage 2 │  Stage 3   │  Stage 4   │ Stage 5 │  Stage 6 │
│  Collect │  Clean   │  Engineer  │ Vectorize  │ Matrix  │ Recommend│
│   Data   │  Data    │ Features   │   Text     │Creation │  Movies  │
└──────────┴──────────┴────────────┴────────────┴─────────┴──────────┘
```

### Stage 1 — 📦 Data Collection
- Source: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (Kaggle)
- Two CSV files: `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`
- ~5,000 movies with rich metadata

### Stage 2 — 🧹 Data Cleaning
- Merged movies and credits DataFrames on the movie title
- Selected relevant features: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`
- Dropped null values and duplicate entries
- Parsed JSON-like string columns using Python's `ast` module

### Stage 3 — ⚙️ Feature Engineering
- Extracted top 3 cast members per movie
- Isolated director from crew data
- Tokenized `overview` text (no spaces for multi-word names)
- Concatenated all features into a unified `tags` column

### Stage 4 — 🔡 Text Vectorization
- Applied **Bag of Words** using `CountVectorizer` (max 5,000 features)
- Applied `Porter Stemmer` to normalize word forms
- Converted the tags corpus into a sparse feature matrix

### Stage 5 — 📊 Cosine Similarity Matrix
- Computed pairwise **Cosine Similarity** across all 5,000 movie vectors
- Resulting in a 5000 × 5000 similarity matrix
- Serialized the matrix and movie data with `Pickle` for fast loading

### Stage 6 — 🎬 Recommendation Generation
- Given a movie title → find its index in the dataset
- Retrieve its similarity scores from the matrix
- Sort scores in descending order → return top 5 results
- Fetch posters for each via TMDB API

---

## 📦 Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Clone the Repository

```bash
git clone https://github.com/vikashkumarsingh21/movie-recommender-system.git
cd movie-recommender-system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Requirements

```txt
streamlit
pandas
numpy
scikit-learn
requests
pickle5
```

---

## 💻 Local Setup

### Step 1 — Get Your TMDB API Key

1. Create a free account at [TMDB](https://www.themoviedb.org/)
2. Navigate to **Settings → API**
3. Copy your **API Key (v3 auth)**

### Step 2 — Configure the API Key

Open `app.py` and locate the poster-fetching function. Replace the placeholder with your key:

```python
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
```

### Step 3 — Prepare Data Files

Ensure these files are in the project root:

```
movies_dict.pkl    ← Movie metadata dictionary
similarity.pkl     ← Precomputed cosine similarity matrix
```

> If the `.pkl` files are missing, run the Jupyter Notebook (`movie_recommender.ipynb`) to regenerate them from the CSV files.

### Step 4 — Run the Application

```bash
streamlit run app.py
```

Then open your browser at: **`http://localhost:8501`**

---

## 🎮 Usage

1. **Open** the application in your browser
2. **Select** a movie from the dropdown menu (e.g., *The Dark Knight*)
3. **Click** the **"Show Recommendations"** button
4. **Browse** the 5 recommended movies displayed with their posters
5. **Explore** — repeat with any movie you like!

---

## 📁 Project Structure

```
CineMatch/
│
├── app.py                    # Main Streamlit application
├── movies_dict.pkl           # Serialized movie metadata (DataFrame → dict)
├── movies.pkl                # Serialized movies list
├── similarity.pkl            # Precomputed cosine similarity matrix
│
├── tmdb_5000_movies.csv      # Raw TMDB movies dataset
├── tmdb_5000_credits.csv     # Raw TMDB credits dataset
│
├── movie_recommender.ipynb   # Jupyter Notebook (data processing & model)
│
├── requirements.txt          # Python dependencies
├── setup.sh                  # Render deployment setup script
│
└── README.md                 # Project documentation
```

---

## 🔌 API Integration

CineMatch integrates with the **TMDB (The Movie Database) API** to fetch real-time movie posters.

### Endpoint Used

```
GET https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US
```

### Poster URL Construction

```python
base_url = "https://image.tmdb.org/t/p/w500/"
poster_path = response_data['poster_path']
full_url = base_url + poster_path
```

### Rate Limits

| Plan | Requests/Second | Requests/Day |
|---|---|---|
| Free | 40 | ~3,000 |

> The app fetches 5 posters per recommendation request, well within free tier limits.

### Error Handling

```python
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
except Exception:
    return "https://via.placeholder.com/500x750?text=No+Poster"
```

---

## 🚀 Future Improvements

Here's the roadmap for upcoming features:

- [ ] 🤝 **Collaborative Filtering** — Add user-behavior-based recommendations
- [ ] 🔍 **Search Autocomplete** — Fuzzy search for movie titles
- [ ] ⭐ **User Ratings** — Allow users to rate movies and refine suggestions
- [ ] 🎭 **Genre Filters** — Filter recommendations by genre, year, or language
- [ ] 🗂️ **Watchlist Feature** — Save and manage movies to watch later
- [ ] 🔐 **User Authentication** — Personal profiles with viewing history
- [ ] 📊 **Recommendation Explanations** — Show *why* a movie was recommended
- [ ] 🌍 **Multilingual Support** — Recommendations in multiple languages
- [ ] 🎬 **Trailer Integration** — Embed YouTube trailers for each movie
- [ ] 🧪 **A/B Testing** — Compare recommendation algorithms

---

## 🤝 Contributing

Contributions are what make the open-source community amazing. Any contributions you make are **greatly appreciated**.

### How to Contribute

1. **Fork** the repository
2. **Create** your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your changes
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 style for Python code
- Write clear, descriptive commit messages
- Add comments for complex logic
- Update the README if you add/change features
- Test thoroughly before submitting a PR

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

```
MIT License — free to use, modify, and distribute with attribution.
```

---

## 👨‍💻 Author

<div align="center">

### Vikas Kumar

*Machine Learning Engineer & Full Stack Developer*

[![GitHub](https://img.shields.io/badge/GitHub-vikashkumarsingh21-181717?style=for-the-badge&logo=github)](https://github.com/vikashkumarsingh21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/your-linkedin-username)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://your-portfolio-url.com)

</div>

---

## 🙏 Acknowledgements

- [TMDB](https://www.themoviedb.org/) — for the movie database and API
- [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — for the TMDB 5000 dataset
- [Streamlit](https://streamlit.io/) — for the amazing web framework
- [Scikit-Learn](https://scikit-learn.org/) — for ML utilities
- [Render](https://render.com/) — for free cloud deployment

---

<div align="center">

⭐ **If you found this project helpful, please give it a star!** ⭐

*Made with ❤️ by [Vikas Kumar](https://github.com/vikashkumarsingh21)*

</div>