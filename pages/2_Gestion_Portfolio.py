"""
Gestion Portfolio - MVP Amélioré
Interface pour gérer les positions avec univers d'investissement et informations détaillées
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils_data import load_etf_data, search_etf, format_currency

# Configuration de la page
st.set_page_config(
    page_title="Gestion Portfolio",
    page_icon="📂",
    layout="wide"
)

ASSET_TYPE_TO_CLASSE1 = {
    "Action": "equities",
    "Crypto": "crypto",
    "Obligation": "bonds",
    "Immobilier": "real estate",
    "Livret": "cash",
    "Matières Premières": "commodities",
    "Monétaire": "cash",
    "Titrisé": "securitized",
    "Autre": "other",
    "Actif Manuel": "other"  # valeur de secours
}

def map_user_type_to_classe1(user_type):
    """Retourne la CLASSE 1 correspondant au type choisi par l'utilisateur."""
    return ASSET_TYPE_TO_CLASSE1.get(user_type)

# Titre
st.title("📂 Gestion Portfolio")

# Initialiser les données si nécessaire
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

if 'univers_etf' not in st.session_state:
    st.session_state.univers_etf = []

# Charger les données ETF
etf_data = load_etf_data()

# Onglets pour organiser les fonctionnalités
tab1, tab2, tab3, tab4 = st.tabs(["➕ Ajouter Position", "⭐ Depuis Univers", "📋 Mes Positions", "📤 Import/Export"])

