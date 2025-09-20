"""
Page de Recherche ETF - Filtrage avancé et affichage des résultats
Interface de recherche en 4 colonnes avec visualisation des ETF
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils_categories import (
    load_category_mapping, apply_category_mapping, get_unique_categories,
    get_brokers_info, get_broker_color, format_currency, format_percentage
)

# Configuration de la page
st.set_page_config(
    page_title="Recherche ETF - Portfolio Manager Pro",
    page_icon="🔍",
    layout="wide"
)

# CSS pour la page de recherche
st.markdown("""
<style>
    /* Variables CSS adaptatives */
    :root {
        --card-bg: #ffffff;
        --text-primary: #2c3e50;
        --text-secondary: #6c757d;
        --bg-secondary: #f8f9fa;
        --border-color: #dee2e6;
        --card-shadow: 0 4px 16px rgba(0,0,0,0.1);
        --card-shadow-hover: 0 8px 24px rgba(0,0,0,0.15);
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: #1e1e1e;
            --text-primary: #fafafa;
            --text-secondary: #a6a6a6;
            --bg-secondary: #262730;
            --border-color: rgba(102, 126, 234, 0.3);
            --card-shadow: 0 4px 16px rgba(0,0,0,0.3);
            --card-shadow-hover: 0 8px 24px rgba(0,0,0,0.4);
        }
    }

    /* Cards ETF */
    .etf-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: var(--card-shadow);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        color: var(--text-primary);
    }

    .etf-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--card-shadow-hover);
    }

    .etf-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 1rem;
    }

    .etf-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        flex: 1;
    }

    .etf-provider {
        background: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .etf-isin {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    .etf-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .badge {
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .badge-pea { background: #d4edda; color: #155724; }
    .badge-assurance { background: #cce7ff; color: #004085; }
    .badge-hedged { background: #fff3cd; color: #856404; }
    .badge-sfdr-8 { background: #d1ecf1; color: #0c5460; }
    .badge-sfdr-9 { background: #d4edda; color: #155724; }

    .etf-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .metric {
        text-align: center;
    }

    .metric-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .etf-classification {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }

    .classification-level {
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }

    .classification-label {
        font-weight: 600;
        color: var(--text-primary);
    }

    .broker-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .broker-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        color: white;
    }

    .broker-available { opacity: 1; }
    .broker-unavailable { opacity: 0.3; background: #6c757d !important; }

    /* Filtres */
    .filter-section {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: var(--card-shadow);
        margin-bottom: 2rem;
        color: var(--text-primary);
    }

    .filter-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Métriques de synthèse */
    .summary-metrics {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }

    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
    }

    .summary-item {
        text-align: center;
    }

    .summary-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .summary-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* Univers ETF */
    .univers-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
    }

    .univers-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .etf-header {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .etf-metrics {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .summary-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_etf_data():
    """Charge les données ETF avec cache"""
    try:
        df = pd.read_excel('data/etf_base_assets.xlsx')
        # Appliquer le mapping des catégories
        df = apply_category_mapping(df)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données ETF: {e}")
        return pd.DataFrame()

def filter_etf_data(df, filters):
    """Applique les filtres sur les données ETF"""
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Filtrage par catégorie principale (CLASSE 1)
    if filters['classe_1'] and filters['classe_1'] != 'Toutes':
        if 'CLASSE 1_LISIBLE' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['CLASSE 1_LISIBLE'] == filters['classe_1']]
        else:
            filtered_df = filtered_df[filtered_df['CLASSE 1'] == filters['classe_1']]
    
    # Filtrage par sous-catégorie (CLASSE 2)
    if filters['classe_2'] and filters['classe_2'] != 'Toutes':
        if 'CLASSE 2_LISIBLE' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['CLASSE 2_LISIBLE'] == filters['classe_2']]
        else:
            filtered_df = filtered_df[filtered_df['CLASSE 2'] == filters['classe_2']]
    
    # Filtrage par région (CLASSE 3)
    if filters['classe_3'] and filters['classe_3'] != 'Toutes':
        if 'CLASSE 3_LISIBLE' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['CLASSE 3_LISIBLE'] == filters['classe_3']]
        else:
            filtered_df = filtered_df[filtered_df['CLASSE 3'] == filters['classe_3']]
    
    # Filtrage par spécialisation (CLASSE 5)
    if filters['classe_5'] and filters['classe_5'] != 'Toutes':
        filtered_df = filtered_df[filtered_df['CLASSE 5'] == filters['classe_5']]
    
    # Filtrage par courtier
    if filters['broker'] and filters['broker'] != 'Tous':
        if filters['broker'] in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[filters['broker']] == True]
    
    # Filtrage par éligibilité PEA
    if filters['pea_eligible']:
        if 'PEA' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['PEA'] == 'Y']
    
    # Filtrage par assurance vie
    if filters['assurance_vie']:
        if 'ASSVIE' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['ASSVIE'] == 'Y']
    
    # Filtrage par protection change
    if filters['hedged']:
        if 'HEDGED' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['HEDGED'] == 'Y']
    
    # Filtrage par frais maximum
    if filters['max_fees'] < 2.0 and 'FRAIS DE GESTION' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['FRAIS DE GESTION'] <= filters['max_fees']]
    
    return filtered_df

