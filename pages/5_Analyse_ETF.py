"""
Analyse ETF - MVP
Interface pour analyser la performance et les caractéristiques d'un ETF spécifique
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from utils_data import load_etf_data, format_currency

# Configuration de la page
st.set_page_config(
    page_title="Analyse ETF",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_etf_prices():
    """Charge les prix des ETFs depuis le fichier Excel"""
    try:
        prices_df = pd.read_excel("data/etf_prices_extended.xlsx", index_col=0, parse_dates=True)
        prices_df.index = pd.to_datetime(prices_df.index)
        return prices_df
    except Exception as e:
        st.error(f"Erreur lors du chargement des prix: {e}")
        return pd.DataFrame()

def calculate_performance_metrics(prices):
    """Calcule les métriques de performance"""
    if prices.empty or len(prices) < 2:
        return {}
    
    # Rendements
    returns = prices.pct_change().dropna()
    
    # Performance cumulée
    cum_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
    
    # Rendement annualisé
    years = len(prices) / 52  # Approximation jours de trading
    annualized_return = ((prices.iloc[-1] / prices.iloc[0]) ** (1/years) - 1) * 100 if years > 0 else 0
    
    # Volatilité annualisée
    volatility = returns.std() * np.sqrt(52) * 100
    
    # Ratio de Sharpe (en supposant taux sans risque = 1%)
    risk_free_rate = 1
    sharpe = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
    
    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.expanding().max()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100
    
    return {
        'cum_return': cum_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown,
        'returns': returns,
        'cumulative': cumulative
    }

def get_sfdr_info(sfdr_value):
    """Retourne les informations sur la classification SFDR"""
    if pd.isna(sfdr_value) or sfdr_value == '-':
        return "N/A", "⚫", "Pas de classification SFDR"
    
    sfdr_value = str(sfdr_value)
    
    if sfdr_value == "6":
        return "Article 6", "🔵", "Pas d'objectifs durables spécifiques"
    elif sfdr_value == "8":
        return "Article 8", "🟢", "Favorise des caractéristiques environnementales/sociales"
    elif sfdr_value == "9":
        return "Article 9", "🟩", "Objectif d'investissement durable"
    else:
        return f"Article {sfdr_value}", "⚫", "Classification SFDR spécifique"

def create_styled_badge(label, value, color="blue", icon=""):
    """Crée un badge stylé avec Streamlit"""
    if color == "green":
        bg_color = "#d4edda"
        text_color = "#155724"
        border_color = "#c3e6cb"
    elif color == "red":
        bg_color = "#f8d7da"
        text_color = "#721c24"
        border_color = "#f5c6cb"
    elif color == "orange":
        bg_color = "#fff3cd"
        text_color = "#856404"
        border_color = "#ffeaa7"
    elif color == "purple":
        bg_color = "#e2e3ff"
        text_color = "#383874"
        border_color = "#c5c6ff"
    else:  # blue par défaut
        bg_color = "#d1ecf1"
        text_color = "#0c5460"
        border_color = "#bee5eb"
    
    badge_html = f"""
    <div style="
        display: inline-block;
        padding: 8px 12px;
        margin: 4px;
        background-color: {bg_color};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
    ">
        {icon} <strong>{label}:</strong> {value}
    </div>
    """
    return badge_html

def create_performance_chart(prices, etf_name, interactive=False):
    """Crée un graphique de performance"""
    if prices.empty:
        return None
    
    # Normaliser à 100
    normalized_prices = (prices / prices.iloc[0]) * 100
    
    if interactive:
        # Version Plotly interactive
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=normalized_prices.index,
            y=normalized_prices.values,
            mode='lines',
            name=etf_name,
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>Date:</b> %{x}<br><b>Performance:</b> %{y:.2f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Performance de {etf_name} (Base 100)",
            xaxis_title="Date",
            yaxis_title="Performance (%)",
            hovermode='x unified',
            height=500,
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    else:
        # Version Streamlit native
        df_chart = pd.DataFrame({
            'Performance (%)': normalized_prices.values
        }, index=normalized_prices.index)
        
        return df_chart

# Titre principal
st.title("📈 Analyse ETF")

# Charger les données
etf_data = load_etf_data()
etf_prices = load_etf_prices()

if etf_data.empty:
    st.error("❌ Impossible de charger les données ETF")
    st.stop()

# Vérifier l'univers ETF dans session_state
if 'univers_etf' not in st.session_state:
    st.session_state.univers_etf = []

# Sélection de l'ETF
st.subheader("🎯 Sélection de l'ETF")

# Choix du mode de sélection
col_mode1, col_mode2 = st.columns(2)

with col_mode1:
    use_univers = st.radio(
        "Mode de sélection:",
        ["Univers d'investissement", "Recherche manuelle"],
        help="Choisissez comment sélectionner l'ETF à analyser"
    )

if use_univers == "Univers d'investissement":
    # Mode univers d'investissement
    if st.session_state.univers_etf:
        available_etfs = etf_data[etf_data['ISIN'].isin(st.session_state.univers_etf)]
        st.info(f"🎯 Sélection dans votre univers d'investissement ({len(available_etfs)} ETFs)")
        
        # Créer la liste des options avec nom + ISIN
        etf_options = []
        for _, row in available_etfs.iterrows():
            etf_name = row.get('NOM', 'Nom non disponible')
            etf_isin = row.get('ISIN', 'ISIN non disponible')
            etf_options.append(f"{etf_name} ({etf_isin})")

        selected_etf_display = st.selectbox(
            "Choisissez un ETF de votre univers:",
            etf_options,
            help="Sélectionnez l'ETF que vous souhaitez analyser en détail"
        )
    else:
        st.warning("Votre univers d'investissement est vide. Utilisez la page Recherche ETF pour le créer ou passez en mode recherche manuelle.")
        st.stop()
        
else:
    # Mode recherche manuelle
    with col_mode2:
        search_term = st.text_input(
            "Recherche rapide:",
            placeholder="Tapez le nom, ISIN ou fournisseur...",
            help="Recherchez un ETF par nom, ISIN ou fournisseur"
        )
    
    # Filtrer les ETFs selon la recherche
    if search_term:
        mask = (
            etf_data['NOM'].str.contains(search_term, case=False, na=False) |
            etf_data['ISIN'].str.contains(search_term, case=False, na=False) |
            etf_data['PROVIDER'].str.contains(search_term, case=False, na=False)
        )
        available_etfs = etf_data[mask]
        
        if len(available_etfs) > 0:
            st.info(f"🔍 {len(available_etfs)} ETF(s) trouvé(s) pour '{search_term}'")
            
            # Créer la liste des options avec nom + ISIN
            etf_options = []
            for _, row in available_etfs.iterrows():
                etf_name = row.get('NOM', 'Nom non disponible')
                etf_isin = row.get('ISIN', 'ISIN non disponible')
                etf_provider = row.get('PROVIDER', 'N/A')
                etf_options.append(f"{etf_name} ({etf_isin}) - {etf_provider}")

            selected_etf_display = st.selectbox(
                "Sélectionnez l'ETF à analyser:",
                etf_options,
                help="Choisissez parmi les résultats de recherche"
            )
        else:
            st.warning(f"Aucun ETF trouvé pour '{search_term}'. Essayez avec d'autres termes.")
            st.stop()
    else:
        st.info("💡 Tapez quelques lettres dans la barre de recherche pour commencer")
        st.stop()

if selected_etf_display:
    # Extraire l'ISIN de la sélection selon le mode
    if use_univers == "Univers d'investissement":
        # Format: "Nom (ISIN)"
        selected_isin = selected_etf_display.split('(')[-1].replace(')', '')
    else:
        # Format: "Nom (ISIN) - Provider"
        parts = selected_etf_display.split('(')[1].split(')')
        selected_isin = parts[0]
    
    selected_etf_row = available_etfs[available_etfs['ISIN'] == selected_isin].iloc[0]
    
    # Section des caractéristiques
    st.subheader("📋 Caractéristiques de l'ETF")
    
    # Informations générales avec badges stylés
    st.markdown("### 🏷️ Informations générales")
    
    badges_html = ""
    badges_html += create_styled_badge("Nom", selected_etf_row.get('NOM', 'N/A'), "blue", "🏷️")
    badges_html += create_styled_badge("ISIN", selected_etf_row.get('ISIN', 'N/A'), "blue", "🔢")
    badges_html += create_styled_badge("Fournisseur", selected_etf_row.get('PROVIDER', 'N/A'), "purple", "🏢")
    badges_html += create_styled_badge("Devise", selected_etf_row.get('DEVISE ETF', 'N/A'), "blue", "💱")
    
    # Frais de gestion
    frais = selected_etf_row.get('FRAIS DE GESTION', 'N/A')
    if frais != 'N/A' and pd.notna(frais):
        try:
            frais_num = float(frais)
            badges_html += create_styled_badge("Frais de gestion", f"{frais_num:.2f}%", "orange", "💰")
        except:
            badges_html += create_styled_badge("Frais de gestion", str(frais), "orange", "💰")
    else:
        badges_html += create_styled_badge("Frais de gestion", "N/A", "orange", "💰")
    
    st.markdown(badges_html, unsafe_allow_html=True)
    
    # Classification
    st.markdown("### 📊 Classification")
    
    class_badges_html = ""
    class_badges_html += create_styled_badge("Classe 1", selected_etf_row.get('CLASSE 1', 'N/A'), "blue", "📊")
    class_badges_html += create_styled_badge("Classe 2", selected_etf_row.get('CLASSE 2', 'N/A'), "blue", "📈")
    class_badges_html += create_styled_badge("Classe 3", selected_etf_row.get('CLASSE 3', 'N/A'), "blue", "📉")
    
    # Encours
    encours = selected_etf_row.get('ENCOURS SOUS GESTION (EUR)', 'N/A')
    if encours != 'N/A' and pd.notna(encours):
        try:
            encours_num = float(encours)
            class_badges_html += create_styled_badge("Encours (mn)", format_currency(encours_num), "purple", "💼")
        except:
            class_badges_html += create_styled_badge("Encours mn)", str(encours), "purple", "💼")
    else:
        class_badges_html += create_styled_badge("Encours (mn)", "N/A", "purple", "💼")
    
    st.markdown(class_badges_html, unsafe_allow_html=True)
    
    # Classification SFDR
    st.markdown("### � Classification SFDR")
    
    sfdr_value = selected_etf_row.get('SFDR', 'N/A')
    sfdr_label, sfdr_icon, sfdr_description = get_sfdr_info(sfdr_value)
    
    sfdr_color = "green" if sfdr_value in ['8', '9'] else "blue"
    sfdr_badge_html = create_styled_badge("SFDR", sfdr_label, sfdr_color, sfdr_icon)
    st.markdown(sfdr_badge_html, unsafe_allow_html=True)
    
    if sfdr_value in ['8', '9']:
        st.success(f"🌱 **ETF Durable:** {sfdr_description}")
    elif sfdr_value == '6':
        st.info(f"ℹ️ **ETF Standard:** {sfdr_description}")
    else:
        st.info(f"ℹ️ {sfdr_description}")
    
    # Caractéristiques spéciales
    st.markdown("### 🎯 Éligibilités et caractéristiques")
    
    special_badges_html = ""
    
    # PEA
    pea_eligible = selected_etf_row.get('PEA', 'N')
    pea_color = "green" if pea_eligible == 'Y' else "red"
    pea_text = "Éligible" if pea_eligible == 'Y' else "Non éligible"
    special_badges_html += create_styled_badge("PEA", pea_text, pea_color, "🇫🇷")
    
    # Assurance Vie
    assvie_eligible = selected_etf_row.get('ASSVIE', 'N')
    assvie_color = "green" if assvie_eligible == 'Y' else "red"
    assvie_text = "Éligible" if assvie_eligible == 'Y' else "Non éligible"
    special_badges_html += create_styled_badge("Assurance Vie", assvie_text, assvie_color, "🛡️")
    
    # Couverture de change
    hedged = selected_etf_row.get('HEDGED', 'N')
    hedged_color = "blue" if hedged == 'Y' else "orange"
    hedged_text = "Couvert" if hedged == 'Y' else "Non couvert"
    special_badges_html += create_styled_badge("Couverture change", hedged_text, hedged_color, "�")
    
    st.markdown(special_badges_html, unsafe_allow_html=True)
    
    # Section Performance
    st.subheader("📈 Analyse de Performance")
    
    # Vérifier si on a des données de prix pour cet ETF
    if not etf_prices.empty and selected_isin in etf_prices.columns:
        etf_price_series = etf_prices[selected_isin].dropna()
        
        if len(etf_price_series) > 1:
            # Calculer les métriques
            metrics = calculate_performance_metrics(etf_price_series)
            
            # Afficher les métriques
            st.markdown("### 📊 Métriques de Performance")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    "Performance Totale",
                    f"{metrics['cum_return']:.0f}%",
                    help="Performance totale depuis le début de la période"
                )
            
            with col2:
                st.metric(
                    "Rendement Annualisé",
                    f"{metrics['annualized_return']:.1f}%",
                    help="Rendement moyen annualisé"
                )
            
            with col3:
                st.metric(
                    "Volatilité",
                    f"{metrics['volatility']:.0f}%",
                    help="Volatilité annualisée"
                )
            
            with col4:
                st.metric(
                    "Ratio de Sharpe",
                    f"{metrics['sharpe']:.2f}",
                    help="Ratio rendement/risque (taux sans risque: 2%)"
                )
            
            with col5:
                st.metric(
                    "Drawdown Max",
                    f"{metrics['max_drawdown']:.0f}%",
                    help="Perte maximale observée"
                )
            
            # Graphique de performance
            st.markdown("### 📈 Évolution de la Performance")
            
            # Options d'affichage
            col_left, col_right = st.columns([3, 1])
            
            with col_right:
                interactive_mode = st.checkbox(
                    "🔍 Mode interactif (Plotly)",
                    value=False,
                    help="Activez pour zoomer et explorer le graphique de manière interactive"
                )
            
            with col_left:
                if interactive_mode:
                    # Graphique Plotly interactif
                    fig = create_performance_chart(etf_price_series, selected_etf_row.get('NOM', selected_isin), interactive=True)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    # Graphique Streamlit natif
                    chart_data = create_performance_chart(etf_price_series, selected_etf_row.get('NOM', selected_isin), interactive=False)
                    if chart_data is not None:
                        st.line_chart(chart_data, height=400)
            
            # Période d'analyse
            st.markdown("### 📅 Informations sur la période")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Date de début:** {etf_price_series.index[0].strftime('%d/%m/%Y')}")
            with col2:
                st.write(f"**Date de fin:** {etf_price_series.index[-1].strftime('%d/%m/%Y')}")
            with col3:
                days_diff = (etf_price_series.index[-1] - etf_price_series.index[0]).days
                st.write(f"**Période:** {days_diff/365:.1f} ans")
        
        else:
            st.warning("Données de prix insuffisantes pour cet ETF.")
    
    else:
        st.warning(f"Aucune donnée de prix disponible pour l'ETF {selected_isin}")
        st.info("Les données de performance seront disponibles prochainement.")
    
    # Lien vers plus d'informations
    if 'LIEN' in selected_etf_row and pd.notna(selected_etf_row['LIEN']):
        st.markdown("### 🔗 Plus d'informations")
        st.markdown(f"[Consulter la fiche détaillée de l'ETF]({selected_etf_row['LIEN']})")

# Footer
st.markdown("---")
st.markdown("💡 **Astuce:** Utilisez la page 'Recherche ETF' pour construire votre univers d'investissement personnalisé.")