with tab1:
    st.subheader("Ajouter une Position Manuellement")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Option 1: Actif Manuel (libre)**")
        
        
        nom_libre = st.text_input("Nom de l'actif", placeholder="Ex: Action Apple, Bitcoin, etc.")
        isin_libre = st.text_input("Code/ISIN (optionnel)", placeholder="Ex: US0378331005")
        type_libre = st.selectbox("Type d'actif", ["Action", "Crypto", "Obligation", "Immobilier", "Livret", "Matières Premières", "Monétaire","Titrisé", "Autre"], index=0)
        type_libre = map_user_type_to_classe1(type_libre)

        col_qty, col_price = st.columns(2)
        with col_qty:
            quantite_libre = st.number_input("Quantité", min_value=1, value=1, step=1)
        with col_price:
            prix_achat_libre = st.number_input("Prix d'achat (€)", min_value=0.01, value=100.0, step=1.0)

        prix_actuel_libre = st.number_input("Prix actuel (€)", min_value=0.01, value=100.0, step=1.0)
        date_achat_libre = st.date_input("Date d'achat", value=date.today())
        
        # Calculs automatiques mis à jour en temps réel
        cout_libre = quantite_libre * prix_achat_libre
        valeur_libre = quantite_libre * prix_actuel_libre
        pv_libre = valeur_libre - cout_libre
        perf_libre = (pv_libre / cout_libre * 100) if cout_libre > 0 else 0
        
        st.write("**Résumé (Mise à jour automatique)**")
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric("Coût", format_currency(cout_libre))
            st.metric("Valeur", format_currency(valeur_libre))
        with col2_res:
            st.metric("Plus-value", format_currency(pv_libre), delta=f"{perf_libre:+.2f}%")
            st.metric("Performance", f"{perf_libre:+.1f}%")
    
        with st.form("add_manual_position", clear_on_submit=False):
            # Désactiver la soumission sur Entrée
            submit_manual = st.form_submit_button("➕ Ajouter Position Manuel", type="primary", use_container_width=True)
            
        # Traitement uniquement si bouton cliqué ET nom renseigné
        if submit_manual:
            if nom_libre.strip():
                position_libre = {
                    'isin': isin_libre or f"MANUAL_{len(st.session_state.portfolio)}",
                    'nom': nom_libre,
                    'provider': 'Manuel',
                    'quantite': quantite_libre,
                    'prix_achat': prix_achat_libre,
                    'prix_actuel': prix_actuel_libre,
                    'cout_acquisition': cout_libre,
                    'valeur_actuelle': valeur_libre,
                    'date_achat': str(date_achat_libre),
                    'classe_1': type_libre,
                    'type': 'manuel',
                    'frais': 0.0,
                    'expected_return': 0.06
                }
                st.session_state.portfolio.append(position_libre)
                st.success(f"✅ Position ajoutée: {position_libre['nom']}")
                st.rerun()
                
                
            else:
                st.error("⚠️ Veuillez saisir un nom d'actif")
    
    with col2:
        st.write("**Option 2: Recherche ETF dans la Base**")
        
        # Recherche d'ETF
        search_term = st.text_input(
            "Rechercher un ETF",
            placeholder="Ex: MSCI World, IE00B4L5Y983, iShares...",
            key="search_etf_add"
        )
        
        if search_term:
            filtered_etfs = search_etf(etf_data, search_term)
            
            if not filtered_etfs.empty:
                st.write(f"**{len(filtered_etfs)} ETF(s) trouvé(s)**")
                
                # Sélection ETF
                etf_options = {}
                for idx, row in filtered_etfs.head(5).iterrows():
                    key = f"{row['NOM']} ({row['ISIN']})"
                    etf_options[key] = idx
                
                if etf_options:
                    selected_etf_key = st.selectbox("Choisir un ETF", list(etf_options.keys()))
                    selected_etf_idx = etf_options[selected_etf_key]
                    selected_etf_data = filtered_etfs.loc[selected_etf_idx]
                    
                    # Afficher les détails de l'ETF sélectionné
                    with st.expander("📊 Détails de l'ETF"):
                        detail_col1, detail_col2 = st.columns(2)
                        with detail_col1:
                            st.write(f"**Fournisseur:** {selected_etf_data.get('PROVIDER', 'N/A')}")
                            st.write(f"**Frais:** {selected_etf_data.get('FRAIS DE GESTION', 0):.2f}%")
                            st.write(f"**AUM:** {selected_etf_data.get('ENCOURS SOUS GESTION (EUR)', 0):,.0f} M€".replace(',', ' '))
                        with detail_col2:
                            st.write(f"**PEA:** {'✅ Oui' if selected_etf_data.get('PEA') == 'Y' else '❌ Non'}")
                            st.write(f"**Assurance Vie:** {'✅ Oui' if selected_etf_data.get('ASSVIE') == 'Y' else '❌ Non'}")
                            st.write(f"**Hedgé:** {'✅ Oui' if selected_etf_data.get('HEDGED') == 'Y' else '❌ Non'}")
                            st.write(f"**Classe:** {selected_etf_data.get('CLASSE 1', 'N/A')}")
                            expected_ret = selected_etf_data.get('EXP_MACRO_RETURN', 5.0) / 100 if pd.notna(selected_etf_data.get('EXP_MACRO_RETURN', 5.0)) else 0.05
                            st.write(f"**Rendement Attendu:** {expected_ret*100:.1f}%")
                    
                    # Formulaire d'ajout
                
                    st.write(f"**Position pour:** {selected_etf_data['NOM']}")
                    
                    col_qty, col_price = st.columns(2)
                    with col_qty:
                        quantite_etf = st.number_input("Quantité", min_value=1, value=1, step=1, key="qty_etf")
                    with col_price:
                        prix_achat_etf = st.number_input("Prix d'achat (€)", min_value=0.01, value=100.0, step=1.0, key="price_etf")
                    
                    prix_actuel_etf = st.number_input("Prix actuel (€)", min_value=0.01, value=100.0, step=1.0, key="current_price_etf")
                    date_achat_etf = st.date_input("Date d'achat", value=date.today(), key="date_etf")
                    
                    # Calculs automatiques mis à jour en temps réel
                    cout_etf = quantite_etf * prix_achat_etf
                    valeur_etf = quantite_etf * prix_actuel_etf
                    pv_etf = valeur_etf - cout_etf
                    perf_etf = (pv_etf / cout_etf * 100) if cout_etf > 0 else 0
                    
                    st.write("**Calculs Automatiques**")
                    col1_calc, col2_calc = st.columns(2)
                    with col1_calc:
                        st.metric("Coût d'acquisition", format_currency(cout_etf))
                        st.metric("Valeur actuelle", format_currency(valeur_etf))
                    with col2_calc:
                        st.metric("Plus-value", format_currency(pv_etf), delta=f"{perf_etf:+.2f}%")
                        st.metric("Performance", f"{perf_etf:+.1f}%")
                    with st.form("add_etf_position", clear_on_submit=False):
                        submit_etf = st.form_submit_button("➕ Ajouter ETF au Portfolio", type="primary", use_container_width=True)
                        
                    # Traitement uniquement si bouton cliqué
                    if submit_etf:
                        nouvelle_position = {
                            'isin': selected_etf_data['ISIN'],
                            'nom': selected_etf_data['NOM'],
                            'provider': selected_etf_data.get('PROVIDER', 'N/A'),
                            'quantite': quantite_etf,
                            'prix_achat': prix_achat_etf,
                            'prix_actuel': prix_actuel_etf,
                            'cout_acquisition': cout_etf,
                            'valeur_actuelle': valeur_etf,
                            'date_achat': str(date_achat_etf),
                            'classe_1': selected_etf_data.get('CLASSE 1', 'N/A'),
                            'type': 'etf',
                            'frais': selected_etf_data.get('FRAIS DE GESTION', 0),
                            'expected_return': selected_etf_data.get('EXP_MACRO_RETURN', 5.0) / 100 if pd.notna(selected_etf_data.get('EXP_MACRO_RETURN', 5.0)) else 0.05,
                            'aum': selected_etf_data.get('ENCOURS SOUS GESTION (EUR)', 0),
                            'pea': selected_etf_data.get('PEA', 'N'),
                            'assvie': selected_etf_data.get('ASSVIE', 'N'),
                            'hedged': selected_etf_data.get('HEDGED', 'N')
                        }
                        st.session_state.portfolio.append(nouvelle_position)
                        
                        st.success(f"✅ Position ajoutée: {nouvelle_position['nom']}")
                        st.rerun()
            else:
                st.warning("Aucun ETF trouvé")

