"""
Recherche ETF & Univers d'Investissement - MVP
Interface pour explorer les ETFs et créer un univers d'investissement personnalisé
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils_data import load_etf_data, search_etf, filter_etf_data, format_currency

# Configuration de la page
st.set_page_config(
    page_title="Recherche ETF",
    page_icon="🔍",
    layout="wide"
)

# Initialiser l'univers d'investissement
if 'univers_etf' not in st.session_state:
    st.session_state.univers_etf = []

# Titre
st.title("🔍 Recherche ETF & Univers d'Investissement")

# Charger les données
etf_data = load_etf_data()

if etf_data.empty:
    st.error("❌ Impossible de charger les données ETF")
    st.stop()

# Onglets principaux
tab1, tab2 = st.tabs(["🔍 Recherche ETF", "⭐ Mon Univers"])

with tab1:
    # Statistiques générales
    st.subheader("📊 Vue d'Ensemble")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("ETFs Disponibles", f"{len(etf_data):,}")
    with col2:
        if 'PROVIDER' in etf_data.columns:
            st.metric("Fournisseurs", etf_data['PROVIDER'].nunique())
    with col3:
        if 'CLASSE 1' in etf_data.columns:
            st.metric("Classes d'Actifs", etf_data['CLASSE 1'].nunique())
    with col4:
        if 'PEA' in etf_data.columns:
            pea_count = (etf_data['PEA'] == 'O').sum()
            st.metric("ETFs Éligibles PEA", f"{pea_count:,}")
    
    st.markdown("---")
    
    # Interface de recherche et filtres
    filter_col, result_col = st.columns([1, 2])
    
    with filter_col:
        st.write("**🔎 Filtres de Recherche**")
        
        # Recherche textuelle
        search_term = st.text_input(
            "Recherche textuelle",
            placeholder="Nom, ISIN, fournisseur...",
            help="Recherchez par nom d'ETF, ISIN ou fournisseur"
        )
        
        # Filtres par catégorie
        if 'CLASSE 1' in etf_data.columns:
            classe_1_options = ['Tous'] + sorted(etf_data['CLASSE 1'].dropna().unique().tolist())
            selected_classe_1 = st.selectbox("Classe d'Actifs", classe_1_options)
        
        # Filtre par fournisseur
        if 'PROVIDER' in etf_data.columns:
            provider_options = ['Tous'] + sorted(etf_data['PROVIDER'].dropna().unique().tolist())
            selected_provider = st.selectbox("Fournisseur", provider_options)
        
        # Filtre éligibilité PEA
        if 'PEA' in etf_data.columns:
            pea_filter = st.selectbox(
                "Éligibilité PEA", 
                ['Tous', 'Éligible PEA', 'Non éligible PEA']
            )
        
        # Filtre par frais de gestion
        if 'FRAIS DE GESTION' in etf_data.columns:
            frais_data = etf_data['FRAIS DE GESTION'].dropna()
            if not frais_data.empty:
                max_frais = st.slider(
                    "Frais de gestion max (%)",
                    min_value=0.0,
                    max_value=float(frais_data.max()),
                    value=float(frais_data.max()),
                    step=0.01,
                    format="%.2f%%"
                )
        
        # Bouton de réinitialisation
        if st.button("🔄 Réinitialiser"):
            st.rerun()
    
    with result_col:
        st.write("**📋 Résultats de Recherche**")
        
        # Appliquer les filtres
        filtered_data = etf_data.copy()
        
        if search_term:
            filtered_data = search_etf(filtered_data, search_term)
        
        # Construire les filtres
        filters = {}
        if 'selected_classe_1' in locals() and selected_classe_1 != 'Tous':
            filters['classe_1'] = [selected_classe_1]
        if 'selected_provider' in locals() and selected_provider != 'Tous':
            filters['provider'] = [selected_provider]
        if 'pea_filter' in locals() and pea_filter != 'Tous':
            filters['pea'] = pea_filter == 'Éligible PEA'
        if 'max_frais' in locals():
            filters['frais_max'] = max_frais
        
        if filters:
            filtered_data = filter_etf_data(filtered_data, filters)
        
        # Afficher les résultats
        st.write(f"**{len(filtered_data):,}** ETFs trouvés")
        
        if len(filtered_data) > 0:
            # Limiter l'affichage
            if len(filtered_data) > 50:
                st.info(f"Affichage des 50 premiers résultats sur {len(filtered_data)}")
                display_data = filtered_data.head(50)
            else:
                display_data = filtered_data
            
            # Colonnes à afficher avec informations détaillées
            display_columns = ['ISIN', 'NOM', 'PROVIDER']
            column_config = {
                'ISIN': st.column_config.TextColumn("ISIN", width="small"),
                'NOM': st.column_config.TextColumn("Nom ETF", width="large"),
                'PROVIDER': st.column_config.TextColumn("Fournisseur", width="small")
            }
            
            # Ajouter les colonnes disponibles
            for col in ['FRAIS DE GESTION', 'ENCOURS SOUS GESTION (EUR)', 'PEA', 'ASSVIE', 'HEDGED', 'CLASSE 1']:
                if col in display_data.columns:
                    display_columns.append(col)
                    if col == 'FRAIS DE GESTION':
                        column_config[col] = st.column_config.NumberColumn("Frais (%)", format="%.2f", width="small")
                    elif col == 'ENCOURS SOUS GESTION (EUR)':
                        column_config[col] = st.column_config.NumberColumn("AUM (M€)", format="%.0f", width="small")
                    elif col in ['PEA', 'ASSVIE', 'HEDGED']:
                        column_config[col] = st.column_config.TextColumn(col, width="small")
                    else:
                        column_config[col] = st.column_config.TextColumn(col, width="small")
            
            # Tableau avec sélection
            selected_etfs = st.dataframe(
                display_data[display_columns],
                column_config=column_config,
                selection_mode="multi-row",
                on_select="rerun",
                use_container_width=True,
                key="etf_search_results"
            )
            
            # Actions sur les ETFs sélectionnés
            if selected_etfs.selection.rows:
                selected_indices = selected_etfs.selection.rows
                selected_data = display_data.iloc[selected_indices]
                
                st.write(f"**{len(selected_indices)} ETF(s) sélectionné(s)**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("⭐ Ajouter à l'Univers", type="primary"):
                        added_count = 0
                        for _, etf in selected_data.iterrows():
                            # Vérifier si l'ETF n'est pas déjà dans l'univers
                            if not any(u['isin'] == etf['ISIN'] for u in st.session_state.univers_etf):
                                univers_etf = {
                                    'isin': etf['ISIN'],
                                    'nom': etf['NOM'],
                                    'provider': etf.get('PROVIDER', 'N/A'),
                                    'frais': etf.get('FRAIS DE GESTION', 0),
                                    'aum': etf.get('ENCOURS SOUS GESTION (EUR)', 0),
                                    'pea': etf.get('PEA', 'N'),
                                    'assvie': etf.get('ASSVIE', 'N'),
                                    'hedged': etf.get('HEDGED', 'N'),
                                    'classe_1': etf.get('CLASSE 1', 'N/A'),
                                    'expected_return': etf.get('EXP_MACRO_RETURN', 5.0) / 100 if pd.notna(etf.get('EXP_MACRO_RETURN', 5.0)) else 0.05  # Convertir en décimal
                                }
                                st.session_state.univers_etf.append(univers_etf)
                                added_count += 1
                        
                        if added_count > 0:
                            st.success(f"✅ {added_count} ETF(s) ajouté(s) à votre univers!")
                        else:
                            st.warning("⚠️ Ces ETFs sont déjà dans votre univers")
                        st.rerun()
                
                with col2:
                    if st.button("📊 Voir Détails"):
                        # Afficher les détails des ETFs sélectionnés
                        for _, etf in selected_data.iterrows():
                            with st.expander(f"📋 {etf['NOM']}"):
                                detail_col1, detail_col2 = st.columns(2)
                                with detail_col1:
                                    st.write(f"**ISIN:** {etf['ISIN']}")
                                    st.write(f"**Fournisseur:** {etf.get('PROVIDER', 'N/A')}")
                                    st.write(f"**Classe:** {etf.get('CLASSE 1', 'N/A')}")
                                with detail_col2:
                                    st.write(f"**Frais:** {etf.get('FRAIS DE GESTION', 0):.2f}%")
                                    st.write(f"**AUM:** {etf.get('ENCOURS SOUS GESTION (EUR)', 0):.0f} M€")
                                    st.write(f"**PEA:** {'✅' if etf.get('PEA') == 'Y' else '❌'}")
                                    st.write(f"**Assurance Vie:** {'✅' if etf.get('ASSVIE') == 'Y' else '❌'}")
                                    st.write(f"**Hedgé:** {'✅' if etf.get('HEDGED') == 'Y' else '❌'}")
                
                with col3:
                    if st.button("➕ Vers Portfolio"):
                        st.info("💡 Redirection vers Gestion Portfolio")
                        st.switch_page("pages/2_Gestion_Portfolio.py")
        else:
            st.warning("⚠️ Aucun ETF ne correspond à vos critères")

with tab2:
    st.subheader("⭐ Mon Univers d'Investissement")
    
    if not st.session_state.univers_etf:
        st.info("📭 Votre univers d'investissement est vide. Utilisez l'onglet 'Recherche ETF' pour ajouter des ETFs favoris.")
    else:
        # Statistiques de l'univers
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("ETFs dans l'Univers", len(st.session_state.univers_etf))
        
        with col2:
            frais_moyen = sum(etf.get('frais', 0) for etf in st.session_state.univers_etf) / len(st.session_state.univers_etf)
            st.metric("Frais Moyen", f"{frais_moyen:.2f}%")
        
        with col3:
            pea_count = sum(1 for etf in st.session_state.univers_etf if etf.get('pea') == 'Y')
            st.metric("Éligibles PEA", f"{pea_count}/{len(st.session_state.univers_etf)}")
        
        with col4:
            expected_return = sum(etf.get('expected_return', 0.05) for etf in st.session_state.univers_etf) / len(st.session_state.univers_etf)
            st.metric("Rendement Moyen", f"{expected_return*100:.1f}%")
        
        st.markdown("---")
        
        # Tableau de l'univers
        univers_df = pd.DataFrame(st.session_state.univers_etf)
        
        # Affichage avec actions
        for i, etf in enumerate(st.session_state.univers_etf):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{etf['nom']}**")
                    st.write(f"ISIN: {etf['isin']} | {etf['provider']}")
                
                with col2:
                    st.write(f"**Frais:** {etf.get('frais', 0):.2f}%")
                    st.write(f"**AUM:** {etf.get('aum', 0):.0f} M€")
                    st.write(f"**PEA:** {'✅' if etf.get('pea') == 'Y' else '❌'}")
                    st.write(f"**Assurance Vie:** {'✅' if etf.get('assvie') == 'Y' else '❌'}")
                    st.write(f"**Hedgé:** {'✅' if etf.get('hedged') == 'Y' else '❌'}")
                
                with col3:
                    col_add, col_del = st.columns(2)
                    with col_add:
                        if st.button("➕", key=f"add_to_portfolio_{i}", help="Ajouter au portfolio"):
                            st.info("Redirection vers Gestion Portfolio")
                            # Ici on pourrait pre-remplir les données
                            st.switch_page("pages/2_Gestion_Portfolio.py")
                    
                    with col_del:
                        if st.button("🗑️", key=f"remove_from_univers_{i}", help="Retirer de l'univers"):
                            st.session_state.univers_etf.pop(i)
                            st.rerun()
                
                # Détails supplémentaires
                with st.expander("📊 Détails"):
                    detail_col1, detail_col2, detail_col3 = st.columns(3)
                    with detail_col1:
                        st.write(f"**Classe:** {etf.get('classe_1', 'N/A')}")
                    with detail_col2:
                        st.write(f"**Rendement Attendu:** {etf.get('expected_return', 0.05)*100:.1f}%")
                    with detail_col3:
                        st.write(f"**PEA:** {'✅ Oui' if etf.get('pea') == 'Y' else '❌ Non'}")
                        st.write(f"**Assurance Vie:** {'✅ Oui' if etf.get('assvie') == 'Y' else '❌ Non'}")
                        st.write(f"**Hedgé:** {'✅ Oui' if etf.get('hedged') == 'Y' else '❌ Non'}")
                
                st.markdown("---")
        
        # Actions sur l'univers complet
        if st.session_state.univers_etf:
            st.subheader("🔧 Actions sur l'Univers")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📤 Exporter l'Univers"):
                    univers_df = pd.DataFrame(st.session_state.univers_etf)
                    csv_data = univers_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Télécharger CSV",
                        data=csv_data,
                        file_name=f"univers_etf_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("🗑️ Vider l'Univers", type="secondary"):
                    if st.checkbox("⚠️ Confirmer la suppression"):
                        st.session_state.univers_etf = []
                        st.success("Univers vidé!")
                        st.rerun()

# Section d'aide
with st.expander("❓ Aide - Univers d'Investissement"):
    st.markdown("""
    ### Qu'est-ce que l'Univers d'Investissement ?
    
    L'univers d'investissement est votre sélection personnelle d'ETFs favoris que vous considérez pour vos investissements.
    
    ### Comment l'utiliser :
    
    1. **Rechercher** des ETFs avec les filtres
    2. **Sélectionner** les ETFs intéressants
    3. **Ajouter à l'Univers** pour créer votre sélection personnelle
    4. **Gérer votre Univers** depuis l'onglet dédié
    5. **Ajouter au Portfolio** directement depuis l'univers
    
    ### Avantages :
    - Pré-sélection de vos ETFs préférés
    - Accès rapide aux informations importantes
    - Facilite la construction de portefeuille
    - Exporter/sauvegarder votre sélection
    """)