def render_etf_card(etf_row):
    """Génère une card pour un ETF"""
    # Informations de base
    name = etf_row.get('NOM', 'N/A')
    isin = etf_row.get('ISIN', 'N/A')
    provider = etf_row.get('PROVIDER', 'N/A')
    
    # Métriques financières
    fees = etf_row.get('FRAIS DE GESTION', 0)
    encours = etf_row.get('ENCOURS SOUS GESTION (EUR)', 0)
    expected_return = etf_row.get('EXP_MACRO_RETURN', 0)
    
    # Éligibilités
    pea = etf_row.get('PEA', False)
    assvie = etf_row.get('ASSVIE', False)
    hedged = etf_row.get('HEDGED', False)
    sfdr = etf_row.get('SFDR', '')
    
    # Classification
    classe_1 = etf_row.get('CLASSE 1_LISIBLE', etf_row.get('CLASSE 1', 'N/A'))
    classe_2 = etf_row.get('CLASSE 2_LISIBLE', etf_row.get('CLASSE 2', 'N/A'))
    classe_3 = etf_row.get('CLASSE 3_LISIBLE', etf_row.get('CLASSE 3', 'N/A'))
    classe_4 = etf_row.get('CLASSE 4', 'N/A')
    classe_5 = etf_row.get('CLASSE 5', 'N/A')
    
    # Brokers
    brokers = ['XTB', 'ING', 'SCALABLE', 'EASYBOURSE', 'BOURSO', 'BOURSEDIRECT', 'ETORO']
    
    # Construction de la card
    badges_html = ""
    
    # Badges d'éligibilité
    if pea:
        badges_html += '<span class="badge badge-pea">PEA</span>'
    if assvie:
        badges_html += '<span class="badge badge-assurance">Assurance Vie</span>'
    if hedged:
        badges_html += '<span class="badge badge-hedged">Hedgé</span>'
    if sfdr == 'Article 8':
        badges_html += '<span class="badge badge-sfdr-8">SFDR Art. 8</span>'
    elif sfdr == 'Article 9':
        badges_html += '<span class="badge badge-sfdr-9">SFDR Art. 9</span>'
    
    # Métriques
    metrics_html = f"""
    <div class="etf-metrics">
        <div class="metric">
            <div class="metric-value">{fees:.2f}%</div>
            <div class="metric-label">Frais</div>
        </div>
        <div class="metric">
            <div class="metric-value">{encours:.0f}M€</div>
            <div class="metric-label">Encours</div>
        </div>
        <div class="metric">
            <div class="metric-value">{expected_return:.1f}%</div>
            <div class="metric-label">Rdt Espéré</div>
        </div>
    </div>
    """
    
    # Classification
    classification_html = f"""
    <div class="etf-classification">
        <div class="classification-level">
            <span class="classification-label">Type:</span> {classe_1}
        </div>
        <div class="classification-level">
            <span class="classification-label">Catégorie:</span> {classe_2}
        </div>
        <div class="classification-level">
            <span class="classification-label">Région:</span> {classe_3}
        </div>"""
    
    if classe_4 != 'N/A' and pd.notna(classe_4):
        classification_html += f"""
        <div class="classification-level">
            <span class="classification-label">Zone:</span> {classe_4}
        </div>"""
    
    if classe_5 != 'N/A' and pd.notna(classe_5):
        classification_html += f"""
        <div class="classification-level">
            <span class="classification-label">Spécialisation:</span> {classe_5}
        </div>"""
    
    classification_html += "</div>"
    
    # Badges des brokers
    broker_badges_html = ""
    for broker in brokers:
        if broker in etf_row and etf_row[broker]:
            color = get_broker_color(broker)
            broker_badges_html += f'<span class="broker-badge broker-available" style="background-color: {color};">{broker}</span>'
        else:
            broker_badges_html += f'<span class="broker-badge broker-unavailable">{broker}</span>'
    
    # Assemblage final
    card_html = f"""
    <div class="etf-card">
        <div class="etf-header">
            <h4 class="etf-name">{name}</h4>
            <div class="etf-provider">{provider}</div>
        </div>
        <div class="etf-isin">ISIN: {isin}</div>
        <div class="etf-badges">
            {badges_html}
        </div>
        {metrics_html}
        {classification_html}
        <div class="broker-badges">
            {broker_badges_html}
        </div>
    </div>
    """
    
    return card_html