with tab2:
    st.subheader("⭐ Ajouter depuis Mon Univers")
    
    if not st.session_state.univers_etf:
        st.info("📭 Votre univers d'investissement est vide. Utilisez la page 'Recherche ETF' pour créer votre sélection d'ETFs favoris.")
        if st.button("🔍 Aller à la Recherche ETF"):
            st.switch_page("pages/3_Recherche_ETF.py")
    else:
        st.write(f"**{len(st.session_state.univers_etf)} ETF(s) dans votre univers**")
        
        # Sélectionner un ETF de l'univers
        univers_options = {}
        for i, etf in enumerate(st.session_state.univers_etf):
            key = f"{etf['nom']} ({etf['provider']}) - {etf['frais']:.2f}%"
            univers_options[key] = i
        
        selected_univers_key = st.selectbox("Choisir un ETF de votre univers", list(univers_options.keys()))
        selected_univers_idx = univers_options[selected_univers_key]
        selected_univers_etf = st.session_state.univers_etf[selected_univers_idx]
        
        # Afficher les informations détaillées
        with st.container():
            st.write("**📊 Informations Détaillées**")
            
            info_col1, info_col2, info_col3 = st.columns(3)
            
            with info_col1:
                st.write(f"**Fournisseur:** {selected_univers_etf['provider']}")
                st.write(f"**ISIN:** {selected_univers_etf['isin']}")
                st.write(f"**Classe:** {selected_univers_etf.get('classe_1', 'N/A')}")
            
            with info_col2:
                st.write(f"**Frais:** {selected_univers_etf.get('frais', 0):.2f}%")
                st.write(f"**AUM:** {selected_univers_etf.get('aum', 0):,.0f} M€".replace(',', ' '))
                st.write(f"**Rendement Attendu:** {selected_univers_etf.get('expected_return', 0.05)*100:.1f}%")
            
            with info_col3:
                st.write(f"**PEA:** {'✅ Oui' if selected_univers_etf.get('pea') == 'Y' else '❌ Non'}")
                st.write(f"**Assurance Vie:** {'✅ Oui' if selected_univers_etf.get('assvie') == 'Y' else '❌ Non'}")
                st.write(f"**Hedgé:** {'✅ Oui' if selected_univers_etf.get('hedged') == 'Y' else '❌ Non'}")
        
        # Formulaire d'ajout depuis l'univers
        
            st.write(f"**Ajouter une position:** {selected_univers_etf['nom']}")
            
            pos_col1, pos_col2 = st.columns(2)
            
            with pos_col1:
                quantite_univ = st.number_input("Quantité", min_value=1, value=1, step=1, key="qty_univ")
                prix_achat_univ = st.number_input("Prix d'achat (€)", min_value=0.01, value=100.0, step=1.0, key="price_univ")
            
            with pos_col2:
                prix_actuel_univ = st.number_input("Prix actuel (€)", min_value=0.01, value=100.0, step=1.0, key="current_price_univ")
                date_achat_univ = st.date_input("Date d'achat", value=date.today(), key="date_univ")
            
            # Calculs automatiques mis à jour en temps réel
            cout_univ = quantite_univ * prix_achat_univ
            valeur_univ = quantite_univ * prix_actuel_univ
            pv_univ = valeur_univ - cout_univ
            perf_univ = (pv_univ / cout_univ * 100) if cout_univ > 0 else 0
            
            st.write("**Résumé de la Position (Calcul automatique)**")
            calc_col1, calc_col2, calc_col3, calc_col4 = st.columns(4)
            
            with calc_col1:
                st.metric("Coût", format_currency(cout_univ))
            with calc_col2:
                st.metric("Valeur", format_currency(valeur_univ))
            with calc_col3:
                st.metric("Plus-value", format_currency(pv_univ))
            with calc_col4:
                st.metric("Performance", f"{perf_univ:+.1f}%", delta=f"{pv_univ:+.0f}€")
        with st.form("add_from_univers", clear_on_submit=False):
            submit_univers = st.form_submit_button("➕ Ajouter au Portfolio", type="primary", use_container_width=True)
            
        # Traitement uniquement si bouton cliqué
        if submit_univers:
            position_univers = {
                'isin': selected_univers_etf['isin'],
                'nom': selected_univers_etf['nom'],
                'provider': selected_univers_etf['provider'],
                'quantite': quantite_univ,
                'prix_achat': prix_achat_univ,
                'prix_actuel': prix_actuel_univ,
                'cout_acquisition': cout_univ,
                'valeur_actuelle': valeur_univ,
                'date_achat': str(date_achat_univ),
                'classe_1': selected_univers_etf.get('classe_1', 'N/A'),
                'type': 'etf',
                'frais': selected_univers_etf.get('frais', 0),
                'expected_return': selected_univers_etf.get('expected_return', 0.05),
                'aum': selected_univers_etf.get('aum', 0),
                'pea': selected_univers_etf.get('pea', 'N'),
                'assvie': selected_univers_etf.get('assvie', 'N'),
                'hedged': selected_univers_etf.get('hedged', 'N')
            }
            st.session_state.portfolio.append(position_univers)
            
            st.success(f"✅ Position ajoutée: {position_univers['nom']}")
            st.rerun()
            


