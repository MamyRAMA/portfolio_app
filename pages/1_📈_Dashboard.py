"""
Dashboard Portfolio - Suivi et analyse complète du portefeuille
Visualisations interactives, tableau de bord et projections
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from utils_categories import (
    calculate_portfolio_metrics, format_currency, format_percentage,
    calculate_expected_return, apply_category_mapping, get_drill_down_data
)

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Portfolio - Portfolio Manager Pro",
    page_icon="📈",
    layout="wide"
)

# CSS pour le dashboard avec adaptation thème
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
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: #1e1e1e;
            --text-primary: #fafafa;
            --text-secondary: #a6a6a6;
            --bg-secondary: #262730;
            --border-color: rgba(102, 126, 234, 0.3);
            --card-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }
    }

    /* Dashboard cards */
    .dashboard-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: var(--card-shadow);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        color: var(--text-primary);
    }

    .metric-big {
        text-align: center;
        padding: 1rem;
    }

    .metric-value-big {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .metric-label-big {
        color: var(--text-secondary);
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .positive { color: #28a745; }
    .negative { color: #dc3545; }
    .neutral { color: #6c757d; }

    /* Tableau portfolio */
    .portfolio-table {
        background: var(--card-bg);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: var(--card-shadow);
        color: var(--text-primary);
    }

    /* Section upload */
    .upload-section {
        background: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px dashed var(--border-color);
        text-align: center;
        color: var(--text-primary);
        margin: 1rem 0;
    }

    .upload-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #495057;
        margin-bottom: 1rem;
    }

    /* Projections */
    .projection-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }

    .projection-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        opacity: 0.9;
    }

    .projection-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .projection-subtitle {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    /* Actions rapides */
    .quick-actions {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }

    .quick-action-btn {
        background: #667eea;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }

    .quick-action-btn:hover {
        background: #764ba2;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Responsive */
    @media (max-width: 768px) {
        .metric-value-big {
            font-size: 2rem;
        }
        
        .quick-actions {
            flex-direction: column;
        }
        
        .quick-action-btn {
            width: 100%;
            text-align: center;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_etf_data():
    """Charge les données ETF avec cache"""
    try:
        df = pd.read_excel('data/etf_base_assets.xlsx')
        df = apply_category_mapping(df)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données ETF: {e}")
        return pd.DataFrame()

def create_portfolio_table(df_portfolio):
    """Crée le tableau du portefeuille avec formatage"""
    if df_portfolio.empty:
        return pd.DataFrame()
    
    # Colonnes à afficher
    display_columns = [
        'Type', 'Nom', 'ISIN', 'Quantité', 'Prix_Achat', 'Prix_Actuel',
        'Date_Achat', 'Valeur_Actuelle', 'Plus_Value', 'Performance_%'
    ]
    
    # Créer le tableau d'affichage
    df_display = df_portfolio.copy()
    
    # Assurer que toutes les colonnes existent
    for col in display_columns:
        if col not in df_display.columns:
            df_display[col] = 0 if col in ['Quantité', 'Prix_Achat', 'Prix_Actuel', 'Valeur_Actuelle', 'Plus_Value', 'Performance_%'] else ''
    
    # Formatage des colonnes
    df_display['Prix_Achat'] = df_display['Prix_Achat'].apply(lambda x: f"{x:.2f} €" if pd.notna(x) else "0,00 €")
    df_display['Prix_Actuel'] = df_display['Prix_Actuel'].apply(lambda x: f"{x:.2f} €" if pd.notna(x) else "0,00 €")
    df_display['Valeur_Actuelle'] = df_display['Valeur_Actuelle'].apply(lambda x: f"{x:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(x) else "0,00 €")
    df_display['Plus_Value'] = df_display['Plus_Value'].apply(lambda x: f"{x:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(x) else "0,00 €")
    df_display['Performance_%'] = df_display['Performance_%'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "0,0%")
    df_display['Quantité'] = df_display['Quantité'].apply(lambda x: f"{int(x)}" if pd.notna(x) else "0")
    
    return df_display[display_columns]

def create_repartition_chart(df_portfolio, theme='plotly'):
    """Crée le camembert de répartition du portefeuille"""
    if df_portfolio.empty:
        return go.Figure()
    
    # Calcul de la répartition par type
    if 'Type' not in df_portfolio.columns:
        df_portfolio['Type'] = 'ETF'
    
    repartition = df_portfolio.groupby('Type')['Valeur_Actuelle'].sum().reset_index()
    repartition['Percentage'] = (repartition['Valeur_Actuelle'] / repartition['Valeur_Actuelle'].sum()) * 100
    
    # Couleurs adaptatives selon le thème
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    
    fig = go.Figure(data=[go.Pie(
        labels=repartition['Type'],
        values=repartition['Valeur_Actuelle'],
        hole=0.4,
        textposition="inside",
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>" +
                      "Valeur: %{value:,.0f} €<br>" +
                      "Pourcentage: %{percent}<br>" +
                      "<extra></extra>",
        marker=dict(
            colors=colors,
            line=dict(color='white', width=2)
        )
    )])
    
    fig.update_layout(
        title={
            'text': "Répartition du Portefeuille par Type",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'weight': 'bold'}
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        margin=dict(t=50, b=50, l=50, r=50),
        height=400
    )
    
    return fig

def create_performance_chart(df_portfolio):
    """Crée le graphique de performance par actif"""
    if df_portfolio.empty or 'Performance_%' not in df_portfolio.columns:
        return go.Figure()
    
    # Données pour le graphique
    df_perf = df_portfolio.copy()
    df_perf = df_perf.sort_values('Performance_%', ascending=True)
    
    # Couleurs selon la performance
    colors = ['#dc3545' if x < 0 else '#28a745' for x in df_perf['Performance_%']]
    
    fig = go.Figure(data=[
        go.Bar(
            y=df_perf['Nom'],
            x=df_perf['Performance_%'],
            orientation='h',
            marker=dict(color=colors),
            text=[f"{x:.1f}%" for x in df_perf['Performance_%']],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>" +
                         "Performance: %{x:.1f}%<br>" +
                         "<extra></extra>"
        )
    ])
    
    # Ligne de performance moyenne
    avg_perf = df_perf['Performance_%'].mean()
    fig.add_vline(
        x=avg_perf,
        line_dash="dash",
        line_color="blue",
        annotation_text=f"Moyenne: {avg_perf:.1f}%",
        annotation_position="top"
    )
    
    fig.update_layout(
        title={
            'text': "Performance par Actif",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'weight': 'bold'}
        },
        xaxis_title="Performance (%)",
        yaxis_title="Actifs",
        height=max(400, len(df_perf) * 25),
        margin=dict(t=50, b=50, l=200, r=100)
    )
    
    return fig

def calculate_portfolio_weighted_return(df_portfolio, df_etf):
    """Calcule le rendement pondéré du portefeuille basé sur EXP_MACRO_RETURN"""
    if df_portfolio.empty:
        return 0.05  # 5% par défaut
    
    total_valeur = df_portfolio['Valeur_Actuelle'].sum()
    if total_valeur == 0:
        return 0.05
    
    rendement_pondere = 0
    valeur_mappee = 0
    
    # Calculer le rendement pour chaque actif mappé dans la base ETF
    for _, actif in df_portfolio.iterrows():
        poids = actif['Valeur_Actuelle'] / total_valeur
        
        if 'ISIN' in actif and not pd.isna(actif['ISIN']) and not df_etf.empty:
            etf_match = df_etf[df_etf['ISIN'] == actif['ISIN']]
            if not etf_match.empty and 'EXP_MACRO_RETURN' in etf_match.columns:
                rendement_etf = etf_match.iloc[0]['EXP_MACRO_RETURN']
                if pd.notna(rendement_etf):
                    rendement_pondere += (rendement_etf / 100) * poids
                    valeur_mappee += actif['Valeur_Actuelle']
                    continue
        
        # Si pas de mapping, utiliser rendement par défaut selon le type
        if actif.get('Type') == 'ETF':
            rendement_defaut = 0.06  # 6% pour ETF
        elif actif.get('Type') == 'Action':
            rendement_defaut = 0.08  # 8% pour actions
        elif actif.get('Type') == 'Obligation':
            rendement_defaut = 0.03  # 3% pour obligations
        else:
            rendement_defaut = 0.05  # 5% pour autres
        
        rendement_pondere += rendement_defaut * poids
    
    # Si aucun actif mappé, utiliser la moyenne pondérée des actifs mappés dans la base
    if valeur_mappee == 0 and not df_etf.empty and 'EXP_MACRO_RETURN' in df_etf.columns:
        rendements_valides = df_etf['EXP_MACRO_RETURN'].dropna()
        if not rendements_valides.empty:
            rendement_pondere = rendements_valides.mean() / 100
    
    return max(0.01, min(0.15, rendement_pondere))  # Borné entre 1% et 15%

def create_projection_chart(df_portfolio, df_etf, years_range, monthly_contribution=0):
    """Crée le graphique de projection d'évolution avec versements mensuels"""
    if df_portfolio.empty:
        return go.Figure()
    
    projections = []
    valeur_initiale = df_portfolio['Valeur_Actuelle'].sum()
    
    # Calcul du rendement moyen pondéré du portefeuille
    rendement_annuel = calculate_portfolio_weighted_return(df_portfolio, df_etf)
    
    for year in years_range:
        # Capital investi = valeur initiale + versements mensuels
        capital_investi = valeur_initiale + (monthly_contribution * 12 * year)
        
        # Calcul de la valeur avec capitalisation des intérêts composés
        # Capital initial réévalué
        valeur_future_initiale = valeur_initiale * ((1 + rendement_annuel) ** year)
        
        # Calcul des versements mensuels avec capitalisation (plus précis)
        if monthly_contribution > 0 and rendement_annuel > 0:
            # Rendement mensuel
            rendement_mensuel = (1 + rendement_annuel) ** (1/12) - 1
            # Formule FV des versements mensuels: PMT * [((1+r)^n - 1) / r]
            nombre_mois = year * 12
            valeur_future_versements = monthly_contribution * (((1 + rendement_mensuel) ** nombre_mois - 1) / rendement_mensuel)
            valeur_totale = valeur_future_initiale + valeur_future_versements
        elif monthly_contribution > 0:
            # Si rendement = 0, simple addition
            valeur_future_versements = monthly_contribution * 12 * year
            valeur_totale = valeur_future_initiale + valeur_future_versements
        else:
            valeur_totale = valeur_future_initiale
        
        plus_value = valeur_totale - capital_investi
        
        projections.append({
            'Année': year,
            'Capital_Investi': capital_investi,
            'Valeur_Totale': valeur_totale,
            'Plus_Value': plus_value
        })
    
    df_proj = pd.DataFrame(projections)
    
    fig = go.Figure()
    
    # Capital investi (montant cumulé des investissements)
    fig.add_trace(go.Scatter(
        x=df_proj['Année'],
        y=df_proj['Capital_Investi'],
        mode='lines+markers',
        name='Capital Investi',
        line=dict(color='#95a5a6', width=2, dash='dot'),
        marker=dict(size=6),
        hovertemplate="Année %{x}<br>Capital investi: %{y:,.0f} €<extra></extra>",
        fill=None
    ))
    
    # Valeur totale réévaluée
    fig.add_trace(go.Scatter(
        x=df_proj['Année'],
        y=df_proj['Valeur_Totale'],
        mode='lines+markers',
        name='Valeur Réévaluée',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8),
        hovertemplate="Année %{x}<br>Valeur réévaluée: %{y:,.0f} €<br>Plus-value: %{customdata:,.0f} €<extra></extra>",
        customdata=df_proj['Plus_Value'],
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    # Ligne de valeur actuelle
    fig.add_hline(
        y=valeur_initiale,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Valeur actuelle: {format_currency(valeur_initiale)}"
    )
    
    fig.update_layout(
        title={
            'text': f"Projection d'Évolution avec Versements Programmés<br><span style='font-size:12px;color:#666;'>Hypothèse de rendement: {rendement_annuel*100:.1f}% par an</span>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'weight': 'bold'}
        },
        xaxis_title="Années",
        yaxis_title="Valeur (€)",
        height=400,
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def process_price_update_file(uploaded_file, df_portfolio):
    """Traite le fichier de mise à jour des prix"""
    try:
        # Lire le fichier selon son extension
        if uploaded_file.name.endswith('.csv'):
            df_prices = pd.read_csv(uploaded_file, sep=';', encoding='utf-8-sig')
            if df_prices.shape[1] == 1:  # Essayer avec virgule
                uploaded_file.seek(0)
                df_prices = pd.read_csv(uploaded_file, sep=',', encoding='utf-8-sig')
        else:
            df_prices = pd.read_excel(uploaded_file)
        
        # Validation des colonnes
        required_cols = ['Nom', 'ISIN', 'Nouveau_Prix']
        if not all(col in df_prices.columns for col in required_cols):
            # Essayer des variantes de noms
            col_mapping = {
                'Nom': ['Nom', 'Name', 'NOM', 'NAME'],
                'ISIN': ['ISIN', 'isin'],
                'Nouveau_Prix': ['Nouveau_Prix', 'Prix', 'Price', 'Nouveau Prix', 'New_Price']
            }
            
            for standard_col, variants in col_mapping.items():
                for variant in variants:
                    if variant in df_prices.columns:
                        df_prices = df_prices.rename(columns={variant: standard_col})
                        break
        
        # Vérifier à nouveau
        missing_cols = [col for col in required_cols if col not in df_prices.columns]
        if missing_cols:
            return None, f"Colonnes manquantes: {missing_cols}"
        
        # Mise à jour des prix
        updates_count = 0
        for idx, row in df_prices.iterrows():
            # Recherche par ISIN en priorité
            mask = df_portfolio['ISIN'] == row['ISIN']
            if not mask.any():
                # Fallback sur le nom
                mask = df_portfolio['Nom'].str.contains(row['Nom'], case=False, na=False)
            
            if mask.any():
                df_portfolio.loc[mask, 'Prix_Actuel'] = row['Nouveau_Prix']
                updates_count += 1
        
        # Recalculer les métriques
        df_portfolio['Valeur_Actuelle'] = df_portfolio['Quantité'] * df_portfolio['Prix_Actuel']
        df_portfolio['Plus_Value'] = df_portfolio['Valeur_Actuelle'] - (df_portfolio['Quantité'] * df_portfolio['Prix_Achat'])
        df_portfolio['Performance_%'] = ((df_portfolio['Prix_Actuel'] - df_portfolio['Prix_Achat']) / df_portfolio['Prix_Achat']) * 100
        
        return df_portfolio, f"{updates_count} prix mis à jour avec succès"
        
    except Exception as e:
        return None, f"Erreur lors du traitement: {str(e)}"

def main():
    """Fonction principale du dashboard"""
    
    st.title("📈 Dashboard Portfolio")
    st.markdown("Suivi en temps réel de vos investissements")
    
    # Vérification de l'existence du portefeuille
    if 'portfolio' not in st.session_state or st.session_state.portfolio.empty:
        st.warning("Aucun portefeuille trouvé. Commencez par créer ou importer un portefeuille.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📂 Créer un Portfolio"):
                st.switch_page("pages/2_📂_Gestion_Portfolio.py")
        
        with col2:
            if st.button("🔍 Explorer les ETF"):
                st.switch_page("pages/3_🔍_Recherche_ETF.py")
        return
    
    # Chargement des données
    df_portfolio = st.session_state.portfolio.copy()
    df_etf = load_etf_data()
    
    # Calcul des métriques
    metrics = calculate_portfolio_metrics(df_portfolio)
    
    # Actions rapides
    st.markdown("""
    <div class="quick-actions">
        <span style="font-weight: 600; color: #495057; margin-right: 1rem;">Actions rapides:</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Mettre à jour les prix"):
            st.session_state.show_price_update = True
    with col2:
        if st.button("📊 Gérer Portfolio"):
            st.switch_page("pages/2_📂_Gestion_Portfolio.py")
    with col3:
        if st.button("🔍 Rechercher ETF"):
            st.switch_page("pages/3_🔍_Recherche_ETF.py")
    with col4:
        if st.button("📥 Exporter"):
            csv = df_portfolio.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name=f"portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Section de mise à jour des prix
    if st.session_state.get('show_price_update', False):
        st.markdown("---")
        st.markdown("### 🔄 Mise à Jour des Prix")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="upload-section">
                <div class="upload-title">📁 Upload Fichier de Prix</div>
                <p>Formats supportés: CSV, Excel<br>
                Colonnes requises: <strong>Nom, ISIN, Nouveau_Prix</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choisir un fichier",
                type=['csv', 'xlsx', 'xls'],
                help="Fichier avec colonnes: Nom, ISIN, Nouveau_Prix"
            )
            
            if uploaded_file:
                updated_portfolio, message = process_price_update_file(uploaded_file, df_portfolio.copy())
                
                if updated_portfolio is not None:
                    st.success(message)
                    st.session_state.portfolio = updated_portfolio
                    st.session_state.show_price_update = False
                    st.rerun()
                else:
                    st.error(message)
        
        with col2:
            st.markdown("**Template de mise à jour:**")
            template_df = pd.DataFrame({
                'Nom': ['ETF Example 1', 'ETF Example 2'],
                'ISIN': ['IE00B4L5Y983', 'IE00B5BMR087'],
                'Nouveau_Prix': [85.50, 412.30]
            })
            
            csv_template = template_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Télécharger Template",
                data=csv_template,
                file_name="template_prix.csv",
                mime="text/csv"
            )
            
            if st.button("❌ Annuler"):
                st.session_state.show_price_update = False
                st.rerun()
    
    st.markdown("---")
    
    # Métriques principales
    st.markdown("### 🎯 Vue d'Ensemble")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        performance_color = "positive" if metrics['performance_globale'] >= 0 else "negative"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-big">
                <div class="metric-value-big">{format_currency(metrics['valeur_totale'])}</div>
                <div class="metric-label-big">Valeur Totale</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pv_color = "positive" if metrics['plus_value_totale'] >= 0 else "negative"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-big">
                <div class="metric-value-big {pv_color}">{format_currency(metrics['plus_value_totale'])}</div>
                <div class="metric-label-big">Plus-Value</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        perf_color = "positive" if metrics['performance_globale'] >= 0 else "negative"
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-big">
                <div class="metric-value-big {perf_color}">{format_percentage(metrics['performance_globale'])}</div>
                <div class="metric-label-big">Performance</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-big">
                <div class="metric-value-big">{metrics['nombre_actifs']}</div>
                <div class="metric-label-big">Actifs</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tableau détaillé du portefeuille
    st.markdown("### 📊 Détail du Portefeuille")
    
    df_display = create_portfolio_table(df_portfolio)
    if not df_display.empty:
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Ligne de total
        total_valeur = df_portfolio['Valeur_Actuelle'].sum()
        total_pv = df_portfolio['Plus_Value'].sum()
        total_perf = (total_pv / (total_valeur - total_pv)) * 100 if (total_valeur - total_pv) > 0 else 0
        
        st.markdown(f"""
        **TOTAL:** Valeur: {format_currency(total_valeur)} | Plus-Value: {format_currency(total_pv)} | Performance: {total_perf:.1f}%
        """)
    
    # Visualisations
    st.markdown("### 📈 Visualisations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Camembert de répartition
        fig_pie = create_repartition_chart(df_portfolio)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Graphique de performance
        fig_perf = create_performance_chart(df_portfolio)
        st.plotly_chart(fig_perf, use_container_width=True)
    
    # Projections d'évolution avec versements programmés
    st.markdown("### 🔮 Projections d'Évolution et Versements Programmés")
    
    # Paramètres de simulation
    st.markdown("#### ⚙️ Paramètres de Simulation")
    col1, col2 = st.columns(2)
    
    with col1:
        custom_years = st.slider("Horizon d'investissement (années)", 1, 40, 15, help="Durée de la projection d'investissement")
    
    with col2:
        monthly_contribution = st.number_input(
            "Versement mensuel (€)",
            min_value=0,
            value=500,
            step=50,
            help="Montant investi chaque mois en plus du capital initial"
        )
    
    # Graphique de projection avec paramètres dynamiques
    years_range = range(1, custom_years + 1)
    fig_proj = create_projection_chart(df_portfolio, df_etf, years_range, monthly_contribution)
    st.plotly_chart(fig_proj, use_container_width=True)
    
    # Métriques de projection pour différents horizons
    st.markdown("#### 📊 Projections Clés")
    
    col1, col2, col3 = st.columns(3)
    horizons = [5, 10, 20]  # Horizons fixes comme demandé
    
    # Calcul du rendement pondéré cohérent avec le graphique
    valeur_initiale = metrics['valeur_totale']
    rendement_annuel_projections = calculate_portfolio_weighted_return(df_portfolio, df_etf)
    
    for i, horizon in enumerate(horizons):
        # Calculs avec versements mensuels
        capital_investi = valeur_initiale + (monthly_contribution * 12 * horizon)
        
        # Capital initial réévalué
        valeur_future_initiale = valeur_initiale * ((1 + rendement_annuel_projections) ** horizon)
        
        if monthly_contribution > 0 and rendement_annuel_projections > 0:
            # Rendement mensuel pour calcul précis
            rendement_mensuel = (1 + rendement_annuel_projections) ** (1/12) - 1
            nombre_mois = horizon * 12
            valeur_future_versements = monthly_contribution * (((1 + rendement_mensuel) ** nombre_mois - 1) / rendement_mensuel)
            valeur_totale_future = valeur_future_initiale + valeur_future_versements
        elif monthly_contribution > 0:
            valeur_future_versements = monthly_contribution * 12 * horizon
            valeur_totale_future = valeur_future_initiale + valeur_future_versements
        else:
            valeur_totale_future = valeur_future_initiale
        
        plus_value_future = valeur_totale_future - capital_investi
        
        with [col1, col2, col3][i]:
            # Couleur selon l'horizon
            gradient_colors = [
                "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
                "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"
            ]
            
            st.markdown(f"""
            <div style="background: {gradient_colors[i]}; color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                <div style="font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem; opacity: 0.9;">
                    Horizon {horizon} ans
                </div>
                <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">
                    {format_currency(valeur_totale_future)}
                </div>
                <div style="font-size: 0.9rem; opacity: 0.8;">
                    Capital investi: {format_currency(capital_investi)}<br>
                    Plus-value: {format_currency(plus_value_future)}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Résumé détaillé de la projection personnalisée
    st.markdown("#### 📈 Détails de votre Projection")
    
    # Calculs pour l'horizon personnalisé
    capital_investi_custom = valeur_initiale + (monthly_contribution * 12 * custom_years)
    
    # Capital initial réévalué
    valeur_future_initiale_custom = valeur_initiale * ((1 + rendement_annuel_projections) ** custom_years)
    
    if monthly_contribution > 0 and rendement_annuel_projections > 0:
        # Calcul précis avec capitalisation mensuelle
        rendement_mensuel = (1 + rendement_annuel_projections) ** (1/12) - 1
        nombre_mois = custom_years * 12
        valeur_future_versements_custom = monthly_contribution * (((1 + rendement_mensuel) ** nombre_mois - 1) / rendement_mensuel)
        valeur_totale_future_custom = valeur_future_initiale_custom + valeur_future_versements_custom
    elif monthly_contribution > 0:
        valeur_future_versements_custom = monthly_contribution * 12 * custom_years
        valeur_totale_future_custom = valeur_future_initiale_custom + valeur_future_versements_custom
    else:
        valeur_totale_future_custom = valeur_future_initiale_custom
        valeur_future_versements_custom = 0
    
    plus_value_future_custom = valeur_totale_future_custom - capital_investi_custom
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Composition du Patrimoine Futur**")
        
        # Capital initial réévalué avec tooltip
        col1_1, col1_2 = st.columns([3, 1])
        with col1_1:
            st.metric("Capital Initial Réévalué", format_currency(valeur_future_initiale_custom))
        with col1_2:
            st.markdown("💡", help="Valeur future de votre capital actuel avec les intérêts composés")
        
        if monthly_contribution > 0:
            # Valeur future des versements avec tooltip
            col1_3, col1_4 = st.columns([3, 1])
            with col1_3:
                st.metric("Valeur Future des Versements", format_currency(valeur_future_versements_custom))
            with col1_4:
                st.markdown("💡", help="Valeur future de vos versements mensuels avec capitalisation des intérêts")
            
            # Montant total versé avec tooltip
            col1_5, col1_6 = st.columns([3, 1])
            with col1_5:
                st.metric("Montant Total Versé", format_currency(monthly_contribution * 12 * custom_years))
            with col1_6:
                st.markdown("💡", help="Somme brute de tous vos versements mensuels (sans intérêts)")
    
    with col2:
        st.markdown("**🎯 Performance Projetée**")
        
        # Multiplicateur du capital initial seulement (plus logique)
        multiplicateur_capital_initial = valeur_future_initiale_custom / valeur_initiale if valeur_initiale > 0 else 0
        taux_rendement_global = ((valeur_totale_future_custom / capital_investi_custom) ** (1/custom_years) - 1) * 100 if capital_investi_custom > 0 else 0
        
        # Multiplicateur avec tooltip
        col2_1, col2_2 = st.columns([3, 1])
        with col2_1:
            st.metric("Multiplicateur Capital Initial", f"{multiplicateur_capital_initial:.1f}x")
        with col2_2:
            st.markdown("💡", help="Combien de fois votre capital initial sera multiplié (hors versements)")
        
        # Taux de rendement avec tooltip
        col2_3, col2_4 = st.columns([3, 1])
        with col2_3:
            st.metric("Taux de Rendement Global", f"{taux_rendement_global:.1f}% / an")
        with col2_4:
            st.markdown("💡", help="Rendement annuel moyen sur l'ensemble (capital + versements)")
        
        # Rentabilité avec tooltip
        col2_5, col2_6 = st.columns([3, 1])
        with col2_5:
            st.metric("Rentabilité Totale", f"{(plus_value_future_custom/capital_investi_custom)*100:.0f}%")
        with col2_6:
            st.markdown("💡", help="Pourcentage de gain total par rapport au montant investi")
    
    # Informations sur les hypothèses
    st.info(f"""
    **💡 Hypothèses de calcul :**
    - Rendement moyen pondéré du portefeuille : **{rendement_annuel_projections*100:.1f}% par an**
    - Versements mensuels : **{format_currency(monthly_contribution)}** (capitalisation annuelle)
    - Reinvestissement automatique des dividendes
    - Frais de gestion déjà intégrés dans les rendements ETF
    - Projection basée sur les rendements macro attendus (EXP_MACRO_RETURN) de chaque actif
    """)
    
    if monthly_contribution > 0:
        st.success(f"""
        💰 **Impact des versements programmés :**
        En ajoutant {format_currency(monthly_contribution)} par mois pendant {custom_years} ans, vous investirez 
        {format_currency(monthly_contribution * 12 * custom_years)} supplémentaires qui généreront 
        {format_currency(valeur_future_versements_custom - monthly_contribution * 12 * custom_years)} de plus-value !
        """)

if __name__ == "__main__":
    # Initialisation du session state
    if 'show_price_update' not in st.session_state:
        st.session_state.show_price_update = False
    
    main()