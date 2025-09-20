"""
Dashboard Portfolio - MVP Optimisé
Vue d'ensemble avec positions détaillées, allocations et métriques avancées
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils_data import load_etf_data, calculate_portfolio_metrics, format_currency, format_percentage, get_portfolio_allocation

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Portfolio",
    page_icon="📈",
    layout="wide"
)

# Titre
st.title("📈 Dashboard Portfolio")

# Vérifier si un portfolio existe
if not st.session_state.get('portfolio', []):
    st.warning("⚠️ Aucune position en portefeuille")
    st.info("💡 Ajoutez des positions via la page **Gestion Portfolio** pour voir votre dashboard.")
    
    # Afficher quelques statistiques générales sur les ETFs disponibles
    st.subheader("📊 Aperçu de la Base de Données ETF")
    
    etf_data = load_etf_data()
    if not etf_data.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("ETFs Disponibles", len(etf_data))
        
        with col2:
            if 'PROVIDER' in etf_data.columns:
                st.metric("Fournisseurs", etf_data['PROVIDER'].nunique())
        
        with col3:
            if 'CLASSE 1' in etf_data.columns:
                st.metric("Classes d'Actifs", etf_data['CLASSE 1'].nunique())
        
        with col4:
            if 'PEA' in etf_data.columns:
                pea_eligible = (etf_data['PEA'] == 'Y').sum()
                st.metric("ETFs Éligibles PEA", pea_eligible)
    
    st.stop()

# Calcul des métriques du portfolio
portfolio_metrics = calculate_portfolio_metrics(st.session_state.portfolio)
etf_data = load_etf_data()

# Métriques principales
st.subheader("📊 Vue d'Ensemble du Portfolio")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Valeur Totale", 
        format_currency(portfolio_metrics['valeur_totale']),
        help="Valeur actuelle totale du portefeuille"
    )

with col2:
    total_cout = sum(pos['cout_acquisition'] for pos in st.session_state.portfolio)
    st.metric(
        "Coût Total", 
        format_currency(total_cout),
        help="Investissement total réalisé"
    )

with col3:
    st.metric(
        "Plus-Value", 
        format_currency(portfolio_metrics['plus_value_totale']),
        delta=format_percentage(portfolio_metrics['performance_globale']),
        help="Plus-value totale et performance en %"
    )

with col4:
    st.metric(
        "Positions", 
        portfolio_metrics['nombre_positions'],
        help="Nombre total de positions"
    )

with col5:
    if portfolio_metrics['valeur_totale'] > 0:
        position_moyenne = portfolio_metrics['valeur_totale'] / portfolio_metrics['nombre_positions']
        st.metric(
            "Position Moyenne", 
            format_currency(position_moyenne),
            help="Valeur moyenne par position"
        )

st.markdown("---")

# Tableau détaillé des positions
st.subheader("📋 Détail des Positions")

# Créer un DataFrame pour l'affichage
positions_display = []
for pos in st.session_state.portfolio:
    plus_value = pos['valeur_actuelle'] - pos['cout_acquisition']
    performance = (plus_value / pos['cout_acquisition'] * 100) if pos['cout_acquisition'] > 0 else 0
    
    positions_display.append({
        'Nom': pos['nom'],
        'ISIN': pos['isin'],
        'Fournisseur': pos['provider'],
        'Quantité': int(pos['quantite']),  # Sans décimale comme demandé
        'Prix Achat (€)': round(pos['prix_achat'], 2),
        'Prix Actuel (€)': round(pos['prix_actuel'], 2),
        'Date Achat': pos['date_achat'],
        'Valeur (€)': round(pos['valeur_actuelle'], 2),
        'Plus-Value (€)': round(plus_value, 2),
        'Performance (%)': round(performance, 2),
        'Classe': pos.get('classe_1', 'N/A'),
        'Frais (%)': pos.get('frais', 0),
        'PEA': '✅' if pos.get('pea') == 'Y' else '❌'
    })

if positions_display:
    df_positions = pd.DataFrame(positions_display)
    
    # Configuration des colonnes pour l'affichage
    column_config = {
        'Nom': st.column_config.TextColumn("Nom", width="large"),
        'ISIN': st.column_config.TextColumn("ISIN", width="small"),
        'Fournisseur': st.column_config.TextColumn("Fournisseur", width="small"),
        'Quantité': st.column_config.NumberColumn("Qté", format="%d"),
        'Prix Achat (€)': st.column_config.NumberColumn("Prix Achat", format="%.2f €"),
        'Prix Actuel (€)': st.column_config.NumberColumn("Prix Actuel", format="%.2f €"),
        'Date Achat': st.column_config.DateColumn("Date Achat"),
        'Valeur (€)': st.column_config.NumberColumn("Valeur", format="%.2f €"),
        'Plus-Value (€)': st.column_config.NumberColumn("Plus-Value", format="%.2f €"),
        'Performance (%)': st.column_config.NumberColumn("Perf %", format="%.2f%%"),
        'Classe': st.column_config.TextColumn("Classe", width="small"),
        'Frais (%)': st.column_config.NumberColumn("Frais", format="%.2f%%"),
        'PEA': st.column_config.TextColumn("PEA", width="small")
    }
    
    # Tableau interactif
    st.dataframe(
        df_positions,
        column_config=column_config,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# Graphiques de répartition
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🥧 Allocation par Classe d'Actifs")
    
    allocation_df = get_portfolio_allocation(st.session_state.portfolio, etf_data)
    
    if not allocation_df.empty:
        fig_allocation = px.pie(
            allocation_df,
            values='Valeur',
            names='Catégorie',
            title="Répartition par Classe",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_allocation.update_traces(textposition='inside', textinfo='percent+label')
        fig_allocation.update_layout(showlegend=True, height=400)
        st.plotly_chart(fig_allocation, use_container_width=True)
    else:
        st.info("Données d'allocation non disponibles")

with col2:
    st.subheader("📊 Top 5 Positions")
    
    # Top positions par valeur
    top_positions = sorted(st.session_state.portfolio, key=lambda x: x['valeur_actuelle'], reverse=True)[:5]
    
    if top_positions:
        top_names = [pos['nom'][:30] + '...' if len(pos['nom']) > 30 else pos['nom'] for pos in top_positions]
        top_values = [pos['valeur_actuelle'] for pos in top_positions]
        
        fig_top = px.bar(
            x=top_values,
            y=top_names,
            orientation='h',
            title="Top 5 par Valeur",
            labels={'x': 'Valeur (€)', 'y': 'Position'}
        )
        fig_top.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# Analyse des performances
st.subheader("📈 Analyse des Performances")

perf_col1, perf_col2, perf_col3 = st.columns(3)

with perf_col1:
    st.write("**📊 Statistiques de Performance**")
    
    performances = []
    for pos in st.session_state.portfolio:
        if pos['cout_acquisition'] > 0:
            perf = (pos['valeur_actuelle'] - pos['cout_acquisition']) / pos['cout_acquisition'] * 100
            performances.append(perf)
    
    if performances:
        st.metric("Performance Moyenne", f"{sum(performances)/len(performances):+.2f}%")
        st.metric("Meilleure Performance", f"{max(performances):+.2f}%")
        st.metric("Moins Bonne Performance", f"{min(performances):+.2f}%")
    
with perf_col2:
    st.write("**💰 Répartition des Frais**")
    
    # Calculer les frais totaux
    frais_annuels_total = 0
    for pos in st.session_state.portfolio:
        if pos.get('type') == 'etf' and pos.get('frais', 0) > 0:
            frais_annuels = pos['valeur_actuelle'] * (pos.get('frais', 0) / 100)
            frais_annuels_total += frais_annuels
    
    st.metric("Frais Annuels Estimés", format_currency(frais_annuels_total))
    
    if portfolio_metrics['valeur_totale'] > 0:
        taux_frais_global = (frais_annuels_total / portfolio_metrics['valeur_totale']) * 100
        st.metric("Taux de Frais Global", f"{taux_frais_global:.2f}%")

with perf_col3:
    st.write("**🏷️ Informations Diversification**")
    
    # Compter les types d'actifs
    types_actifs = {}
    for pos in st.session_state.portfolio:
        type_actif = pos.get('type', 'unknown')
        types_actifs[type_actif] = types_actifs.get(type_actif, 0) + 1
    
    st.metric("ETFs", types_actifs.get('etf', 0))
    st.metric("Actifs Manuels", types_actifs.get('manuel', 0))
    
    # Éligibilité PEA
    pea_eligible = sum(1 for pos in st.session_state.portfolio if pos.get('pea') == 'Y')
    st.metric("Positions PEA", f"{pea_eligible}/{len(st.session_state.portfolio)}")

# Graphique d'évolution potentielle (basé sur les rendements attendus)
st.markdown("---")
st.subheader("🔮 Projection de Rendement")

col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.portfolio:
        # Calculer le rendement attendu pondéré
        rendement_pondere = 0
        valeur_totale = portfolio_metrics['valeur_totale']
        
        for pos in st.session_state.portfolio:
            poids = pos['valeur_actuelle'] / valeur_totale
            rendement_attendu = pos.get('expected_return', 0.05)  # 5% par défaut
            rendement_pondere += poids * rendement_attendu
        
        # Projection sur plusieurs années
        years = list(range(1, 11))  # 10 ans
        projections = []
        valeur_actuelle = valeur_totale
        
        for year in years:
            valeur_projetee = valeur_totale * ((1 + rendement_pondere) ** year)
            projections.append(valeur_projetee)
        
        # Graphique de projection
        fig_projection = go.Figure()
        
        fig_projection.add_trace(go.Scatter(
            x=[0] + years,
            y=[valeur_totale] + projections,
            mode='lines+markers',
            name='Projection',
            line=dict(color='green', width=3)
        ))
        
        fig_projection.update_layout(
            title=f"Projection de Croissance (Rendement: {rendement_pondere*100:.1f}%/an)",
            xaxis_title="Années",
            yaxis_title="Valeur (€)",
            height=400
        )
        
        st.plotly_chart(fig_projection, use_container_width=True)

with col2:
    st.write("**💡 Informations Projection**")
    st.write(f"**Rendement Attendu Pondéré:** {rendement_pondere*100:.1f}%/an")
    st.write(f"**Valeur Actuelle:** {format_currency(valeur_totale)}")
    
    if projections:
        st.write(f"**Projection 5 ans:** {format_currency(projections[4])}")
        st.write(f"**Projection 10 ans:** {format_currency(projections[9])}")
        
        gain_5_ans = projections[4] - valeur_totale
        gain_10_ans = projections[9] - valeur_totale
        
        st.write(f"**Gain potentiel 5 ans:** {format_currency(gain_5_ans)}")
        st.write(f"**Gain potentiel 10 ans:** {format_currency(gain_10_ans)}")

# Actions rapides
st.markdown("---")
st.subheader("⚡ Actions Rapides")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("➕ Ajouter Position", type="primary"):
        st.switch_page("pages/2_Gestion_Portfolio.py")

with action_col2:
    if st.button("🔍 Rechercher ETF"):
        st.switch_page("pages/3_Recherche_ETF.py")

with action_col3:
    if st.button("📊 Analyses Avancées"):
        st.switch_page("pages/4_Analyses_Avancees.py")

with action_col4:
    if st.button("🔄 Actualiser", help="Recharger le dashboard"):
        st.rerun()

# Footer avec dernière mise à jour
st.markdown("---")
st.caption(f"Dernière actualisation: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}")