with tab3:
    st.subheader("📋 Mes Positions Actuelles")
    
    if not st.session_state.portfolio:
        st.info("📭 Aucune position en portefeuille. Utilisez les onglets précédents pour ajouter des positions.")
    else:
        # Résumé du portefeuille
        total_cout = sum(pos['cout_acquisition'] for pos in st.session_state.portfolio)
        total_valeur = sum(pos['valeur_actuelle'] for pos in st.session_state.portfolio)
        total_plus_value = total_valeur - total_cout
        performance_globale = (total_plus_value / total_cout * 100) if total_cout > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Positions", len(st.session_state.portfolio))
        with col2:
            st.metric("Coût Total", format_currency(total_cout))
        with col3:
            st.metric("Valeur Actuelle", format_currency(total_valeur))
        with col4:
            st.metric("Performance", f"{performance_globale:+.2f}%")
        
        st.markdown("---")
        
        # Tableau détaillé des positions
        for i, position in enumerate(st.session_state.portfolio):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{position['nom']}**")
                    info_line = f"ISIN: {position['isin']} | {position['provider']}"
                    if position.get('type') == 'etf':
                        info_line += f" | Frais: {position.get('frais', 0):.2f}%"
                    st.write(info_line)
                
                with col2:
                    plus_value = position['valeur_actuelle'] - position['cout_acquisition']
                    performance = (plus_value / position['cout_acquisition'] * 100) if position['cout_acquisition'] > 0 else 0
                    
                    st.metric("Valeur", format_currency(position['valeur_actuelle']))
                    st.write(f"**Quantité:** {int(position['quantite'])}")  # Quantité sans décimale
                    st.write(f"**Performance:** {performance:+.2f}%")
                
                with col3:
                    if st.button("🗑️", key=f"delete_{i}", help="Supprimer"):
                        st.session_state.portfolio.pop(i)
                        st.rerun()
                
                # Détails expandables avec toutes les informations
                with st.expander("📊 Détails Complets"):
                    detail_col1, detail_col2, detail_col3 = st.columns(3)
                    
                    with detail_col1:
                        st.write("**📈 Données Financières**")
                        st.write(f"Prix d'achat: {format_currency(position['prix_achat'])}")
                        st.write(f"Prix actuel: {format_currency(position['prix_actuel'])}")
                        st.write(f"Plus-value: {format_currency(plus_value)}")
                        st.write(f"Date d'achat: {position['date_achat']}")
                    
                    with detail_col2:
                        st.write("**ℹ️ Informations ETF**")
                        if position.get('type') == 'etf':
                            st.write(f"AUM: {position.get('aum', 0):,.0f} M€".replace(',', ' '))
                            st.write(f"Rendement attendu: {position.get('expected_return', 0)*100:.1f}%")
                            st.write(f"PEA: {'✅ Oui' if position.get('pea') == 'Y' else '❌ Non'}")
                            st.write(f"Assurance Vie: {'✅ Oui' if position.get('assvie') == 'Y' else '❌ Non'}")
                            st.write(f"Hedgé: {'✅ Oui' if position.get('hedged') == 'Y' else '❌ Non'}")
                        else:
                            st.write("Actif manuel")
                            st.write(f"Rendement attendu: {position.get('expected_return', 0)*100:.1f}%")
                    
                    with detail_col3:
                        st.write("**🏷️ Classification**")
                        st.write(f"Classe: {position.get('classe_1', 'N/A')}")
                        st.write(f"Type: {position.get('type', 'N/A').title()}")
                
                st.markdown("---")

