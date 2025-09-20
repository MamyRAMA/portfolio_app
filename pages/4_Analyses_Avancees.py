"""
Analyses Avancées - MVP avec Simulation d'Investissement
Interface pour analyser le portefeuille et simuler des investissements
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils_data import load_etf_data, get_portfolio_allocation, format_currency

# Configuration de la page
st.set_page_config(
    page_title="Analyses Avancées",
    page_icon="🧮",
    layout="wide"
)

# Titre
st.title("🧮 Analyses Avancées")

# Vérifier si un portfolio existe
if not st.session_state.get('portfolio', []):
    st.warning("⚠️ Aucun portfolio à analyser")
    st.info("💡 Ajoutez des positions via **Gestion Portfolio** pour accéder aux analyses avancées.")
    st.stop()

# Charger les données
etf_data = load_etf_data()

# Onglets d'analyse
tab1, tab2, tab3, tab4 = st.tabs(["📊 Diversification", "💰 Coûts & Frais", "🔮 Simulation", "⚖️ Optimisation"])

with tab1:
    st.subheader("📊 Analyse de Diversification")
    
    # Calculs de diversification
    portfolio_data = st.session_state.portfolio
    
    # Analyse par classe d'actifs
    allocation_df = get_portfolio_allocation(portfolio_data, etf_data)
    
    if not allocation_df.empty:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Graphique camembert
            fig_pie = px.pie(
                allocation_df,
                values='Valeur',
                names='Catégorie',
                title="Répartition par Classe d'Actifs"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Tableau détaillé
            st.write("**Détail de l'Allocation**")
            allocation_display = allocation_df.copy()
            allocation_display['Valeur (€)'] = allocation_display['Valeur'].apply(format_currency)
            allocation_display['Pourcentage (%)'] = allocation_display['Pourcentage'].round(1)
            
            st.dataframe(
                allocation_display[['Catégorie', 'Valeur (€)', 'Pourcentage (%)']],
                use_container_width=True,
                hide_index=True
            )
    
    # Score de diversification
    st.subheader("🎯 Score de Diversification")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Nombre de positions
        nb_positions = len(portfolio_data)
        score_positions = min(nb_positions / 10 * 100, 100)  # Max 100% à 10 positions
        st.metric("Positions", nb_positions, help=f"Score: {score_positions:.0f}/100")
    
    with col2:
        # Diversification géographique (approximation via classes)
        if not allocation_df.empty:
            nb_classes = len(allocation_df)
            score_classes = min(nb_classes / 5 * 100, 100)  # Max 100% à 5 classes
            st.metric("Classes d'Actifs", nb_classes, help=f"Score: {score_classes:.0f}/100")
        else:
            score_classes = 0
    
    with col3:
        # Score global de diversification
        score_global = (score_positions + score_classes) / 2
        
        if score_global >= 80:
            emoji = "🟢"
            comment = "Excellente"
        elif score_global >= 60:
            emoji = "🟡"
            comment = "Bonne"
        else:
            emoji = "🔴"
            comment = "À améliorer"
        
        st.metric("Score Global", f"{score_global:.0f}/100 {emoji}")
        st.write(f"**Diversification:** {comment}")

with tab2:
    st.subheader("💰 Analyse des Coûts et Frais")
    
    # Calculer les frais détaillés
    frais_data = []
    frais_total_annuel = 0
    
    for pos in portfolio_data:
        if pos.get('type') == 'etf' and pos.get('frais', 0) > 0:
            frais_annuel = pos['valeur_actuelle'] * (pos.get('frais', 0) / 100)
            frais_total_annuel += frais_annuel
            
            frais_data.append({
                'Nom': pos['nom'][:30] + '...' if len(pos['nom']) > 30 else pos['nom'],
                'Valeur (€)': pos['valeur_actuelle'],
                'Frais (%)': pos.get('frais', 0),
                'Frais Annuels (€)': frais_annuel
            })
    
    if frais_data:
        # Métriques principales
        valeur_totale = sum(pos['valeur_actuelle'] for pos in portfolio_data)
        taux_frais_moyen = (frais_total_annuel / valeur_totale) * 100 if valeur_totale > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Frais Annuels Totaux", format_currency(frais_total_annuel))
        
        with col2:
            st.metric("Taux de Frais Moyen", f"{taux_frais_moyen:.2f}%")
        
        with col3:
            frais_10_ans = frais_total_annuel * 10
            st.metric("Frais sur 10 ans", format_currency(frais_10_ans))
        
        # Tableau détaillé
        st.write("**Détail des Frais par ETF**")
        df_frais = pd.DataFrame(frais_data)
        
        st.dataframe(
            df_frais,
            column_config={
                'Valeur (€)': st.column_config.NumberColumn("Valeur", format="%.2f €"),
                'Frais (%)': st.column_config.NumberColumn("Frais", format="%.2f%%"),
                'Frais Annuels (€)': st.column_config.NumberColumn("Frais Annuels", format="%.2f €")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Graphique des frais
        if len(df_frais) > 1:
            fig_frais = px.bar(
                df_frais,
                x='Nom',
                y='Frais Annuels (€)',
                title="Frais Annuels par ETF",
                labels={'Nom': 'ETF', 'Frais Annuels (€)': 'Frais Annuels (€)'}
            )
            fig_frais.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_frais, use_container_width=True)
    
    else:
        st.info("Aucun frais détecté dans le portefeuille (ETFs gratuits ou positions manuelles)")

with tab3:
    st.subheader("🔮 Simulation d'Investissement")
    
    # Interface de simulation
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**⚙️ Paramètres de Simulation**")
        
        # Capital initial (valeur actuelle du portefeuille)
        valeur_actuelle = sum(pos['valeur_actuelle'] for pos in portfolio_data)
        
        capital_initial = st.number_input(
            "Capital initial (€)",
            min_value=1000,
            value=int(valeur_actuelle) if valeur_actuelle > 1000 else 10000,
            step=1000,
            help="Montant de départ pour la simulation"
        )
        
        # Horizon d'investissement
        horizon = st.slider(
            "Horizon d'investissement (années)",
            min_value=1,
            max_value=40,
            value=20,
            help="Durée de l'investissement"
        )
        
        # Versements mensuels
        versement_mensuel = st.number_input(
            "Versement mensuel (€)",
            min_value=0,
            value=500,
            step=50,
            help="Montant investi chaque mois"
        )
        
        # Taux d'inflation
        taux_inflation = st.slider(
            "Inflation annuelle (%)",
            min_value=0.0,
            max_value=5.0,
            value=2.0,
            step=0.1,
            help="Taux d'inflation estimé"
        ) / 100
        
        # Calculer le rendement attendu pondéré du portefeuille
        rendement_pondere = 0
        if portfolio_data:
            for pos in portfolio_data:
                poids = pos['valeur_actuelle'] / valeur_actuelle
                rendement_attendu = pos.get('expected_return', 0.05)
                rendement_pondere += poids * rendement_attendu
        else:
            rendement_pondere = 0.05
        
        st.info(f"**Rendement attendu du portefeuille:** {rendement_pondere*100:.1f}%/an")
        
        # Permettre d'ajuster le rendement
        rendement_ajuste = st.slider(
            "Ajuster le rendement (%)",
            min_value=0.0,
            max_value=15.0,
            value=rendement_pondere*100,
            step=0.1,
            help="Rendement annuel attendu"
        ) / 100
    
    with col2:
        st.write("**📈 Résultats de la Simulation**")
        
        # Calculs de simulation
        def calculer_simulation(capital, versement, rendement, inflation, annees):
            valeurs_nominales = []
            valeurs_reelles = []
            cumul_verse = []
            
            valeur = capital
            total_verse = capital
            
            for annee in range(1, annees + 1):
                # Ajout des versements mensuels
                for mois in range(12):
                    valeur = valeur * (1 + rendement/12) + versement
                    total_verse += versement
                
                valeurs_nominales.append(valeur)
                valeur_reelle = valeur / ((1 + inflation) ** annee)
                valeurs_reelles.append(valeur_reelle)
                cumul_verse.append(total_verse)
            
            return valeurs_nominales, valeurs_reelles, cumul_verse
        
        valeurs_nom, valeurs_reel, cumul_verse = calculer_simulation(
            capital_initial, versement_mensuel, rendement_ajuste, taux_inflation, horizon
        )
        
        # Métriques finales
        if valeurs_nom:
            valeur_finale_nom = valeurs_nom[-1]
            valeur_finale_reel = valeurs_reel[-1]
            total_verse_final = cumul_verse[-1]
            plus_value = valeur_finale_nom - total_verse_final
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric("Valeur Finale", format_currency(valeur_finale_nom))
                st.metric("En Pouvoir d'Achat", format_currency(valeur_finale_reel))
            
            with metric_col2:
                st.metric("Total Versé", format_currency(total_verse_final))
                st.metric("Plus-Value", format_currency(plus_value))
            
            with metric_col3:
                rendement_total = (plus_value / total_verse_final * 100) if total_verse_final > 0 else 0
                rendement_annuel = ((valeur_finale_nom / total_verse_final) ** (1/horizon) - 1) * 100
                st.metric("Gain Total", f"{rendement_total:.1f}%")
                st.metric("Rendement Annuel", f"{rendement_annuel:.1f}%")
        
        # Graphique d'évolution
        if valeurs_nom:
            annees = list(range(1, horizon + 1))
            
            fig_sim = go.Figure()
            
            fig_sim.add_trace(go.Scatter(
                x=annees,
                y=valeurs_nom,
                mode='lines+markers',
                name='Valeur Nominale',
                line=dict(color='green', width=3)
            ))
            
            fig_sim.add_trace(go.Scatter(
                x=annees,
                y=valeurs_reel,
                mode='lines+markers',
                name='Valeur Réelle (inflation)',
                line=dict(color='blue', width=2, dash='dash')
            ))
            
            fig_sim.add_trace(go.Scatter(
                x=annees,
                y=cumul_verse,
                mode='lines+markers',
                name='Total Versé',
                line=dict(color='orange', width=2)
            ))
            
            fig_sim.update_layout(
                title=f"Évolution du Capital sur {horizon} ans",
                xaxis_title="Années",
                yaxis_title="Valeur (€)",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_sim, use_container_width=True)
        
        # Analyse de sensibilité
        st.write("**🎚️ Analyse de Sensibilité**")
        
        sensibilite_data = []
        for rdt in [rendement_ajuste-0.02, rendement_ajuste-0.01, rendement_ajuste, rendement_ajuste+0.01, rendement_ajuste+0.02]:
            if rdt > 0:
                val_test, _, _ = calculer_simulation(capital_initial, versement_mensuel, rdt, taux_inflation, horizon)
                if val_test:
                    sensibilite_data.append({
                        'Rendement': f"{rdt*100:.1f}%",
                        'Valeur Finale': format_currency(val_test[-1])
                    })
        
        if sensibilite_data:
            st.dataframe(pd.DataFrame(sensibilite_data), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("⚖️ Recommandations d'Optimisation")
    
    # Analyse du portefeuille actuel
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Analyse Actuelle**")
        
        # Concentration par position
        valeur_totale = sum(pos['valeur_actuelle'] for pos in portfolio_data)
        positions_tri = sorted(portfolio_data, key=lambda x: x['valeur_actuelle'], reverse=True)
        
        if positions_tri:
            plus_grosse_position = positions_tri[0]['valeur_actuelle'] / valeur_totale * 100
            
            st.write(f"**Plus grosse position:** {plus_grosse_position:.1f}%")
            
            if plus_grosse_position > 30:
                st.warning("⚠️ Position très concentrée (>30%)")
            elif plus_grosse_position > 20:
                st.info("ℹ️ Position assez concentrée (>20%)")
            else:
                st.success("✅ Bonne répartition des positions")
        
        # Analyse des frais
        if frais_data:
            frais_moyen = sum(pos.get('frais', 0) for pos in portfolio_data if pos.get('type') == 'etf') / len([p for p in portfolio_data if p.get('type') == 'etf'])
            
            st.write(f"**Frais moyens:** {frais_moyen:.2f}%")
            
            if frais_moyen > 0.5:
                st.warning("⚠️ Frais élevés (>0.5%)")
            elif frais_moyen > 0.3:
                st.info("ℹ️ Frais modérés (>0.3%)")
            else:
                st.success("✅ Frais faibles")
    
    with col2:
        st.write("**💡 Recommandations**")
        
        recommandations = []
        
        # Recommandations basées sur la diversification
        if not allocation_df.empty:
            if len(allocation_df) < 3:
                recommandations.append("🎯 Diversifier sur plus de classes d'actifs")
            
            # Vérifier la concentration
            if not allocation_df.empty:
                max_allocation = allocation_df['Pourcentage'].max()
                if max_allocation > 70:
                    recommandations.append("⚖️ Réduire la concentration sur une classe")
        
        # Recommandations sur les frais
        positions_etf = [p for p in portfolio_data if p.get('type') == 'etf']
        if positions_etf:
            frais_eleves = [p for p in positions_etf if p.get('frais', 0) > 0.5]
            if frais_eleves:
                recommandations.append("💰 Considérer des ETF moins chers")
        
        # Recommandations sur les positions
        if len(portfolio_data) < 5:
            recommandations.append("📈 Ajouter plus de positions pour diversifier")
        elif len(portfolio_data) > 20:
            recommandations.append("🎯 Simplifier avec moins de positions")
        
        # Recommandations PEA
        positions_pea = sum(1 for p in portfolio_data if p.get('pea') == 'Y')
        if positions_pea < len(portfolio_data) / 2:
            recommandations.append("🇫🇷 Privilégier les ETF éligibles PEA")
        
        # Affichage des recommandations
        if recommandations:
            for i, rec in enumerate(recommandations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.success("✅ Portefeuille bien équilibré !")
        
        # Score global
        score_diversification = min(len(allocation_df) * 20, 100) if not allocation_df.empty else 0
        score_frais = max(0, 100 - (frais_moyen * 200)) if frais_data else 100
        score_positions = min(len(portfolio_data) * 10, 100)
        
        score_final = (score_diversification + score_frais + score_positions) / 3
        
        st.write("**🏆 Score Global du Portefeuille**")
        
        if score_final >= 80:
            emoji = "🟢"
            commentaire = "Excellent portefeuille"
        elif score_final >= 60:
            emoji = "🟡"
            commentaire = "Bon portefeuille"
        else:
            emoji = "🔴"
            commentaire = "Portefeuille à optimiser"
        
        st.metric("Score", f"{score_final:.0f}/100 {emoji}")
        st.write(f"**{commentaire}**")

# Actions rapides
st.markdown("---")
st.subheader("⚡ Actions Rapides")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("📊 Retour Dashboard"):
        st.switch_page("pages/1_Dashboard.py")

with action_col2:
    if st.button("📂 Gérer Portfolio"):
        st.switch_page("pages/2_Gestion_Portfolio.py")

with action_col3:
    if st.button("🔍 Rechercher ETF"):
        st.switch_page("pages/3_Recherche_ETF.py")

with action_col4:
    if st.button("🔄 Actualiser"):
        st.rerun()