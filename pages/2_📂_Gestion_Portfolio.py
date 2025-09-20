"""
Gestion Portfolio - Import/Export, création manuelle et templates
Interface complète pour gérer les actifs du portefeuille
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import io
from utils_categories import calculate_portfolio_metrics, format_currency, format_percentage

# Configuration de la page
st.set_page_config(
    page_title="Gestion Portfolio - Portfolio Manager Pro",
    page_icon="📂",
    layout="wide"
)

# CSS pour la page de gestion
st.markdown("""
<style>
    /* Onglets stylisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }

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

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        background: var(--card-bg);
        border-radius: 15px 15px 0 0;
        border: 1px solid var(--border-color);
        padding: 0 2rem;
        font-weight: 600;
        color: var(--text-secondary);
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }

    /* Template cards */
    .template-card {
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        color: var(--text-primary);
    }

    .template-card:hover {
        border-color: #667eea;
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }

    .template-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }

    .template-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .template-description {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.4;
    }

    /* Formulaire de création */
    .form-section {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: var(--card-shadow);
        margin-bottom: 2rem;
        color: var(--text-primary);
    }

    .form-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Zone d'upload */
    .upload-zone {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        background: #f8f9ff;
        margin: 1rem 0;
    }

    .upload-icon {
        font-size: 4rem;
        color: #667eea;
        margin-bottom: 1rem;
    }

    .upload-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .upload-subtitle {
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
    }

    /* Portfolio items */
    .portfolio-item {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        color: var(--text-primary);
    }

    .portfolio-item:hover {
        border-color: #667eea;
        box-shadow: var(--card-shadow);
    }

    .item-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }

    .item-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.5rem;
        font-size: 0.9rem;
        color: #6c757d;
    }

    /* Actions buttons */
    .action-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .action-btn {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.85rem;
    }

    .btn-danger {
        background: #dc3545;
        color: white;
    }

    .btn-danger:hover {
        background: #c82333;
    }

    .btn-warning {
        background: #ffc107;
        color: #212529;
    }

    .btn-warning:hover {
        background: #e0a800;
    }

    /* Success/error messages */
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }

    .error-msg {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .item-details {
            grid-template-columns: 1fr;
        }
        
        .action-buttons {
            flex-direction: column;
        }
        
        .upload-zone {
            padding: 2rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def create_template_portfolio(template_type="examples"):
    """Crée un template de portefeuille"""
    if template_type == "examples":
        # Template avec exemples
        return pd.DataFrame([
            {
                'Type': 'ETF',
                'Nom': 'iShares Core S&P 500 UCITS ETF',
                'ISIN': 'IE00B5BMR087',
                'Quantité': 10,
                'Prix_Achat': 400.00,
                'Prix_Actuel': 420.50,
                'Date_Achat': '2023-01-15'
            },
            {
                'Type': 'Action',
                'Nom': 'Apple Inc.',
                'ISIN': 'US0378331005',
                'Quantité': 5,
                'Prix_Achat': 150.00,
                'Prix_Actuel': 175.25,
                'Date_Achat': '2023-03-10'
            },
            {
                'Type': 'ETF',
                'Nom': 'Vanguard FTSE Europe UCITS ETF',
                'ISIN': 'IE00B945VV12',
                'Quantité': 15,
                'Prix_Achat': 28.50,
                'Prix_Actuel': 31.20,
                'Date_Achat': '2023-02-20'
            },
            {
                'Type': 'Crypto',
                'Nom': 'Bitcoin ETF',
                'ISIN': 'XS2399364982',
                'Quantité': 2,
                'Prix_Achat': 45000.00,
                'Prix_Actuel': 52000.00,
                'Date_Achat': '2023-04-01'
            }
        ])
    else:
        # Template vide
        return pd.DataFrame(columns=[
            'Type', 'Nom', 'ISIN', 'Quantité', 'Prix_Achat', 'Prix_Actuel', 'Date_Achat'
        ])

def calculate_portfolio_fields(df):
    """Calcule les champs dérivés du portefeuille"""
    if df.empty:
        return df
    
    df = df.copy()
    
    # Convertir les types
    numeric_cols = ['Quantité', 'Prix_Achat', 'Prix_Actuel']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculs
    df['Valeur_Achat'] = df['Quantité'] * df['Prix_Achat']
    df['Valeur_Actuelle'] = df['Quantité'] * df['Prix_Actuel']
    df['Plus_Value'] = df['Valeur_Actuelle'] - df['Valeur_Achat']
    df['Performance_%'] = ((df['Prix_Actuel'] - df['Prix_Achat']) / df['Prix_Achat']) * 100
    
    # Nettoyer les NaN
    df = df.fillna(0)
    
    return df

def validate_portfolio_data(df):
    """Valide les données du portefeuille"""
    errors = []
    
    # Colonnes obligatoires
    required_cols = ['Type', 'Nom', 'Quantité', 'Prix_Achat', 'Date_Achat']
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Colonne manquante: {col}")
    
    if errors:
        return False, errors
    
    # Validation des données
    for idx, row in df.iterrows():
        if pd.isna(row['Nom']) or row['Nom'] == '':
            errors.append(f"Ligne {idx+1}: Nom requis")
        
        if pd.isna(row['Quantité']) or row['Quantité'] <= 0:
            errors.append(f"Ligne {idx+1}: Quantité doit être > 0")
        
        if pd.isna(row['Prix_Achat']) or row['Prix_Achat'] <= 0:
            errors.append(f"Ligne {idx+1}: Prix d'achat doit être > 0")
    
    return len(errors) == 0, errors

def process_uploaded_file(uploaded_file):
    """Traite le fichier uploadé"""
    try:
        # Lire selon l'extension
        if uploaded_file.name.endswith('.csv'):
            # Essayer différents séparateurs
            content = uploaded_file.read().decode('utf-8-sig')
            if ';' in content:
                df = pd.read_csv(io.StringIO(content), sep=';')
            else:
                df = pd.read_csv(io.StringIO(content), sep=',')
        else:
            df = pd.read_excel(uploaded_file)
        
        return df, None
        
    except Exception as e:
        return None, f"Erreur lors de la lecture du fichier: {str(e)}"

def render_portfolio_item(idx, row):
    """Affiche un élément du portefeuille"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Calculer les métriques
        valeur_actuelle = row.get('Valeur_Actuelle', 0)
        plus_value = row.get('Plus_Value', 0)
        performance = row.get('Performance_%', 0)
        
        performance_color = "🟢" if performance >= 0 else "🔴"
        
        st.markdown(f"""
        <div class="portfolio-item">
            <div class="item-header">
                <span>{row.get('Type', 'N/A')} - {row.get('Nom', 'N/A')}</span>
                <span>{performance_color} {performance:.1f}%</span>
            </div>
            <div class="item-details">
                <div><strong>ISIN:</strong> {row.get('ISIN', 'N/A')}</div>
                <div><strong>Quantité:</strong> {int(row.get('Quantité', 0))}</div>
                <div><strong>Prix achat:</strong> {row.get('Prix_Achat', 0):.2f} €</div>
                <div><strong>Prix actuel:</strong> {row.get('Prix_Actuel', 0):.2f} €</div>
                <div><strong>Valeur:</strong> {valeur_actuelle:,.2f} €</div>
                <div><strong>+/-:</strong> {plus_value:,.2f} €</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️", key=f"delete_{idx}", help="Supprimer cet actif"):
            return True  # Signal de suppression
    
    return False

def main():
    """Fonction principale de la page de gestion"""
    
    st.title("📂 Gestion Portfolio")
    st.markdown("Import/Export, création manuelle et gestion de vos actifs")
    
    # Initialisation du session state
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = pd.DataFrame()
    
    # Interface à onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Ajout d'actif", "📥 Import", "📊 Export", "⚙️ Gestion"])
    
    # ONGLET AJOUT D'ACTIF
    with tab1:
        st.markdown("### 📋 Ajout d'Actif au Portefeuille")
        st.markdown("Choisissez votre méthode préférée pour ajouter des actifs à votre portefeuille")
        
        # Sélection du mode d'ajout
        add_mode = st.radio(
            "**Comment souhaitez-vous ajouter l'actif ?**",
            ["🌟 Depuis l'univers ETF", "🔍 Rechercher un ETF par nom", "✏️ Saisie manuelle"],
            horizontal=True
        )
        
        st.markdown("---")
        
        # MODE 1: Depuis l'univers ETF
        if add_mode == "🌟 Depuis l'univers ETF":
            st.markdown("#### 🌟 Sélection depuis votre Univers ETF")
            
            # Vérifier si un univers ETF existe
            if 'univers_etf' not in st.session_state or st.session_state.univers_etf.empty:
                st.warning("❌ Aucun ETF dans votre univers d'investissement.")
                st.markdown("""
                **Pour utiliser cette fonctionnalité :**
                1. Allez sur la page **🔍 Recherche ETF**
                2. Sélectionnez les ETF qui vous intéressent
                3. Ajoutez-les à votre univers avec le bouton **➕ Ajouter**
                4. Revenez ici pour les ajouter à votre portefeuille
                """)
                
                if st.button("🔍 Aller à la Recherche ETF"):
                    st.switch_page("pages/3_🔍_Recherche_ETF.py")
            else:
                # Sélection d'un ETF de l'univers
                etf_options = [f"{row['NOM']} ({row['PROVIDER']}) - {row['ISIN']}" 
                              for _, row in st.session_state.univers_etf.iterrows()]
                
                selected_etf_idx = st.selectbox(
                    "Sélectionnez un ETF de votre univers:",
                    range(len(etf_options)),
                    format_func=lambda x: etf_options[x]
                )
                
                selected_etf_data = st.session_state.univers_etf.iloc[selected_etf_idx]
                
                # Formulaire pour les détails de l'achat
                with st.form("add_from_universe"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Détails de l'ETF sélectionné:**")
                        st.write(f"**Nom:** {selected_etf_data['NOM']}")
                        st.write(f"**ISIN:** {selected_etf_data['ISIN']}")
                        st.write(f"**Provider:** {selected_etf_data['PROVIDER']}")
                        
                        quantity = st.number_input(
                            "Quantité *",
                            min_value=0.0001,
                            value=1.0,
                            step=0.1,
                            help="Nombre de parts à acheter"
                        )
                        
                        purchase_date = st.date_input(
                            "Date d'achat *",
                            value=date.today(),
                            help="Date d'acquisition"
                        )
                    
                    with col2:
                        purchase_price = st.number_input(
                            "Prix d'achat (€/part) *",
                            min_value=0.01,
                            value=50.0,
                            step=0.01,
                            help="Prix d'achat par part"
                        )
                        
                        current_price = st.number_input(
                            "Prix actuel (€/part) *",
                            min_value=0.01,
                            value=50.0,
                            step=0.01,
                            help="Prix actuel par part"
                        )
                    
                    # Calculs automatiques
                    if quantity > 0 and purchase_price > 0:
                        purchase_value = quantity * purchase_price
                        current_value = quantity * current_price
                        capital_gain = current_value - purchase_value
                        performance = ((current_price - purchase_price) / purchase_price) * 100
                        
                        st.markdown("#### 📊 Calculs Automatiques")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Valeur d'achat", f"{purchase_value:,.2f} €")
                        with col2:
                            st.metric("Valeur actuelle", f"{current_value:,.2f} €")
                        with col3:
                            st.metric("Plus-value", f"{capital_gain:,.2f} €")
                        with col4:
                            st.metric("Performance", f"{performance:+.1f}%")
                    
                    submitted = st.form_submit_button("➕ Ajouter l'ETF au portefeuille", type="primary")
                    
                    if submitted:
                        if quantity <= 0 or purchase_price <= 0 or current_price <= 0:
                            st.error("❌ Veuillez remplir tous les champs obligatoires avec des valeurs > 0")
                        else:
                            # Créer le nouvel actif
                            new_asset = pd.DataFrame([{
                                'Type': 'ETF',
                                'Nom': selected_etf_data['NOM'],
                                'ISIN': selected_etf_data['ISIN'],
                                'Quantité': quantity,
                                'Prix_Achat': purchase_price,
                                'Prix_Actuel': current_price,
                                'Date_Achat': purchase_date.strftime('%Y-%m-%d')
                            }])
                            
                            # Calculer les champs dérivés
                            new_asset = calculate_portfolio_fields(new_asset)
                            
                            # Ajouter au portefeuille
                            if st.session_state.portfolio.empty:
                                st.session_state.portfolio = new_asset
                            else:
                                st.session_state.portfolio = pd.concat([
                                    st.session_state.portfolio, new_asset
                                ], ignore_index=True)
                            
                            st.success(f"✅ ETF '{selected_etf_data['NOM']}' ajouté avec succès !")
                            st.rerun()
        
        # MODE 2: Recherche ETF par nom
        elif add_mode == "🔍 Rechercher un ETF par nom":
            st.markdown("#### 🔍 Recherche d'ETF par Nom")
            
            # Charger la base ETF si disponible
            try:
                df_etf = pd.read_excel('data/etf_base_assets.xlsx')
                
                search_term = st.text_input(
                    "Rechercher un ETF:",
                    placeholder="Tapez le nom de l'ETF...",
                    help="Recherche dans les noms d'ETF de la base de données"
                )
                
                if search_term and len(search_term) >= 3:
                    # Filtrer les ETF correspondants
                    filtered_etfs = df_etf[
                        df_etf['NOM'].str.contains(search_term, case=False, na=False)
                    ].head(10)  # Limiter à 10 résultats
                    
                    if not filtered_etfs.empty:
                        # Afficher les options
                        etf_search_options = [
                            f"{row['NOM']} ({row.get('PROVIDER', 'N/A')}) - {row['ISIN']}"
                            for _, row in filtered_etfs.iterrows()
                        ]
                        
                        selected_search_idx = st.selectbox(
                            "Sélectionnez l'ETF:",
                            range(len(etf_search_options)),
                            format_func=lambda x: etf_search_options[x]
                        )
                        
                        selected_search_data = filtered_etfs.iloc[selected_search_idx]
                        
                        # Formulaire pour les détails
                        with st.form("add_from_search"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Détails de l'ETF sélectionné:**")
                                st.write(f"**Nom:** {selected_search_data['NOM']}")
                                st.write(f"**ISIN:** {selected_search_data['ISIN']}")
                                st.write(f"**Provider:** {selected_search_data.get('PROVIDER', 'N/A')}")
                                if 'FRAIS DE GESTION' in selected_search_data:
                                    st.write(f"**Frais:** {selected_search_data['FRAIS DE GESTION']:.2f}%")
                                
                                quantity = st.number_input(
                                    "Quantité *",
                                    min_value=0.0001,
                                    value=1.0,
                                    step=0.1,
                                    key="search_quantity"
                                )
                                
                                purchase_date = st.date_input(
                                    "Date d'achat *",
                                    value=date.today(),
                                    key="search_date"
                                )
                            
                            with col2:
                                purchase_price = st.number_input(
                                    "Prix d'achat (€/part) *",
                                    min_value=0.01,
                                    value=50.0,
                                    step=0.01,
                                    key="search_purchase_price"
                                )
                                
                                current_price = st.number_input(
                                    "Prix actuel (€/part) *",
                                    min_value=0.01,
                                    value=50.0,
                                    step=0.01,
                                    key="search_current_price"
                                )
                            
                            # Calculs automatiques
                            if quantity > 0 and purchase_price > 0:
                                purchase_value = quantity * purchase_price
                                current_value = quantity * current_price
                                capital_gain = current_value - purchase_value
                                performance = ((current_price - purchase_price) / purchase_price) * 100
                                
                                st.markdown("#### 📊 Calculs Automatiques")
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("Valeur d'achat", f"{purchase_value:,.2f} €")
                                with col2:
                                    st.metric("Valeur actuelle", f"{current_value:,.2f} €")
                                with col3:
                                    st.metric("Plus-value", f"{capital_gain:,.2f} €")
                                with col4:
                                    st.metric("Performance", f"{performance:+.1f}%")
                            
                            submitted = st.form_submit_button("➕ Ajouter l'ETF au portefeuille", type="primary")
                            
                            if submitted:
                                if quantity <= 0 or purchase_price <= 0 or current_price <= 0:
                                    st.error("❌ Veuillez remplir tous les champs obligatoires avec des valeurs > 0")
                                else:
                                    # Créer le nouvel actif
                                    new_asset = pd.DataFrame([{
                                        'Type': 'ETF',
                                        'Nom': selected_search_data['NOM'],
                                        'ISIN': selected_search_data['ISIN'],
                                        'Quantité': quantity,
                                        'Prix_Achat': purchase_price,
                                        'Prix_Actuel': current_price,
                                        'Date_Achat': purchase_date.strftime('%Y-%m-%d')
                                    }])
                                    
                                    # Calculer les champs dérivés
                                    new_asset = calculate_portfolio_fields(new_asset)
                                    
                                    # Ajouter au portefeuille
                                    if st.session_state.portfolio.empty:
                                        st.session_state.portfolio = new_asset
                                    else:
                                        st.session_state.portfolio = pd.concat([
                                            st.session_state.portfolio, new_asset
                                        ], ignore_index=True)
                                    
                                    st.success(f"✅ ETF '{selected_search_data['NOM']}' ajouté avec succès !")
                                    st.rerun()
                    else:
                        st.info("Aucun ETF trouvé avec ce terme de recherche.")
                
            except Exception as e:
                st.error(f"Erreur lors du chargement de la base ETF: {e}")
        
        # MODE 3: Saisie manuelle
        else:  # add_mode == "✏️ Saisie manuelle"
            st.markdown("#### ✏️ Saisie Manuelle d'Actif")
            
            with st.form("add_manual_asset"):
                col1, col2 = st.columns(2)
                
                with col1:
                    asset_type = st.selectbox(
                        "Type d'actif *",
                        ["ETF", "Action", "Obligation", "Crypto", "Autre"],
                        help="Catégorie de l'actif"
                    )
                    
                    asset_name = st.text_input(
                        "Nom de l'actif *",
                        help="Nom complet de l'actif"
                    )
                    
                    asset_isin = st.text_input(
                        "ISIN (optionnel)",
                        help="Code ISIN de l'actif"
                    )
                    
                    quantity = st.number_input(
                        "Quantité *",
                        min_value=0.0001,
                        value=1.0,
                        step=0.1,
                        help="Nombre d'unités détenues",
                        key="manual_quantity"
                    )
                    
                    purchase_date = st.date_input(
                        "Date d'achat *",
                        value=date.today(),
                        help="Date d'acquisition de l'actif",
                        key="manual_date"
                    )
                
                with col2:
                    purchase_price = st.number_input(
                        "Prix d'achat *",
                        min_value=0.01,
                        value=100.0,
                        step=0.01,
                        help="Prix d'achat unitaire en €",
                        key="manual_purchase_price"
                    )
                    
                    current_price = st.number_input(
                        "Prix actuel *",
                        min_value=0.01,
                        value=100.0,
                        step=0.01,
                        help="Prix actuel unitaire en €",
                        key="manual_current_price"
                    )
                
                # Calculs automatiques
                if quantity > 0 and purchase_price > 0:
                    purchase_value = quantity * purchase_price
                    current_value = quantity * current_price
                    capital_gain = current_value - purchase_value
                    performance = ((current_price - purchase_price) / purchase_price) * 100
                    
                    st.markdown("#### 📊 Calculs Automatiques")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Valeur d'achat", f"{purchase_value:,.2f} €")
                    with col2:
                        st.metric("Valeur actuelle", f"{current_value:,.2f} €")
                    with col3:
                        st.metric("Plus-value", f"{capital_gain:,.2f} €")
                    with col4:
                        st.metric("Performance", f"{performance:+.1f}%")
                
                submitted = st.form_submit_button("➕ Ajouter l'actif au portefeuille", type="primary")
                
                if submitted:
                    if not asset_name or quantity <= 0 or purchase_price <= 0 or current_price <= 0:
                        st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
                    else:
                        # Créer le nouvel actif
                        new_asset = pd.DataFrame([{
                            'Type': asset_type,
                            'Nom': asset_name,
                            'ISIN': asset_isin if asset_isin else '',
                            'Quantité': quantity,
                            'Prix_Achat': purchase_price,
                            'Prix_Actuel': current_price,
                            'Date_Achat': purchase_date.strftime('%Y-%m-%d')
                        }])
                        
                        # Calculer les champs dérivés
                        new_asset = calculate_portfolio_fields(new_asset)
                        
                        # Ajouter au portefeuille
                        if st.session_state.portfolio.empty:
                            st.session_state.portfolio = new_asset
                        else:
                            st.session_state.portfolio = pd.concat([
                                st.session_state.portfolio, new_asset
                            ], ignore_index=True)
                        
                        st.success(f"✅ Actif '{asset_name}' ajouté avec succès !")
                        st.rerun()

    # ONGLET IMPORT
    with tab2:
        st.markdown("### 📥 Import de Portefeuille")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="upload-zone">
                <div class="upload-icon">📁</div>
                <div class="upload-title">Importer vos données</div>
                <div class="upload-subtitle">
                    Formats supportés: CSV, Excel<br>
                    Colonnes obligatoires: <strong>Type, Nom, Quantité, Prix_Achat, Date_Achat</strong><br>
                    Colonnes optionnelles: <strong>ISIN, Prix_Actuel</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choisir un fichier",
                type=['csv', 'xlsx', 'xls'],
                help="Le fichier doit contenir au minimum: Type, Nom, Quantité, Prix_Achat, Date_Achat"
            )
            
            if uploaded_file:
                df_uploaded, error = process_uploaded_file(uploaded_file)
                
                if error:
                    st.error(error)
                else:
                    # Validation
                    is_valid, validation_errors = validate_portfolio_data(df_uploaded)
                    
                    if not is_valid:
                        st.error("Erreurs de validation:")
                        for error in validation_errors:
                            st.write(f"❌ {error}")
                    else:
                        # Calculer les champs dérivés
                        df_processed = calculate_portfolio_fields(df_uploaded)
                        
                        st.success("✅ Fichier validé avec succès !")
                        st.markdown("**Aperçu des données:**")
                        st.dataframe(df_processed.head(), use_container_width=True)
                        
                        # Mode d'import
                        import_mode = st.radio(
                            "Mode d'import:",
                            ["Remplacer le portefeuille existant", "Ajouter au portefeuille existant"],
                            help="Choisir comment traiter les données importées"
                        )
                        
                        if st.button("✅ Confirmer l'import", type="primary"):
                            if import_mode == "Remplacer le portefeuille existant":
                                st.session_state.portfolio = df_processed
                                st.success(f"✅ Portefeuille remplacé ! {len(df_processed)} actifs importés.")
                            else:
                                if st.session_state.portfolio.empty:
                                    st.session_state.portfolio = df_processed
                                else:
                                    st.session_state.portfolio = pd.concat([
                                        st.session_state.portfolio, df_processed
                                    ], ignore_index=True)
                                st.success(f"✅ {len(df_processed)} actifs ajoutés au portefeuille !")
                            
                            st.rerun()
        
        with col2:
            st.markdown("### 📋 Templates")
            
            # Template avec exemples
            st.markdown("""
            <div class="template-card">
                <div class="template-icon">🎯</div>
                <div class="template-title">Template avec Exemples</div>
                <div class="template-description">
                    Portefeuille pré-rempli avec 4 actifs d'exemple
                    (ETF, Action, Crypto)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📥 Télécharger avec exemples", key="template_examples"):
                template_df = create_template_portfolio("examples")
                csv = template_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="💾 Télécharger CSV",
                    data=csv,
                    file_name="template_portfolio_exemples.csv",
                    mime="text/csv"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Template vide
            st.markdown("""
            <div class="template-card">
                <div class="template-icon">📄</div>
                <div class="template-title">Template Vide</div>
                <div class="template-description">
                    Structure vide prête à être remplie avec vos données
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📥 Télécharger vide", key="template_empty"):
                template_df = create_template_portfolio("empty")
                csv = template_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="💾 Télécharger CSV",
                    data=csv,
                    file_name="template_portfolio_vide.csv",
                    mime="text/csv"
                )
    
    # ONGLET IMPORT (maintenant tab2)
    with tab2:
        st.markdown("### � Import de Portefeuille")
        
        st.markdown("""
        <div class="form-section">
            <div class="form-title">➕ Ajouter un nouvel actif</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("add_asset_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                asset_type = st.selectbox(
                    "Type d'actif *",
                    ["ETF", "Action", "Obligation", "Crypto", "Autre"],
                    help="Catégorie de l'actif"
                )
                
                asset_name = st.text_input(
                    "Nom de l'actif *",
                    help="Nom complet de l'actif"
                )
                
                asset_isin = st.text_input(
                    "ISIN (optionnel)",
                    help="Code ISIN de l'actif"
                )
                
                quantity = st.number_input(
                    "Quantité *",
                    min_value=0.0001,
                    value=1.0,
                    step=0.1,
                    help="Nombre d'unités détenues"
                )
            
            with col2:
                purchase_price = st.number_input(
                    "Prix d'achat *",
                    min_value=0.01,
                    value=100.0,
                    step=0.01,
                    help="Prix d'achat unitaire en €"
                )
                
                current_price = st.number_input(
                    "Prix actuel",
                    min_value=0.01,
                    value=100.0,
                    step=0.01,
                    help="Prix actuel unitaire en € (par défaut = prix d'achat)"
                )
                
                purchase_date = st.date_input(
                    "Date d'achat *",
                    value=date.today(),
                    help="Date d'acquisition de l'actif"
                )
            
            # Calculs automatiques
            if quantity > 0 and purchase_price > 0:
                purchase_value = quantity * purchase_price
                current_value = quantity * current_price
                capital_gain = current_value - purchase_value
                performance = ((current_price - purchase_price) / purchase_price) * 100
                
                st.markdown("#### 📊 Calculs Automatiques")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Valeur d'achat", f"{purchase_value:,.2f} €")
                with col2:
                    st.metric("Valeur actuelle", f"{current_value:,.2f} €")
                with col3:
                    st.metric("Plus-value", f"{capital_gain:,.2f} €")
                with col4:
                    st.metric("Performance", f"{performance:+.1f}%")
            
            submitted = st.form_submit_button("➕ Ajouter l'actif", type="primary")
            
            if submitted:
                if not asset_name or quantity <= 0 or purchase_price <= 0:
                    st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
                else:
                    # Créer le nouvel actif
                    new_asset = pd.DataFrame([{
                        'Type': asset_type,
                        'Nom': asset_name,
                        'ISIN': asset_isin if asset_isin else '',
                        'Quantité': quantity,
                        'Prix_Achat': purchase_price,
                        'Prix_Actuel': current_price,
                        'Date_Achat': purchase_date.strftime('%Y-%m-%d')
                    }])
                    
                    # Calculer les champs dérivés
                    new_asset = calculate_portfolio_fields(new_asset)
                    
                    # Ajouter au portefeuille
                    if st.session_state.portfolio.empty:
                        st.session_state.portfolio = new_asset
                    else:
                        st.session_state.portfolio = pd.concat([
                            st.session_state.portfolio, new_asset
                        ], ignore_index=True)
                    
                    st.success(f"✅ Actif '{asset_name}' ajouté avec succès !")
                    st.rerun()
    
    # ONGLET EXPORT
    with tab3:
        st.markdown("### 📊 Export du Portefeuille")
        
        if st.session_state.portfolio.empty:
            st.warning("❌ Aucun portefeuille à exporter. Créez ou importez d'abord un portefeuille.")
        else:
            # Métriques du portefeuille
            metrics = calculate_portfolio_metrics(st.session_state.portfolio)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nombre d'actifs", metrics['nombre_actifs'])
            with col2:
                st.metric("Valeur totale", format_currency(metrics['valeur_totale']))
            with col3:
                st.metric("Performance globale", format_percentage(metrics['performance_globale']))
            
            st.markdown("---")
            
            # Options d'export
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📥 Export Complet")
                st.write("Téléchargez votre portefeuille avec toutes les données calculées")
                
                # Générer le CSV
                csv_data = st.session_state.portfolio.to_csv(index=False, encoding='utf-8-sig')
                
                st.download_button(
                    label="📥 Télécharger Portfolio Complet",
                    data=csv_data,
                    file_name=f"portfolio_complet_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    help="Export avec toutes les colonnes calculées"
                )
            
            with col2:
                st.markdown("#### 🔄 Template Prix")
                st.write("Template pour la mise à jour des prix")
                
                # Template pour mise à jour des prix
                if 'Nom' in st.session_state.portfolio.columns and 'ISIN' in st.session_state.portfolio.columns:
                    template_prix = st.session_state.portfolio[['Nom', 'ISIN', 'Prix_Actuel']].copy()
                    template_prix = template_prix.rename(columns={'Prix_Actuel': 'Nouveau_Prix'})
                    
                    csv_template = template_prix.to_csv(index=False, encoding='utf-8-sig')
                    
                    st.download_button(
                        label="📥 Template Prix",
                        data=csv_template,
                        file_name=f"template_prix_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Pour mettre à jour les prix dans le dashboard"
                    )
            
            # Aperçu des données
            st.markdown("#### 👀 Aperçu des Données")
            st.dataframe(st.session_state.portfolio, use_container_width=True, hide_index=True)
    
    # ONGLET GESTION
    with tab4:
        st.markdown("### ⚙️ Gestion du Portefeuille")
        
        if st.session_state.portfolio.empty:
            st.info("📝 Aucun actif dans le portefeuille. Utilisez les onglets précédents pour en ajouter.")
        else:
            # Actions globales
            st.markdown("#### 🎛️ Actions Globales")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Vider le portefeuille", help="Supprimer tous les actifs"):
                    st.session_state.show_confirm_clear = True
            
            with col2:
                if st.button("📊 Voir Dashboard", help="Aller au dashboard"):
                    st.switch_page("pages/1_📈_Dashboard.py")
            
            with col3:
                metrics = calculate_portfolio_metrics(st.session_state.portfolio)
                st.metric("Total actifs", metrics['nombre_actifs'])
            
            # Confirmation de suppression globale
            if st.session_state.get('show_confirm_clear', False):
                st.warning("⚠️ Êtes-vous sûr de vouloir supprimer tous les actifs ?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Confirmer", type="primary"):
                        st.session_state.portfolio = pd.DataFrame()
                        st.session_state.show_confirm_clear = False
                        st.success("✅ Portefeuille vidé !")
                        st.rerun()
                with col2:
                    if st.button("❌ Annuler"):
                        st.session_state.show_confirm_clear = False
                        st.rerun()
            
            st.markdown("---")
            
            # Liste détaillée des actifs
            st.markdown("#### 📋 Liste Détaillée des Actifs")
            
            # Affichage des actifs avec possibilité de suppression
            assets_to_delete = []
            
            for idx, row in st.session_state.portfolio.iterrows():
                should_delete = render_portfolio_item(idx, row)
                if should_delete:
                    assets_to_delete.append(idx)
            
            # Supprimer les actifs marqués pour suppression
            if assets_to_delete:
                st.session_state.portfolio = st.session_state.portfolio.drop(assets_to_delete).reset_index(drop=True)
                st.success(f"✅ {len(assets_to_delete)} actif(s) supprimé(s) !")
                st.rerun()

if __name__ == "__main__":
    # Initialisation du session state
    if 'show_confirm_clear' not in st.session_state:
        st.session_state.show_confirm_clear = False
    
    main()