"""
Portfolio Manager Pro - Application de gestion de portefeuille d'investissement
Page d'accueil avec onboarding intelligent et design moderne
"""

import streamlit as st
import pandas as pd
import os
from utils_categories import load_category_mapping, calculate_portfolio_metrics, format_currency, format_percentage

# Configuration de la page
st.set_page_config(
    page_title="Portfolio Manager Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/streamlit/streamlit',
        'Report a bug': "mailto:support@portfoliomanager.com",
        'About': "# Portfolio Manager Pro\nUne application complète de gestion de portefeuille d'investissement"
    }
)

# CSS moderne avec adaptation thème sombre/clair
st.markdown("""
<style>
    /* Variables CSS adaptatives */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --info-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --card-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
        --card-shadow-hover: 0 12px 48px rgba(102, 126, 234, 0.25);
        --border-radius: 15px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        
        /* Couleurs adaptatives */
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --text-primary: #2c3e50;
        --text-secondary: #6c757d;
        --border-color: rgba(102, 126, 234, 0.1);
        --card-bg: #ffffff;
    }

    /* Variables pour le mode sombre */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0e1117;
            --bg-secondary: #262730;
            --text-primary: #fafafa;
            --text-secondary: #a6a6a6;
            --border-color: rgba(102, 126, 234, 0.3);
            --card-bg: #1e1e1e;
            --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            --card-shadow-hover: 0 12px 48px rgba(0, 0, 0, 0.4);
        }
    }

    /* Assurer la visibilité du menu hamburger */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp > header [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    
    /* Menu hamburger toujours visible */
    [data-testid="stSidebar"] > div:first-child {
        visibility: visible !important;
    }
    
    button[title="View fullscreen"], 
    button[kind="header"] {
        visibility: visible !important;
        display: block !important;
    }

    /* Header principal */
    .main-header {
        background: var(--primary-gradient);
        padding: 3rem 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }

    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }

    /* Cards de fonctionnalités avec adaptation thème */
    .feature-card {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        transition: var(--transition);
        border: 1px solid var(--border-color);
        height: 100%;
        position: relative;
        overflow: hidden;
        color: var(--text-primary);
    }

    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--card-shadow-hover);
        border-color: rgba(102, 126, 234, 0.4);
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: var(--border-radius) var(--border-radius) 0 0;
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }

    .feature-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        text-align: center;
    }

    .feature-description {
        color: var(--text-secondary);
        text-align: center;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* Boutons modernes */
    .modern-button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        transition: var(--transition);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        cursor: pointer;
        width: 100%;
        text-align: center;
    }

    .modern-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        text-decoration: none;
        color: white;
    }

    /* Métriques du dashboard */
    .metric-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        text-align: center;
        border-left: 4px solid #667eea;
        color: var(--text-primary);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Statistiques de la base ETF */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .stat-item {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        text-align: center;
        transition: var(--transition);
        color: var(--text-primary);
    }

    .stat-item:hover {
        transform: translateY(-4px);
        box-shadow: var(--card-shadow-hover);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* Onboarding steps */
    .onboarding-step {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
        position: relative;
        color: var(--text-primary);
    }

    .step-number {
        position: absolute;
        top: -10px;
        left: 15px;
        background: #28a745;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9rem;
    }

    .step-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        margin-left: 20px;
    }

    .step-description {
        color: var(--text-secondary);
        margin-left: 20px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .feature-card {
            margin-bottom: 1rem;
        }
        
        .stats-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        }
    }

    /* Amélioration globale Streamlit */
    .stApp > header [data-testid="stHeader"] {
        background-color: var(--bg-secondary) !important;
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Sidebar avec design cohérent */
    .stSidebar > div:first-child {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    .stSidebar .stSelectbox label, .stSidebar .stRadio label {
        color: var(--text-primary) !important;
    }
    
    /* Container principal */
    .block-container {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        padding-top: 1rem;
    }
    
    /* Amélioration des éléments Streamlit */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Input fields adaptation */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_etf_data():
    """Charge les données ETF avec cache"""
    try:
        df = pd.read_excel('data/etf_base_assets.xlsx')
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données ETF: {e}")
        return pd.DataFrame()

def check_portfolio_exists():
    """Vérifie si un portefeuille existe déjà"""
    return 'portfolio' in st.session_state and not st.session_state.portfolio.empty

def get_etf_stats(df_etf):
    """Calcule les statistiques de la base ETF"""
    if df_etf.empty:
        return {}
    
    stats = {
        'total_etf': len(df_etf),
        'providers': df_etf['PROVIDER'].nunique() if 'PROVIDER' in df_etf.columns else 0,
        'brokers': 7,  # Nombre de courtiers supportés
        'avg_fees': df_etf['FRAIS DE GESTION'].mean() if 'FRAIS DE GESTION' in df_etf.columns else 0,
        'classes': 5   # Nombre de niveaux de classification
    }
    return stats

def main():
    """Fonction principale de la page d'accueil"""
    
    # Initialisation du session state
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = pd.DataFrame()
    
    if 'univers_etf' not in st.session_state:
        st.session_state.univers_etf = pd.DataFrame()
    
    # Chargement des données ETF
    df_etf = load_etf_data()
    etf_stats = get_etf_stats(df_etf)
    
    # Header principal avec animation
    st.markdown("""
    <div class="main-header">
        <h1>📊 Portfolio Manager Pro</h1>
        <p>Votre gestionnaire de portefeuille intelligent avec analyse ETF avancée</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Détection de l'état du portefeuille
    has_portfolio = check_portfolio_exists()
    
    if has_portfolio:
        # Dashboard exécutif pour utilisateurs existants
        st.markdown("## 🎯 Tableau de Bord Exécutif")
        
        portfolio_metrics = calculate_portfolio_metrics(st.session_state.portfolio)
        
        # Métriques en colonnes
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_currency(portfolio_metrics['valeur_totale'])}</div>
                <div class="metric-label">Valeur Totale</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_currency(portfolio_metrics['plus_value_totale'])}</div>
                <div class="metric-label">Plus-Value</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{format_percentage(portfolio_metrics['performance_globale'])}</div>
                <div class="metric-label">Performance</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{portfolio_metrics['nombre_actifs']}</div>
                <div class="metric-label">Actifs</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    else:
        # Onboarding pour nouveaux utilisateurs
        st.markdown("## 🚀 Bienvenue ! Commençons votre aventure d'investissement")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="onboarding-step">
                <div class="step-number">1</div>
                <div class="step-title">Découvrez notre base de données ETF</div>
                <div class="step-description">Explorez plus de 1900 ETF avec notre moteur de recherche avancé</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 Explorer les ETF", key="explore_etf", help="Découvrir la recherche ETF"):
                st.switch_page("pages/3_🔍_Recherche_ETF.py")
        
        with col2:
            st.markdown("""
            <div class="onboarding-step">
                <div class="step-number">2</div>
                <div class="step-title">Créez votre premier portefeuille</div>
                <div class="step-description">Commencez avec nos templates ou importez vos données existantes</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📂 Créer un Portfolio", key="create_portfolio", help="Aller à la gestion de portfolio"):
                st.switch_page("pages/2_📂_Gestion_Portfolio.py")
        
        st.markdown("---")
    
    # Section des fonctionnalités principales
    st.markdown("## 🛠️ Fonctionnalités Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Dashboard Portfolio</div>
            <div class="feature-description">
                Suivi en temps réel de vos investissements avec visualisations interactives et projections futures.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Accéder au Dashboard", key="dashboard", disabled=not has_portfolio):
            st.switch_page("pages/1_📈_Dashboard.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📂</div>
            <div class="feature-title">Gestion Portfolio</div>
            <div class="feature-description">
                Import/Export, création manuelle, templates intelligents pour gérer vos actifs facilement.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Gérer Portfolio", key="manage"):
            st.switch_page("pages/2_📂_Gestion_Portfolio.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Recherche ETF</div>
            <div class="feature-description">
                Moteur de recherche avancé avec filtrage multi-critères sur plus de 1900 ETF.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Rechercher ETF", key="search"):
            st.switch_page("pages/3_🔍_Recherche_ETF.py")
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧮</div>
            <div class="feature-title">Analyses Avancées</div>
            <div class="feature-description">
                Simulations, backtesting, optimisation de portefeuille et analyses sectorielles.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Analyses Avancées", key="analysis"):
            st.switch_page("pages/4_🧮_Analyses_Avancées.py")
    
    # Statistiques de la base de données
    if etf_stats:
        st.markdown("---")
        st.markdown("## 📊 Notre Base de Données ETF")
        
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-number">{etf_stats['total_etf']:,}</div>
                <div class="stat-label">ETF Disponibles</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{etf_stats['providers']}</div>
                <div class="stat-label">Providers</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{etf_stats['brokers']}</div>
                <div class="stat-label">Courtiers</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{etf_stats['avg_fees']:.2f}%</div>
                <div class="stat-label">Frais Moyens</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{etf_stats['classes']}</div>
                <div class="stat-label">Niveaux Classification</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer informationnel
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 💡 À Propos de Portfolio Manager Pro
        
        Cette application vous accompagne dans la gestion de vos investissements avec :
        - **Analyse ETF complète** : Plus de 1900 ETF analysés et classifiés
        - **Gestion multi-courtiers** : Support de 7 plateformes d'investissement
        - **Projections intelligentes** : Simulations basées sur les rendements attendus
        - **Interface intuitive** : Design moderne et expérience utilisateur optimisée
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Actions Rapides
        """)
        
        if has_portfolio:
            if st.button("📈 Voir Dashboard", key="quick_dashboard"):
                st.switch_page("pages/1_📈_Dashboard.py")
            
            if st.button("🔄 Mettre à jour les prix", key="quick_update"):
                st.switch_page("pages/2_📂_Gestion_Portfolio.py")
        else:
            if st.button("🚀 Template Portfolio", key="quick_template"):
                st.switch_page("pages/2_📂_Gestion_Portfolio.py")
            
            if st.button("🔍 Explorer ETF", key="quick_explore"):
                st.switch_page("pages/3_🔍_Recherche_ETF.py")

if __name__ == "__main__":
    main()