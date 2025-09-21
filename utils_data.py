"""
Utilitaires de données pour Portfolio Manager Pro MVP
Fonctions simplifiées pour charger et manipuler les données ETF
"""

import pandas as pd
import streamlit as st
import os
from typing import Dict, List, Optional

@st.cache_data
def load_etf_data() -> pd.DataFrame:
    """
    Charge les données ETF depuis le fichier Excel
    
    Returns:
        DataFrame avec les données ETF
    """
    try:
        etf_path = "data/etf_base_assets.xlsx"
        if os.path.exists(etf_path):
            df = pd.read_excel(etf_path)
            # Colonnes essentielles pour le MVP
            essential_cols = [
                'ISIN', 'NOM', 'PROVIDER', 'FRAIS DE GESTION', 
                'ENCOURS SOUS GESTION (EUR)', 'CLASSE 1', 'CLASSE 2', 'CLASSE 3',
                'PEA', 'ASSVIE', 'HEDGED', 'DEVISE ETF', 'EXP_MACRO_RETURN', 
                'SFDR', 'LIEN', 'CLASSE 4', 'CLASSE 5', 'Asset_Class', 'Asset_Geo_Area',
                'XTB', 'ING', 'SCALABLE', 'EASYBOURSE', 'BOURSO', 'BOURSEDIRECT', 'ETORO'
            ]
            # Garder seulement les colonnes essentielles qui existent
            available_cols = [col for col in essential_cols if col in df.columns]
            result_df = df[available_cols].copy()
            
            # Nettoyer les données
            # Convertir les valeurs manquantes en chaînes pour éviter les erreurs
            for col in ['PEA', 'ASSVIE', 'HEDGED']:
                if col in result_df.columns:
                    result_df[col] = result_df[col].fillna('N').astype(str)
            
            return result_df
        else:
            st.error("Fichier des données ETF non trouvé")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données ETF: {e}")
        return pd.DataFrame()

@st.cache_data
def load_category_mapping() -> pd.DataFrame:
    """
    Charge le mapping des catégories ETF
    
    Returns:
        DataFrame avec les mappings des catégories
    """
    try:
        mapping_path = "mapping_categories_etf.csv"
        if os.path.exists(mapping_path):
            return pd.read_csv(mapping_path, encoding='utf-8')
        else:
            # Mapping par défaut
            default_mapping = pd.DataFrame({
                'CLASSE': ['CLASSE 1', 'CLASSE 1', 'CLASSE 1'],
                'CATEGORIE_ORIGINALE': ['equities', 'bonds', 'cash','commodities','securitized'],
                'CATEGORIE_LISIBLE': ['Actions', 'Obligations', 'Monétaire', 'Matières Premières', 'Titrisé'],
                'DESCRIPTION': [
                    'Investissement en actions d\'entreprises',
                    'Titres de créance à revenus fixes',
                    'Instruments du marché monétaire',
                    'Investissement en matières premières physiques',
                    'Titres adossés à des actifs comme les MBS'
                ]
            })
            return default_mapping
    except Exception as e:
        st.error(f"Erreur lors du chargement du mapping: {e}")
        return pd.DataFrame()