with tab4:
    st.subheader("📤 Import/Export du Portfolio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Exporter le Portfolio**")
        
        if st.session_state.portfolio:
            export_data = pd.DataFrame(st.session_state.portfolio)
            csv_data = export_data.to_csv(index=False)
            
            st.download_button(
                label="💾 Télécharger en CSV",
                data=csv_data,
                file_name=f"portfolio_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            st.write(f"**{len(st.session_state.portfolio)}** positions à exporter")
        else:
            st.info("Aucune position à exporter")
    
    with col2:
        st.write("**Importer un Portfolio**")
        
        uploaded_file = st.file_uploader(
            "Choisir un fichier CSV",
            type=['csv'],
            help="Format: isin, nom, quantite, prix_achat, prix_actuel, date_achat"
        )
        
        if uploaded_file is not None:
            try:
                import_df = pd.read_csv(uploaded_file)
                
                required_cols = ['isin', 'nom', 'quantite', 'prix_achat', 'prix_actuel']
                missing_cols = [col for col in required_cols if col not in import_df.columns]
                
                if missing_cols:
                    st.error(f"Colonnes manquantes: {', '.join(missing_cols)}")
                else:
                    st.write("**Aperçu des données**")
                    st.dataframe(import_df.head())
                    
                    if st.button("📥 Importer ces données"):
                        for _, row in import_df.iterrows():
                            position = {
                                'isin': row['isin'],
                                'nom': row['nom'],
                                'provider': row.get('provider', 'N/A'),
                                'quantite': float(row['quantite']),
                                'prix_achat': float(row['prix_achat']),
                                'prix_actuel': float(row['prix_actuel']),
                                'cout_acquisition': float(row['quantite']) * float(row['prix_achat']),
                                'valeur_actuelle': float(row['quantite']) * float(row['prix_actuel']),
                                'date_achat': row.get('date_achat', str(date.today())),
                                'classe_1': row.get('classe_1', 'N/A'),
                                'type': row.get('type', 'etf'),
                                'frais': row.get('frais', 0.0),
                                'expected_return': row.get('expected_return', 0.05)
                            }
                            st.session_state.portfolio.append(position)
    
                        
                        st.success(f"✅ {len(import_df)} positions importées!")
                        st.rerun()
            
            except Exception as e:
                st.error(f"Erreur lors de l'import: {e}")

# Actions globales
if st.session_state.portfolio:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Voir Dashboard", type="primary"):
            st.switch_page("pages/1_Dashboard.py")
    
    with col2:
        if st.button("🗑️ Vider Portfolio", type="secondary"):
            if st.checkbox("⚠️ Confirmer suppression complète"):
                st.session_state.portfolio = []
                st.success("Portfolio vidé!")
                st.rerun()