def main():
    """Fonction principale de la page de recherche ETF"""
    
    st.title("🔍 Recherche ETF Avancée")
    st.markdown("Explorez notre base de données de plus de 1900 ETF avec des filtres intelligents")
    
    # Chargement des données
    df_etf = load_etf_data()
    
    if df_etf.empty:
        st.error("Impossible de charger les données ETF")
        return
    
    # Initialisation de l'univers ETF dans le session state
    if 'univers_etf' not in st.session_state:
        st.session_state.univers_etf = pd.DataFrame()
    
    # Interface de filtrage en 4 colonnes
    st.markdown("### 🎛️ Filtres de Recherche")
    
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        # Colonne 1: Type d'investissement
        with col1:
            st.markdown("""
            <div class="filter-section">
                <div class="filter-title">📊 Type d'investissement</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Catégorie principale (CLASSE 1)
            categories_1 = ['Toutes'] + get_unique_categories(df_etf, 'CLASSE 1')
            if 'CLASSE 1_LISIBLE' in df_etf.columns:
                categories_1_lisible = ['Toutes'] + sorted(df_etf['CLASSE 1_LISIBLE'].dropna().unique().tolist())
                selected_classe_1 = st.selectbox("Catégorie principale", categories_1_lisible)
            else:
                selected_classe_1 = st.selectbox("Catégorie principale", categories_1)
            
            # Sous-catégorie (CLASSE 2) - filtrage en cascade
            if selected_classe_1 != 'Toutes':
                if 'CLASSE 1_LISIBLE' in df_etf.columns:
                    filtered_classe_2 = df_etf[df_etf['CLASSE 1_LISIBLE'] == selected_classe_1]
                else:
                    filtered_classe_2 = df_etf[df_etf['CLASSE 1'] == selected_classe_1]
                
                if 'CLASSE 2_LISIBLE' in filtered_classe_2.columns:
                    categories_2 = ['Toutes'] + sorted(filtered_classe_2['CLASSE 2_LISIBLE'].dropna().unique().tolist())
                else:
                    categories_2 = ['Toutes'] + sorted(filtered_classe_2['CLASSE 2'].dropna().unique().tolist())
            else:
                if 'CLASSE 2_LISIBLE' in df_etf.columns:
                    categories_2 = ['Toutes'] + sorted(df_etf['CLASSE 2_LISIBLE'].dropna().unique().tolist())
                else:
                    categories_2 = ['Toutes'] + get_unique_categories(df_etf, 'CLASSE 2')
            
            selected_classe_2 = st.selectbox("Sous-catégorie", categories_2)
        
        # Colonne 2: Région
        with col2:
            st.markdown("""
            <div class="filter-section">
                <div class="filter-title">🌍 Région</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Région (CLASSE 3) avec explication
            col2_1, col2_2 = st.columns([4, 1])
            with col2_1:
                if 'CLASSE 3_LISIBLE' in df_etf.columns:
                    categories_3 = ['Toutes'] + sorted(df_etf['CLASSE 3_LISIBLE'].dropna().unique().tolist())
                else:
                    categories_3 = ['Toutes'] + get_unique_categories(df_etf, 'CLASSE 3')
                selected_classe_3 = st.selectbox("Région", categories_3)
            with col2_2:
                st.markdown("💡", help="Zone géographique principale d'investissement (Europe, États-Unis, Asie, etc.)")
            
            # Zone géographique (CLASSE 4) avec explication
            col2_3, col2_4 = st.columns([4, 1])
            with col2_3:
                if selected_classe_3 != 'Toutes':
                    if 'CLASSE 3_LISIBLE' in df_etf.columns:
                        filtered_classe_4 = df_etf[df_etf['CLASSE 3_LISIBLE'] == selected_classe_3]
                    else:
                        filtered_classe_4 = df_etf[df_etf['CLASSE 3'] == selected_classe_3]
                    categories_4 = ['Toutes'] + sorted(filtered_classe_4['CLASSE 4'].dropna().unique().tolist())
                else:
                    categories_4 = ['Toutes'] + get_unique_categories(df_etf, 'CLASSE 4')
                
                selected_classe_4 = st.selectbox("Zone géographique", categories_4)
            with col2_4:
                st.markdown("💡", help="Sous-région ou pays spécifique dans la région sélectionnée")
        
        # Colonne 3: Critères avancés
        with col3:
            st.markdown("""
            <div class="filter-section">
                <div class="filter-title">🎓 Critères avancés</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Spécialisation (CLASSE 5) avec explication
            col3_1, col3_2 = st.columns([4, 1])
            with col3_1:
                categories_5 = ['Toutes'] + get_unique_categories(df_etf, 'CLASSE 5')
                selected_classe_5 = st.selectbox("Spécialisation", categories_5)
            with col3_2:
                st.markdown("💡", help="Secteur ou thème spécifique (technologie, énergie, dividende, ESG, etc.)")
            
            # Courtier préféré avec explication
            col3_3, col3_4 = st.columns([4, 1])
            with col3_3:
                brokers = ['Tous', 'XTB', 'ING', 'SCALABLE', 'EASYBOURSE', 'BOURSO', 'BOURSEDIRECT', 'ETORO']
                selected_broker = st.selectbox("Courtier préféré", brokers)
            with col3_4:
                st.markdown("💡", help="Filtrer selon la disponibilité chez votre courtier en ligne")
        
        # Colonne 4: Critères pratiques
        with col4:
            st.markdown("""
            <div class="filter-section">
                <div class="filter-title">⚙️ Critères pratiques</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Éligibilités avec explications
            col4_1, col4_2 = st.columns([4, 1])
            with col4_1:
                pea_eligible = st.checkbox("Éligible PEA")
            with col4_2:
                st.markdown("💡", help="Plan d'Épargne en Actions : enveloppe fiscale française permettant d'investir en actions européennes avec avantages fiscaux après 5 ans")
            
            col4_3, col4_4 = st.columns([4, 1])
            with col4_3:
                assurance_vie = st.checkbox("Assurance vie")
            with col4_4:
                st.markdown("💡", help="ETF éligible aux contrats d'assurance-vie, enveloppe fiscale avec avantages après 8 ans")
            
            col4_5, col4_6 = st.columns([4, 1])
            with col4_5:
                hedged = st.checkbox("Protection change")
            with col4_6:
                st.markdown("💡", help="ETF avec couverture du risque de change pour réduire l'impact des fluctuations monétaires")
            
            # Frais maximum avec explication
            col4_7, col4_8 = st.columns([4, 1])
            with col4_7:
                max_fees = st.slider("Frais maximum (%)", 0.0, 2.0, 2.0, 0.1)
            with col4_8:
                st.markdown("💡", help="Frais de gestion annuels prélevés sur l'ETF. Plus ils sont bas, plus votre rendement net sera élevé")
    
    # Application des filtres
    filters = {
        'classe_1': selected_classe_1,
        'classe_2': selected_classe_2,
        'classe_3': selected_classe_3,
        'classe_5': selected_classe_5,
        'broker': selected_broker,
        'pea_eligible': pea_eligible,
        'assurance_vie': assurance_vie,
        'hedged': hedged,
        'max_fees': max_fees
    }
    
    # Filtrage des données
    filtered_df = filter_etf_data(df_etf, filters)
    
    # Métriques de synthèse (avant limitation pour afficher le vrai nombre d'ETF trouvés)
    if not filtered_df.empty:
        nb_etf = len(filtered_df)
        frais_moyen = filtered_df['FRAIS DE GESTION'].mean() if 'FRAIS DE GESTION' in filtered_df.columns else 0
        nb_pea = (filtered_df['PEA'] == 'Y').sum() if 'PEA' in filtered_df.columns else 0
        nb_hedged = (filtered_df['HEDGED'] == 'Y').sum() if 'HEDGED' in filtered_df.columns else 0
        
        # Limitation à 15 ETF triés par frais (après calcul des métriques)
        if 'FRAIS DE GESTION' in filtered_df.columns:
            filtered_df_display = filtered_df.sort_values('FRAIS DE GESTION').head(15)
        else:
            filtered_df_display = filtered_df.head(15)
        
        st.markdown(f"""
        <div class="summary-metrics">
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-value">{nb_etf}</div>
                    <div class="summary-label">ETF trouvés</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{frais_moyen:.2f}%</div>
                    <div class="summary-label">Frais moyens</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{nb_pea}</div>
                    <div class="summary-label">Éligibles PEA</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{nb_hedged}</div>
                    <div class="summary-label">Hedgés</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Affichage des résultats
    st.markdown("### 📋 Résultats de la Recherche")
    
    if filtered_df.empty:
        st.warning("Aucun ETF ne correspond à vos critères. Essayez d'assouplir les filtres.")
    else:
        # Bouton pour ajouter tous les ETF à l'univers
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("➕ Ajouter tous à l'univers", help="Ajouter tous les ETF trouvés à votre univers d'investissement"):
                # Ajouter les ETF à l'univers (tous les ETF trouvés, pas seulement les 15 affichés)
                new_etfs = filtered_df[['ISIN', 'NOM', 'PROVIDER']].copy()
                if st.session_state.univers_etf.empty:
                    st.session_state.univers_etf = new_etfs
                else:
                    # Éviter les doublons par ISIN
                    existing_isins = st.session_state.univers_etf['ISIN'].tolist() if 'ISIN' in st.session_state.univers_etf.columns else []
                    new_etfs = new_etfs[~new_etfs['ISIN'].isin(existing_isins)]
                    st.session_state.univers_etf = pd.concat([st.session_state.univers_etf, new_etfs], ignore_index=True)
                
                st.success(f"{len(new_etfs)} ETF ajoutés à votre univers !")
                st.rerun()
        
        # Cards des ETF (affichage limité à 15)
        for idx, etf_row in filtered_df_display.iterrows():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Afficher la card ETF
                card_html = render_etf_card(etf_row)
                st.markdown(card_html, unsafe_allow_html=True)
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("➕ Ajouter", key=f"add_{idx}", help="Ajouter à l'univers"):
                    # Ajouter cet ETF à l'univers
                    new_etf = pd.DataFrame([{
                        'ISIN': etf_row.get('ISIN', ''),
                        'NOM': etf_row.get('NOM', ''),
                        'PROVIDER': etf_row.get('PROVIDER', '')
                    }])
                    
                    if st.session_state.univers_etf.empty:
                        st.session_state.univers_etf = new_etf
                    else:
                        # Vérifier si déjà présent
                        if etf_row.get('ISIN', '') not in st.session_state.univers_etf['ISIN'].tolist():
                            st.session_state.univers_etf = pd.concat([st.session_state.univers_etf, new_etf], ignore_index=True)
                            st.success("ETF ajouté à l'univers !")
                        else:
                            st.warning("ETF déjà dans l'univers")
                    st.rerun()
    
    # Section Univers ETF
    if not st.session_state.univers_etf.empty:
        st.markdown("""
        <div class="univers-section">
            <h3 class="univers-title">🌟 Mon Univers d'Investissement</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.dataframe(
                st.session_state.univers_etf,
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.markdown(f"**{len(st.session_state.univers_etf)} ETF** dans l'univers")
            
            if st.button("🗑️ Vider l'univers", help="Supprimer tous les ETF de l'univers"):
                st.session_state.univers_etf = pd.DataFrame()
                st.success("Univers vidé !")
                st.rerun()
            
            # Export de l'univers
            if st.button("📥 Exporter l'univers", help="Télécharger l'univers en CSV"):
                csv = st.session_state.univers_etf.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Télécharger CSV",
                    data=csv,
                    file_name="univers_etf.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()