def filter_etf_data(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """
    Applique des filtres sur les données ETF
    
    Args:
        df: DataFrame des ETFs
        filters: Dictionnaire des filtres à appliquer. Clés supportées :
            - 'classe_1', 'classe_2' (list)
            - 'provider' (list)
            - 'pea' (bool)
            - 'frais_max' (float)
            - 'broker' (str) ou 'brokers' (list) : valeurs possibles
              'XTB','ING','SCALABLE','EASYBOURSE','BOURSO','BOURSEDIRECT','ETORO','TOUS'
              La valeur 'TOUS' désactive le filtre broker
        
    Returns:
        DataFrame filtré
    """
    filtered_df = df.copy()
    
    if 'classe_1' in filters and filters['classe_1']:
        filtered_df = filtered_df[filtered_df['CLASSE 1'].isin(filters['classe_1'])]
    if 'classe_2' in filters and filters['classe_2']:
        filtered_df = filtered_df[filtered_df['CLASSE 2'].isin(filters['classe_2'])]

    if 'provider' in filters and filters['provider']:
        filtered_df = filtered_df[filtered_df['PROVIDER'].isin(filters['provider'])]
    
    if 'pea' in filters and filters['pea'] is not None:
        pea_filter = 'Y' if filters['pea'] else 'N'
        if 'PEA' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['PEA'].astype(str).str.upper() == pea_filter]

    if 'assvie' in filters and filters['assvie'] is not None:
        assvie_filter = 'Y' if filters['assvie'] else 'N'
        if 'ASSVIE' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['ASSVIE'].astype(str).str.upper() == assvie_filter]

    if 'frais_max' in filters and filters['frais_max'] is not None:
        col_name = 'FRAIS DE GESTION'
        if col_name in filtered_df.columns:
            filtered_df = filtered_df[
                pd.to_numeric(filtered_df[col_name], errors='coerce').fillna(float('inf')) <= filters['frais_max']
            ]
    
    # Filtre par broker(s)
    broker_cols = ['XTB', 'ING', 'SCALABLE', 'EASYBOURSE', 'BOURSO', 'BOURSEDIRECT', 'ETORO']

    if 'broker' in filters and filters['broker'] in broker_cols:
        selected_broker = filters['broker']
        filtered_df = filtered_df[filtered_df[selected_broker] == True]


    return filtered_df

def calculate_portfolio_metrics(portfolio_data: List[Dict]) -> Dict:
    """
    Calcule les métriques du portefeuille
    
    Args:
        portfolio_data: Liste des positions du portefeuille
        
    Returns:
        Dictionnaire avec les métriques calculées
    """
    if not portfolio_data:
        return {
            'valeur_totale': 0,
            'plus_value_totale': 0,
            'performance_globale': 0,
            'nombre_positions': 0
        }
    
    valeur_totale = sum(pos.get('valeur_actuelle', 0) for pos in portfolio_data)
    cout_total = sum(pos.get('cout_acquisition', 0) for pos in portfolio_data)
    plus_value_totale = valeur_totale - cout_total
    performance_globale = (plus_value_totale / cout_total * 100) if cout_total > 0 else 0
    
    return {
        'valeur_totale': valeur_totale,
        'plus_value_totale': plus_value_totale,
        'performance_globale': performance_globale,
        'nombre_positions': len(portfolio_data)
    }

def format_currency(amount: float) -> str:
    """Formate un montant en euros"""
    return f"{amount:,.2f} €".replace(',', ' ')

def format_percentage(percentage: float) -> str:
    """Formate un pourcentage"""
    return f"{percentage:+.2f}%"

def get_portfolio_allocation(portfolio_data: List[Dict], etf_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule l'allocation du portefeuille par catégorie
    
    Args:
        portfolio_data: Données du portefeuille
        etf_data: Données ETF complètes
        
    Returns:
        DataFrame avec l'allocation par catégorie
    """
    if not portfolio_data:
        return pd.DataFrame()
    
    allocation_data = []
    total_value = sum(pos.get('valeur_actuelle', 0) for pos in portfolio_data)
    
    for position in portfolio_data:
        isin = position.get('isin')
        valeur = position.get('valeur_actuelle', 0)
        
        # Trouver les informations ETF
        
        categorie = position.get('classe_1', 'N/A')
        allocation_data.append({
            'Catégorie': categorie,
            'Valeur': valeur,
            'Pourcentage': (valeur / total_value * 100) if total_value > 0 else 0
        })
    
    if allocation_data:
        df_allocation = pd.DataFrame(allocation_data)
        return df_allocation.groupby('Catégorie').agg({
            'Valeur': 'sum',
            'Pourcentage': 'sum'
        }).reset_index()
    
    return pd.DataFrame()

def search_etf(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """
    Recherche des ETFs par nom ou ISIN
    
    Args:
        df: DataFrame des ETFs
        search_term: Terme de recherche
        
    Returns:
        DataFrame filtré par le terme de recherche
    """
    if not search_term:
        return df
    
    search_term = search_term.lower()
    mask = (
        df['NOM'].str.lower().str.contains(search_term, na=False) |
        df['ISIN'].str.lower().str.contains(search_term, na=False) |
        df['PROVIDER'].str.lower().str.contains(search_term, na=False)
    )
    
    return df[mask]