import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import re
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Franchise Concept Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Color palette ─────────────────────────────────────────────────────────
MAGENTA   = "#E040FB"
TURQUOISE = "#00BCD4"
BLUE      = "#1565C0"
GOLD      = "#FFD600"
BG_DARK   = "#0A0A0F"
BG_CARD   = "#12121A"
BG_INPUT  = "#1A1A26"
TEXT_MAIN = "#F0F0F0"
TEXT_DIM  = "#8888AA"

# ── CSS ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Orbitron:wght@700;900&display=swap');

  html, body, [class*="css"] {{
      background-color: {BG_DARK};
      color: {TEXT_MAIN};
      font-family: 'Space Grotesk', sans-serif;
  }}

  .stApp {{ background-color: {BG_DARK}; }}

  
  section.main > div {{
      max-width: 100% !important;
      line-height: 1 !important;
  }}
  .main-header {{
      text-align: center;
      padding: 2.5rem 0 1rem 0;
  }}
  .main-title {{
      font-family: 'Orbitron', monospace;
      font-size: 10rem;
      font-weight: 900;
      background: linear-gradient(90deg, {MAGENTA}, {TURQUOISE}, {GOLD});
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: 0.05em;
      margin: 0 auto;
      display: block;
      text-align: center;
  }}
  
  .main-subtitle {{
      color: #C0C0D8;
      font-size: 1.15rem;
      font-weight: 400;
      margin-top: 0.5rem;
      letter-spacing: 0.08em;
  }}
  .divider {{
      height: 1px;
      background: linear-gradient(90deg, transparent, {MAGENTA}55, {TURQUOISE}55, transparent);
      margin: 1.5rem 0;
  }}
  .card {{
      background: {BG_CARD};
      border: 1px solid #ffffff11;
      border-radius: 12px;
      padding: 1.4rem 1.6rem;
      margin-bottom: 1rem;
  }}
  .card-title {{
      font-family: 'Orbitron', monospace;
      font-size: 0.85rem;
      letter-spacing: 0.15em;
      color: {TURQUOISE};
      text-transform: uppercase;
      margin-bottom: 0.8rem;
  }}
  .metric-row {{
      display: flex;
      gap: 0.6rem;
      margin-bottom: 1rem;
      flex-wrap: nowrap;
  }}
  .metric-box {{
      flex: 1;
      background: {BG_INPUT};
      border-radius: 10px;
      padding: 1rem;
      text-align: center;
      border: 1px solid #ffffff0a;
  }}
  .metric-value {{
      font-family: 'Orbitron', monospace;
      font-size: 1.6rem;
      font-weight: 700;
      color: {GOLD};
  }}
  .metric-label {{
      font-size: 0.68rem;
      color: {TEXT_DIM};
      margin-top: 0.2rem;
      letter-spacing: 0.02em;
      line-height: 1.3;
  }}
  .prob-container {{
      text-align: center;
      padding: 1.5rem;
  }}
  .prob-number {{
      font-family: 'Orbitron', monospace;
      font-size: 4rem;
      font-weight: 900;
      line-height: 1;
  }}
  .prob-label {{
      font-size: 0.85rem;
      letter-spacing: 0.15em;
      color: {TEXT_DIM};
      margin-top: 0.4rem;
  }}
  .verdict-strong  {{ color: #00E676; font-weight: 600; font-size: 1.1rem; }}
  .verdict-moderate{{ color: {GOLD};   font-weight: 600; font-size: 1.1rem; }}
  .verdict-weak    {{ color: #FF5252; font-weight: 600; font-size: 1.1rem; }}
  .tag {{
      display: inline-block;
      background: rgba(0,188,212,0.12);
      border: 1px solid rgba(0,188,212,0.4);
      color: {TURQUOISE};
      border-radius: 20px;
      padding: 0.2rem 0.7rem;
      font-size: 0.78rem;
      margin: 0.2rem;
  }}
  .tag-gold {{
      background: rgba(255,214,0,0.12);
      border-color: rgba(255,214,0,0.4);
      color: {GOLD};
  }}
  .tag-teal {{
      background: rgba(0,188,212,0.12);
      border-color: rgba(0,188,212,0.4);
      color: {TURQUOISE};
  }}
  .show-row {{
      display: flex;
      align-items: center;
      padding: 0.35rem 0.6rem;
      border-radius: 6px;
      margin: 0.15rem 0;
      font-size: 0.83rem;
  }}
  .show-row-franchise {{
      background: rgba(255,214,0,0.07);
      border-left: 3px solid {GOLD};
  }}
  .show-row-regular {{
      background: rgba(255,255,255,0.03);
      border-left: 3px solid rgba(136,136,170,0.3);
  }}
  .show-title {{ flex: 1; color: #D0D0E8; font-size: 0.85rem; }}
  .show-rating {{ color: #9090B8; font-size: 0.78rem; margin-left: 0.5rem; }}
  .stSelectbox > div > div,
  .stTextInput > div > div > input,
  .stNumberInput > div > div > input {{
      background-color: {BG_INPUT} !important;
      border: 1px solid #ffffff22 !important;
      color: {TEXT_MAIN} !important;
      border-radius: 8px !important;
  }}
  .stButton > button {{
      background: linear-gradient(135deg, {MAGENTA}, {BLUE}) !important;
      color: white !important;
      border: none !important;
      border-radius: 8px !important;
      font-family: 'Orbitron', monospace !important;
      font-size: 0.85rem !important;
      letter-spacing: 0.1em !important;
      padding: 0.6rem 2rem !important;
      width: 100% !important;
      transition: opacity 0.2s !important;
  }}
  .stButton > button:hover {{ opacity: 0.85 !important; }}
  label, .stSelectbox label, .stTextInput label, .stNumberInput label {{
      color: #C0C0D8 !important;
      font-size: 0.85rem !important;
      letter-spacing: 0.04em !important;
  }}
  .stSlider > div > div > div {{ background: {MAGENTA} !important; }}
  .stNumberInput button {{
      background-color: {MAGENTA} !important;
      border-color: {MAGENTA} !important;
      color: white !important;
      border-radius: 6px !important;
  }}
  hr {{ border-color: #ffffff11 !important; }}
  .stMultiSelect span[data-baseweb="tag"] {{
      background-color: rgba(0,188,212,0.2) !important;
      border: 1px solid rgba(0,188,212,0.5) !important;
      color: {TURQUOISE} !important;
      border-radius: 20px !important;
  }}
  .stMultiSelect span[data-baseweb="tag"] span {{
      color: {TURQUOISE} !important;
  }}
  .stMultiSelect [role="button"] svg {{
      fill: {TURQUOISE} !important;
  }}
  .footer {{
      text-align: center;
      color: {TEXT_DIM};
      font-size: 0.78rem;
      padding: 2rem 0 1rem 0;
      letter-spacing: 0.08em;
  }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_resource(ttl=1)
def load_models():
    xgb   = joblib.load('models/xgb_clean.pkl')
    cols = joblib.load('models/feature_cols_clean.pkl')
    return xgb, cols

@st.cache_data
def load_data():
    df_kids = pd.read_csv('models/df_kids_franchise.csv')
    df_mod  = pd.read_csv('models/df_model.csv')
    df_toys = pd.read_csv('models/df_toys.csv')
    opp     = pd.read_csv('models/opportunity.csv')
    with open('models/theme_categories.json') as f:
        themes = json.load(f)
    return df_kids, df_mod, df_toys, opp, themes

xgb_clean, feature_cols_clean = load_models()
df_kids_franchise, df_model, df_toys, opportunity, THEME_CATEGORIES = load_data()

# ── Build inverted index for O(1) animal lookup ───────────────────────────
ANIMAL_INDEX = {}
for cat, keywords in THEME_CATEGORIES.items():
    ANIMAL_INDEX[cat] = cat
    for kw in keywords:
        ANIMAL_INDEX[kw] = cat

# ── Helpers ────────────────────────────────────────────────────────────────
def find_animal_theme(animal, _=None):
    return ANIMAL_INDEX.get(animal.lower(), None)

def analyze_title(title_text):
    words = title_text.strip().split()
    word_count = len(words)
    STOPWORDS = {'the','of','and','a','an','in','is','it','to','for','on','with','at','by','from'}
    HERO_KW   = ['patrol','rescue','hero','super','power','force','ranger',
                 'guard','squad','team','crew','league']
    proper    = [w for w in words if w and w[0].isupper() and w.lower() not in STOPWORDS]
    has_character = 1 if len(proper) >= 2 else 0
    has_hero      = 1 if any(re.search(rf'\b{k}\b', title_text.lower()) for k in HERO_KW) else 0
    return word_count, has_character, has_hero

def build_feature_vector(concept, feature_cols_clean, df_model):
    vec = {}
    for col in feature_cols_clean:
        vec[col] = df_model[col].median() if col in df_model.columns else 0

    vec['runtimeMinutes']         = concept['runtime_minutes']
    vec['on_streaming']           = concept['on_streaming']
    vec['netflix_pop_filled']     = 45.0 if concept['on_streaming'] else 0.0
    vec['genre_adventure']        = concept['genre_adventure']
    vec['genre_family']           = concept['genre_family']
    vec['genre_comedy']           = concept['genre_comedy']
    vec['genre_action']           = concept['genre_action']
    vec['genre_animation']        = 1
    vec['title_word_count']       = concept['title_word_count']
    vec['title_has_character']    = concept['title_has_character']
    vec['title_has_hero_keyword'] = concept['title_has_hero_keyword']
    vec['premiere_year']          = 2025
    vec['run_years']              = 0
    vec['seasons']                = 1

    animal_lower = concept['protagonist_animal'].lower()
    HIGH_ANIMALS = ['duck','bear','turtle','bee','panda','shark',
                    'dinosaur','dino','rex','raptor']
    vec['title_has_high_animal'] = int(animal_lower in HIGH_ANIMALS)

    for col in feature_cols_clean:
        if col.startswith('country_grouped_'):
            vec[col] = 1 if col == f"country_grouped_{concept['country']}" else 0
    for col in feature_cols_clean:
        if col.startswith('technique_grouped_'):
            vec[col] = 1 if col == f"technique_grouped_{concept['technique']}" else 0
    for col in feature_cols_clean:
        if col.startswith('era_'):
            vec[col] = 1 if col == 'era_Streaming Era (2010+)' else 0

    vec['log_votes_per_year'] = 0.0
    vec['averageRating']      = 7.0
   
    return pd.DataFrame([vec])[feature_cols_clean]

# ── Premise tag → genre signal mapping ────────────────────────────────────
PREMISE_TO_GENRE = {
    "Battle/War":       {'genre_action': 1},
    "Competition":      {'genre_action': 1},
    "Sports":           {'genre_action': 1},
    "Exploration":      {'genre_adventure': 1},
    "Mystery":          {'genre_adventure': 1},
    "Friendship":       {'genre_family': 1},
    "Family bonds":     {'genre_family': 1},
    "School/Learning":  {'genre_family': 1},
    "Music":            {'genre_comedy': 1},
    "Comedy/Slapstick": {'genre_comedy': 1},
    "Magic/Fantasy":    {'genre_adventure': 1},
    "Science/Tech":     {'genre_adventure': 1},
}

AGE_TO_SIGNALS = {
    '0–3':   {'runtime_minutes': 7,  'genre_family': 1, 'genre_adventure': 0, 'genre_action': 0},
    '4–9':   {'runtime_minutes': 23, 'genre_family': 1, 'genre_adventure': 1, 'genre_action': 0},
    '10–13': {'runtime_minutes': 23, 'genre_family': 0, 'genre_adventure': 1, 'genre_action': 1},
    '14–18': {'runtime_minutes': 23, 'genre_family': 0, 'genre_adventure': 1, 'genre_action': 1},
}

# ═══════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="main-header">
  <p class="main-title">FRANCHISE<br>CONCEPT ANALYZER</p>          
  <p class="main-subtitle"> 74 years · 3,602 shows · Amazon · Netflix · YouTube · Machine Learning</p>
  <p style="color:{TURQUOISE};font-size:0.95rem;margin-top:0.4rem;letter-spacing:0.08em;font-weight:500;">
    4 datasets · XGBoost · 32 ML features · SHAP-validated
  </p>

</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# INPUT PANEL
# ═══════════════════════════════════════════════════════════════════════════
with st.container():
    st.markdown('<div class="card"><div class="card-title">🎬 Your Concept</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 2])

    with c1:
        series_title = st.text_input("Series Title", value="",
                                     placeholder="e.g. Dino Spark, Luna Bear...")
        animal = st.text_input("Protagonist Animal", value="",
                               placeholder="e.g. monkey, unicorn, bear...")

    with c2:
        country = st.selectbox("Country of Production",
            ["United Kingdom", "United States", "Canada", "Australia",
             "France", "Brazil", "Coproduction", "Other"])
        technique = st.selectbox("Animation Technique",
            ["Traditional", "CGI", "Flash", "Stop Motion", "Other"])

    with c3:
        runtime = st.number_input("Runtime (minutes)", min_value=5, max_value=60,
                                  value=23, step=1)
        on_streaming = st.selectbox("On Streaming?", ["Yes", "No"]) == "Yes"

    with c4:
        genres = st.multiselect("Genres",
            ["Adventure", "Family", "Comedy", "Action"],
            default=["Adventure", "Family"])
        premise_tags = st.multiselect("Premise Tags",
            ["Friendship", "Competition", "Exploration", "Battle/War",
             "Mystery", "School/Learning", "Music", "Sports",
             "Family bonds", "Magic/Fantasy", "Science/Tech", "Comedy/Slapstick"],
            default=["Exploration"])

    with c5:
        auto_words, auto_char, auto_hero = analyze_title(series_title) if series_title.strip() else (0, 0, 0)
        title_words   = auto_words if series_title.strip() else 2
        has_character = auto_char
        has_hero_kw   = auto_hero

        # Detect animal in title
        detected_animal = ''
        if series_title.strip():
            title_lower = series_title.lower()
            for cat, keywords in THEME_CATEGORIES.items():
                if any(re.search(rf'\b{k}\b', title_lower) for k in keywords):
                    detected_animal = cat
                    break

        st.markdown(f"""
        <div style="background:{BG_INPUT};border-radius:8px;padding:0.8rem;margin-bottom:0.8rem;">
          <div class="card-title" style="margin-bottom:0.4rem;">📝 Title Analysis</div>
          <div style="font-size:0.82rem;color:{TEXT_MAIN};">
            Words: <b style="color:{GOLD};">{auto_words if series_title.strip() else '—'}</b> &nbsp;·&nbsp;
            Character: <b style="color:{GOLD};">{'Yes' if auto_char else ('No' if series_title.strip() else '—')}</b> &nbsp;·&nbsp;
            Hero keyword: <b style="color:{'#FF5252' if auto_hero else GOLD};">{'⚠️ Yes' if auto_hero else ('No' if series_title.strip() else '—')}</b>
          </div>
          {f'<div style="margin-top:0.4rem;font-size:0.78rem;color:{TURQUOISE};"> 🔍 Keywords detected in title: <b>{detected_animal.upper()}</b></div>' if detected_animal else ''}
        </div>
        """, unsafe_allow_html=True)

        target_age = st.selectbox("Target Age Range",
            ["0–3", "4–9", "10–13", "14–18"])

    st.markdown('</div>', unsafe_allow_html=True)
    analyze = st.button("⚡  ANALYZE CONCEPT")

# ═══════════════════════════════════════════════════════════════════════════
# ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
if analyze:

    # ── Input validation ──────────────────────────────────────────────────
    if not animal.strip():
        st.warning("⚠️  Please enter a protagonist animal before analyzing.")
        st.stop()

    # ── Merge signals ─────────────────────────────────────────────────────
    premise_genre_boost = {'genre_adventure':0,'genre_family':0,'genre_comedy':0,'genre_action':0}
    for tag in premise_tags:
        for k, v in PREMISE_TO_GENRE.get(tag, {}).items():
            premise_genre_boost[k] = max(premise_genre_boost[k], v)

    age_signals = AGE_TO_SIGNALS.get(target_age, {})

    concept = {
        'protagonist_animal':     animal,
        'country':                country,
        'technique':              technique,
        'on_streaming':           int(on_streaming),
        'runtime_minutes':        age_signals.get('runtime_minutes', runtime),
        'title_word_count':       title_words,
        'title_has_character':    int(has_character),
        'title_has_hero_keyword': int(has_hero_kw),
        'genre_adventure': max(int("Adventure" in genres), premise_genre_boost['genre_adventure'], age_signals.get('genre_adventure', 0)),
        'genre_family':    max(int("Family"    in genres), premise_genre_boost['genre_family'],    age_signals.get('genre_family', 0)),
        'genre_comedy':    max(int("Comedy"    in genres), premise_genre_boost['genre_comedy'],    0),
        'genre_action':    max(int("Action"    in genres), premise_genre_boost['genre_action'],    age_signals.get('genre_action', 0)),
    }

    animal_lower  = animal.lower().strip()
    matched_theme = find_animal_theme(animal_lower)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Title summary ─────────────────────────────────────────────────────
    if series_title.strip():
        st.markdown(f"""
        <div style="text-align:center;padding:0.5rem 0 1rem 0;">
          <span style="font-family:Orbitron;font-size:1.4rem;color:{TEXT_MAIN};">"{series_title}"</span>
          &nbsp;&nbsp;
          <span style="color:{TEXT_DIM};font-size:0.85rem;">{animal.upper()} · {country} · {technique}</span>
        </div>
        """, unsafe_allow_html=True)


    # ── ROW 1: Market Analysis + Probability ─────────────────────────────
    col_market, col_prob = st.columns([3, 2])

    with col_market:
        st.markdown(f'<div class="card"><div class="card-title">📺 Market Analysis — {animal.upper()}</div>', unsafe_allow_html=True)

        if matched_theme and matched_theme in df_kids_franchise['theme'].values:
            shows        = df_kids_franchise[df_kids_franchise['theme'] == matched_theme]
            n_shows      = len(shows)
            n_franchises = int(shows['is_franchise_final'].sum())
            avg_rating   = shows['averageRating'].mean()
            success_rate = n_franchises / n_shows * 100

            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-box">
                <div class="metric-value">{n_shows}</div>
                <div class="metric-label">Shows in dataset</div>
              </div>
              <div class="metric-box">
                <div class="metric-value">{n_franchises}</div>
                <div class="metric-label">Franchises</div>
              </div>
              <div class="metric-box">
                <div class="metric-value">{success_rate:.0f}%</div>
                <div class="metric-label">Success rate</div>
              </div>
              <div class="metric-box">
                <div class="metric-value">{avg_rating:.1f}</div>
                <div class="metric-label">Avg IMDb</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # All shows list
            st.markdown(f'<div class="card-title" style="margin-top:0.5rem;">All {animal.upper()} shows in dataset</div>', unsafe_allow_html=True)
            shows_sorted = shows.sort_values('is_franchise_final', ascending=False)
            max_pop      = df_kids_franchise['netflix_popularity'].max()

            for _, row in shows_sorted.iterrows():
                is_f     = row['is_franchise_final'] == 1
                row_cls  = 'show-row-franchise' if is_f else 'show-row-regular'
                badge    = f'<span class="tag tag-gold" style="font-size:0.65rem;padding:0.1rem 0.4rem;">🏆 FRANCHISE</span>' if is_f else ''
                merch    = f'· {row["bought_last_month"]:,.0f} merch/mo' if is_f and pd.notna(row.get('bought_last_month')) and row.get('bought_last_month', 0) > 0 else ''
                pct      = row['netflix_popularity'] / max_pop * 100 if pd.notna(row.get('netflix_popularity')) and row.get('netflix_popularity', 0) > 0 else 0
                netflix_kpi = f'· Streaming reach: {pct:.0f}th percentile' if pct > 0 else ''

                st.markdown(f"""
                <div class="show-row {row_cls}">
                  <span class="show-title">{row['title']} {badge}</span>
                  <span class="show-rating">IMDb {row['averageRating']:.1f} {merch} {netflix_kpi}</span>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="padding:1rem 0;">
              <span class="tag tag-teal">✨ UNCHARTED TERRITORY</span>
              <p style="color:{TEXT_DIM};font-size:0.88rem;margin-top:0.8rem;">
                <b style="color:{TEXT_MAIN};">'{animal}'</b> has no precedent in 74 years of data.<br>
                No competition. No blueprint. You write the first data point.
              </p>
            </div>
            """, unsafe_allow_html=True)

        # Toy demand
        toy_hits = df_toys[df_toys['title'].str.contains(animal_lower, case=False, na=False)]
        st.markdown(f'<div class="card-title" style="margin-top:1rem;">🧸 Toy Market Demand</div>', unsafe_allow_html=True)

        if len(toy_hits) > 0:
            purchases = toy_hits['boughtInLastMonth'].sum()
            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-box">
                <div class="metric-value">{len(toy_hits):,}</div>
                <div class="metric-label">Products on Amazon</div>
              </div>
              <div class="metric-box">
                <div class="metric-value">{purchases:,.0f}</div>
                <div class="metric-label">Purchases/mo (Aug 2023)</div>
              </div>
              <div class="metric-box">
                <div class="metric-value">{toy_hits['stars'].mean():.1f}★</div>
                <div class="metric-label">Avg rating</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if matched_theme and matched_theme in opportunity['theme'].values:
                opp_row = opportunity[opportunity['theme'] == matched_theme].iloc[0]
                rank    = int((opportunity['opportunity_ratio'] > opp_row['opportunity_ratio']).sum() + 1)
                st.markdown(f"""
                <span class="tag">Opportunity ratio: {opp_row['opportunity_ratio']:,}</span>
                <span class="tag tag-teal">Market rank: #{rank} of {len(opportunity)} categories</span>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="color:{TEXT_DIM};font-size:0.85rem;">No toy listings found for <b>{animal}</b> in Amazon 2023 data.<br>Could be untapped market or low demand.</p>', unsafe_allow_html=True)

        # ── Comparable shows ─────────────────────────────────────────────
        st.markdown(f'<div class="card-title" style="margin-top:1rem;">🎯 Most Similar Shows in Dataset</div>', unsafe_allow_html=True)

        if matched_theme and matched_theme in df_kids_franchise['theme'].values:
            similar = df_kids_franchise[df_kids_franchise['theme'] == matched_theme].copy()
        else:
            # Fallback: same genre flag
            similar = df_kids_franchise.copy()

        # Filter by genre if possible
        genre_filter = concept.get('genre_adventure') or concept.get('genre_family')
        similar = similar.sort_values('is_franchise_final', ascending=False).head(5)

        for _, row in similar.iterrows():
            is_f    = row['is_franchise_final'] == 1
            row_cls = 'show-row-franchise' if is_f else 'show-row-regular'
            badge   = f'<span class="tag tag-gold" style="font-size:0.65rem;padding:0.1rem 0.4rem;">🏆</span>' if is_f else ''
            yt_info = ''
            if 'yt_top10_total_views' in row and row['yt_top10_total_views'] > 0:
                yt_info = f'· {row["yt_top10_total_views"]/1_000_000:.0f}M YT views'
            st.markdown(f"""
            <div class="show-row {row_cls}">
              <span class="show-title">{row['title']} {badge}</span>
              <span class="show-rating">IMDb {row['averageRating']:.1f} {yt_info}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ── Franchise Probability ─────────────────────────────────────────────
    with col_prob:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        with st.spinner("Running model..."):
            X_concept  = build_feature_vector(concept, feature_cols_clean, df_model)
            prob       = xgb_clean.predict_proba(X_concept)[0][1]
            all_probs  = xgb_clean.predict_proba(df_model[feature_cols_clean])[:,1]

        percentile = (all_probs < prob).mean() * 100
        baseline   = 0.087
        multiplier = prob / baseline

        if prob >= 0.30:
            prob_color   = "#00E676"
            verdict_text = "STRONG"
            verdict_cls  = "verdict-strong"
        elif prob >= 0.15:
            prob_color   = GOLD
            verdict_text = "MODERATE"
            verdict_cls  = "verdict-moderate"
        else:
            prob_color   = "#FF5252"
            verdict_text = "CHALLENGING"
            verdict_cls  = "verdict-weak"

        st.markdown(f"""
        <div class="card-title">🎯 Franchise Probability</div>
        <div class="prob-container">
          <div class="prob-number" style="color:{prob_color};">{prob*100:.1f}%</div>
          <div class="prob-label">FRANCHISE PROBABILITY</div>
          <div class="{verdict_cls}" style="margin-top:0.8rem;">{verdict_text}</div>
          <div style="color:{TEXT_DIM};font-size:0.82rem;margin-top:0.4rem;">
            Top {100-percentile:.0f}% of all shows in dataset<br>
            <b style="color:{GOLD};">{multiplier:.1f}x</b> above industry baseline (8.7%)
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Max probability ever seen in dataset for context
        max_prob = 50.0  # practical ceiling for new shows — optimized concepts top out ~48%
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number={'suffix': '%', 'font': {'color': prob_color, 'size': 28, 'family': 'Orbitron'}},
            gauge={
                'axis': {'range': [0, max_prob], 'tickcolor': TEXT_DIM,
                         'tickfont': {'color': TEXT_DIM, 'size': 10}},
                'bar':  {'color': prob_color, 'thickness': 0.25},
                'bgcolor': BG_INPUT,
                'bordercolor': '#333344',
                'steps': [
                    {'range': [0,          max_prob*0.35], 'color': 'rgba(255,82,82,0.13)'},
                    {'range': [max_prob*0.35, max_prob*0.65], 'color': 'rgba(255,214,0,0.13)'},
                    {'range': [max_prob*0.65, max_prob],   'color': 'rgba(0,230,118,0.13)'},
                ],
                'threshold': {
                    'line': {'color': MAGENTA, 'width': 2},
                    'thickness': 0.8,
                    'value': max_prob * 0.9
                }
            }
        ))        
        
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=220,
            margin=dict(l=20, r=20, t=10, b=10),
            font={'color': TEXT_DIM}
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f'<div style="text-align:center;font-size:0.72rem;color:{TEXT_DIM};">Scale: 0–{max_prob:.0f}% · real range for new shows · Magenta = top historical score</div>', unsafe_allow_html=True)
        if premise_tags:
            st.markdown(f'<div class="card-title" style="margin-top:1rem;">Premise signals</div>', unsafe_allow_html=True)
            for tag in premise_tags:
                boost = PREMISE_TO_GENRE.get(tag, {})
                genre_signal = list(boost.keys())[0].replace('genre_','').capitalize() if boost else '—'
                st.markdown(f'<span class="tag">{tag} → {genre_signal}</span>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 2: Sensitivity Analysis ───────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">📈 Sensitivity Analysis — What moves the needle?</div>', unsafe_allow_html=True)

    sensitivity_tests = [
        ('Add streaming',         {'on_streaming': 1, 'netflix_pop_filled': 45.0}),
        ('Remove streaming',      {'on_streaming': 0, 'netflix_pop_filled': 0.0}),
        ('Switch to Traditional', {'technique': 'Traditional'}),
        ('Switch to CGI',         {'technique': 'CGI'}),
        ('Switch to US',          {'country': 'United States'}),
        ('Switch to UK',          {'country': 'United Kingdom'}),
        ('Add Adventure genre',   {'genre_adventure': 1}),
        ('Remove Adventure',      {'genre_adventure': 0}),
        ('2-word title',          {'title_word_count': 2}),
        ('3-word title',          {'title_word_count': 3}),
        ('4-word title',          {'title_word_count': 4}),
        ('Add hero keyword',      {'title_has_hero_keyword': 1}) if not has_hero_kw else ('Remove hero keyword', {'title_has_hero_keyword': 0}),
    ]
    sensitivity_tests = [t for t in sensitivity_tests if t is not None]

    results = []
    for label, overrides in sensitivity_tests:
        test_vec = X_concept.copy()
        for k, v in overrides.items():
            if k in ['on_streaming','netflix_pop_filled','genre_adventure',
                     'genre_family','genre_comedy','genre_action',
                     'title_word_count','title_has_hero_keyword']:
                if k in feature_cols_clean:
                    test_vec[k] = v
            elif k == 'technique':
                for col in feature_cols_clean:
                    if col.startswith('technique_grouped_'):
                        test_vec[col] = 1 if col == f'technique_grouped_{v}' else 0
            elif k == 'country':
                for col in feature_cols_clean:
                    if col.startswith('country_grouped_'):
                        test_vec[col] = 1 if col == f'country_grouped_{v}' else 0
        test_prob = xgb_clean.predict_proba(test_vec)[0][1]
        delta     = test_prob - prob
        if abs(delta) > 0.02:
            results.append((label, test_prob, delta))

    results.sort(key=lambda x: abs(x[2]), reverse=True)

    if results:
        labels = [r[0] for r in results[:10]]
        deltas = [r[2]*100 for r in results[:10]]
        colors = [TURQUOISE if d > 0 else MAGENTA for d in deltas]

        fig_bar = go.Figure(go.Bar(
            x=deltas, y=labels, orientation='h',
            marker_color=colors,
            text=[f"{'+' if d>0 else ''}{d:.1f}%" for d in deltas],
            textposition='outside',
            textfont={'color': TEXT_MAIN, 'size': 11},
        ))
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=10, r=80, t=10, b=10),
            xaxis=dict(showgrid=False, zeroline=True,
                       zerolinecolor='rgba(255,255,255,0.13)',
                       tickcolor=TEXT_DIM, tickfont={'color':TEXT_DIM,'size':10},
                       ticksuffix='%'),
            yaxis=dict(tickfont={'color':TEXT_MAIN,'size':11}, autorange='reversed'),
            bargap=0.3,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.markdown(f'<p style="color:{TEXT_DIM};padding:1rem;">No single change moves the probability by more than 2%. Your concept is well balanced.</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-size:0.78rem;color:{TEXT_DIM};padding:0.4rem 0;">
      ℹ️  CGI scores higher in Streaming Era data — reflects post-2010 market reality.
      Historically, Traditional animation had a higher overall franchise conversion rate.
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ROW 3: Final Verdict ──────────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">🏆 Final Verdict</div>', unsafe_allow_html=True)

    improvements  = [r for r in results if r[2] > 0.02]
    risks         = [r for r in results if r[2] < -0.02]
    best_combo    = sorted(improvements, key=lambda x: x[1], reverse=True)[0] if improvements else None
    worst_combo   = sorted(risks,        key=lambda x: x[1])[0]               if risks        else None

    v1, v2, v3 = st.columns(3)

    with v1:
        st.markdown(f"""
        <div class="metric-box" style="text-align:left;padding:1.2rem;">
          <div class="card-title">Base Probability</div>
          <div style="font-family:Orbitron;font-size:2rem;color:{prob_color};">{prob*100:.1f}%</div>
          <div style="color:{TEXT_DIM};font-size:0.82rem;margin-top:0.4rem;">with your current inputs</div>
          <div style="color:{GOLD};font-size:0.78rem;margin-top:0.3rem;">{multiplier:.1f}x industry baseline</div>
        </div>
        """, unsafe_allow_html=True)

    with v2:
        if best_combo:
            st.markdown(f"""
            <div class="metric-box" style="text-align:left;padding:1.2rem;">
              <div class="card-title">Best Single Change</div>
              <div style="font-family:Orbitron;font-size:1.05rem;color:#00E676;">{best_combo[0]}</div>
              <div style="color:#00E676;font-size:1.4rem;font-weight:700;margin-top:0.3rem;">→ {best_combo[1]*100:.1f}%</div>
              {'<div style="color:#FF5252;font-size:0.75rem;margin-top:0.3rem;">⚠️ CGI scores higher in post-2010 data — Traditional had higher historical rate</div>' if best_combo[0] == "Switch to CGI" else ''}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-box" style="text-align:left;padding:1.2rem;">
              <div class="card-title">Best Single Change</div>
              <div style="color:#00E676;font-size:0.88rem;margin-top:0.6rem;">
                ✅ Your concept is already well optimized.<br>
                No single change improves probability by more than 2%.
              </div>
            </div>
            """, unsafe_allow_html=True)

    with v3:
        if worst_combo:
            st.markdown(f"""
            <div class="metric-box" style="text-align:left;padding:1.2rem;">
              <div class="card-title">Biggest Risk</div>
              <div style="font-family:Orbitron;font-size:1.05rem;color:#FF5252;">{worst_combo[0]}</div>
              <div style="color:#FF5252;font-size:1.4rem;font-weight:700;margin-top:0.3rem;">→ {worst_combo[1]*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-box" style="text-align:left;padding:1.2rem;">
              <div class="card-title">Biggest Risk</div>
              <div style="color:{TEXT_DIM};font-size:0.88rem;margin-top:0.6rem;">
                No single change drops probability significantly.
              </div>
            </div>
            """, unsafe_allow_html=True)


    # ── Market Gap Analysis ───────────────────────────────────────────────
    st.markdown(f"""
    <div class="card">
      <div class="card-title">📊 Market Gap Analysis</div>
      <div style="font-size:1rem;color:{TEXT_DIM};margin-bottom:0.6rem;">
        Based on your concept — here are the most relevant market opportunities.
        Consider these as alternative angles or complementary characters for your show.
      </div>
    """, unsafe_allow_html=True)

    top_gaps = opportunity.sort_values('opportunity_ratio', ascending=False).head(8).copy()

    for _, row in top_gaps.iterrows():
        cat        = row['theme'].upper()
        toys       = int(row['bought_last_month'])
        shows      = int(row['total_shows'])
        franchises = int(row['franchises'])
        ratio      = int(row['opportunity_ratio'])
        is_current = matched_theme and row['theme'] == matched_theme

        if ratio > 50000:
            status_color = '#FF5252'
            status_label = '🔥 UNDERSERVED'
        elif ratio > 15000:
            status_color = GOLD
            status_label = '⚠️ OPPORTUNITY'
        else:
            status_color = TEXT_DIM
            status_label = '✅ COMPETITIVE'

        highlight   = f'border:1px solid {TURQUOISE};background:rgba(0,188,212,0.08);' if is_current else 'border:1px solid transparent;'
        name_color  = TURQUOISE if is_current else TEXT_MAIN
        name_weight = '700' if is_current else '400'
        arrow       = ' ◀' if is_current else ''

        st.markdown(
            f'<div style="display:flex;align-items:center;padding:0.35rem 0.8rem;'
            f'border-radius:6px;margin:0.1rem 0;{highlight}">'
            f'<div style="width:110px;font-size:0.95rem;color:{name_color};font-weight:{name_weight};">{cat}{arrow}</div>'
            f'<div style="flex:1;font-size:0.9rem;color:{TEXT_DIM};">{shows} shows · {franchises} franchises</div>'
            f'<div style="width:130px;font-size:0.9rem;color:{TEXT_DIM};text-align:right;">{toys:,} toys/mo</div>'
            f'<div style="width:130px;text-align:right;font-size:0.9rem;font-weight:600;color:{status_color};">{status_label}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if shows > 0:
            cat_shows = df_kids_franchise[df_kids_franchise['theme'] == row['theme']].sort_values('is_franchise_final', ascending=False)
            with st.expander(f"  See {shows} {row['theme'].upper()} shows"):
                for _, s in cat_shows.iterrows():
                    is_f  = s['is_franchise_final'] == 1
                    badge = '🏆' if is_f else '·'
                    yt    = f" · {s['yt_top10_total_views']/1_000_000:.0f}M YT views" if 'yt_top10_total_views' in s and s['yt_top10_total_views'] > 0 else ''
                    color = GOLD if is_f else TEXT_DIM
                    st.markdown(
                        f'<div style="font-size:0.82rem;color:{color};padding:0.15rem 0;">'
                        f'{badge} {s["title"]} — IMDb {s["averageRating"]:.1f}{yt}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

    st.markdown(f"""
    <div style="margin-top:0.5rem;font-size:0.82rem;color:{TEXT_DIM};">
      Opportunity ratio = toy purchases/month ÷ (franchises + 1) · Higher = more demand, fewer dominant shows
    </div>
    </div>
    """, unsafe_allow_html=True)


    # ── Market status for current concept ────────────────────────────────
    if not matched_theme:
        st.markdown(f"""
        <div style="margin-top:1rem;padding:1rem;background:rgba(0,188,212,0.06);border-left:3px solid {TURQUOISE};border-radius:4px;">
          <b style="color:{TURQUOISE};">🌟 UNCHARTED TERRITORY</b><br>
          <span style="color:{TEXT_DIM};font-size:0.88rem;">
            No '{animal}' show has ever reached franchise status in 74 years of data.
            You would be writing the first data point.
          </span>
        </div>
        """, unsafe_allow_html=True)
    elif matched_theme and int(df_kids_franchise[df_kids_franchise['theme']==matched_theme]['is_franchise_final'].sum()) == 0:
        toy_total = df_toys[df_toys['title'].str.contains(animal_lower, case=False, na=False)]['boughtInLastMonth'].sum()
        n_tried   = len(df_kids_franchise[df_kids_franchise['theme']==matched_theme])
        st.markdown(f"""
        <div style="margin-top:1rem;padding:1rem;background:rgba(255,214,0,0.06);border-left:3px solid {GOLD};border-radius:4px;">
          <b style="color:{GOLD};">🎯 OPEN MARKET</b><br>
          <span style="color:{TEXT_DIM};font-size:0.88rem;">
            {n_tried} shows tried, 0 franchises.
            {f'{toy_total:,.0f} toy purchases/month with no dominant show.' if toy_total > 0 else ''}
            The category exists — nobody has owned it yet.
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:1rem;font-size:0.8rem;color:{TEXT_DIM};">
      ⚠️  The data is a map, not a guarantee. You still need a great idea and a great team.
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 2rem;color:{TEXT_DIM};">
      <div style="font-size:3rem;margin-bottom:1rem;">🎬</div>
      <div style="font-family:Orbitron;font-size:1rem;color:{TURQUOISE};letter-spacing:0.1em;">
        ENTER YOUR CONCEPT ABOVE AND HIT ANALYZE
      </div>
      <div style="font-size:0.88rem;margin-top:0.8rem;max-width:500px;margin-left:auto;margin-right:auto;line-height:1.6;">
        Combines 74 years of animated show data, Amazon toy demand signals,
        and an XGBoost model trained on 1,370 kids shows — including YouTube organic
        reach signal — to predict franchise potential.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="divider"></div>
<div class="footer">
  <div style="font-family:'Orbitron',monospace;font-size:1.1rem;color:{TEXT_MAIN};
              letter-spacing:0.12em;margin-bottom:0.6rem;">
    DAVID HERNÁNDEZ
  </div>
  <div style="margin-bottom:0.5rem;color:{TEXT_DIM};font-size:0.8rem;">
    Data Analytics Portfolio · 2026
  </div>
  <div style="display:flex;justify-content:center;gap:2rem;margin-bottom:0.8rem;">
    <a href="https://github.com/davherdel" target="_blank"
       style="color:{TURQUOISE};text-decoration:none;font-size:0.82rem;letter-spacing:0.05em;">
      ⌥ GitHub
    </a>
    <a href="https://www.linkedin.com/in/david-hernandez-cr-pt/" target="_blank"
       style="color:{TURQUOISE};text-decoration:none;font-size:0.82rem;letter-spacing:0.05em;">
      ↗ LinkedIn
    </a>
  </div>
  <div style="color:{TEXT_DIM};font-size:0.82rem;">
    Sources: IMDb (1948–2023) · Amazon Toys US (Aug 2023) · Netflix (2025) · YouTube Data API v3<br>
    <span style="font-size:0.88rem;color:#666688;">🔭 Roadmap: Regional toy sales data (Amazon EU/Asia) to reduce geographic bias · Live YouTube API search for real-time concept analysis
</span>
  </div>
</div>
""", unsafe_allow_html=True)
