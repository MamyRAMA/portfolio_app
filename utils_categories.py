"""
Module utilitaire pour la gestion des catégories ETF
Fournit des fonctions de mapping et de traitement des classifications ETF
"""

import pandas as pd
import streamlit as st
from typing import Dict, Any
import os

@st.cache_data
def load_category_mapping() -> pd.DataFrame:
    """
    Charge le fichier de mapping des catégories ETF avec cache Streamlit
    
    Returns:
        DataFrame avec les mappings des catégories
    """
    try:
        mapping_path = "mapping_categories_etf.csv"
        if os.path.exists(mapping_path):
            return pd.read_csv(mapping_path, encoding='utf-8')
        else:
            # Créer un mapping par défaut si le fichier n'existe pas
            default_mapping = pd.DataFrame({
                'CLASSE': ['CLASSE 1', 'CLASSE 1', 'CLASSE 1'],
                'CATEGORIE_ORIGINALE': ['equities', 'bonds', 'cash'],
                'CATEGORIE_LISIBLE': ['Actions', 'Obligations', 'Monétaire'],
                'DESCRIPTION': [
                    'Investissement en actions d\'entreprises',
                    'Titres de créance à revenus fixes',
                    'Instruments du marché monétaire'
                ]
            })
            return default_mapping
    except Exception as e:
        st.error(f"Erreur lors du chargement du mapping des catégories: {e}")
        return pd.DataFrame()

def apply_category_mapping(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique le mapping des catégories sur un DataFrame ETF
    
    Args:
        df: DataFrame contenant les données ETF
        
    Returns:
        DataFrame avec les catégories mappées
    """
    if df.empty:
        return df
    
    # Créer une copie pour éviter de modifier l'original
    df_mapped = df.copy()
    
    # Charger le mapping
    mapping_df = load_category_mapping()
    
    if mapping_df.empty:
        return df_mapped
    
    # Appliquer le mapping pour chaque classe
    for classe in ['CLASSE 1', 'CLASSE 2', 'CLASSE 3', 'CLASSE 4', 'CLASSE 5']:
        if classe in df_mapped.columns:
            # Filtrer le mapping pour cette classe
            classe_mapping = mapping_df[mapping_df['CLASSE'] == classe]
            
            if not classe_mapping.empty:
                # Créer un dictionnaire de mapping
                mapping_dict = dict(zip(
                    classe_mapping['CATEGORIE_ORIGINALE'],
                    classe_mapping['CATEGORIE_LISIBLE']
                ))
                
                # Créer une nouvelle colonne avec les valeurs mappées
                col_mapped = f"{classe}_LISIBLE"
                df_mapped[col_mapped] = df_mapped[classe].map(mapping_dict).fillna(df_mapped[classe])
    
    return df_mapped

def get_unique_categories(df: pd.DataFrame, classe: str) -> list:
    """
    Récupère les catégories uniques pour une classe donnée
    
    Args:
        df: DataFrame ETF
        classe: Nom de la classe (ex: 'CLASSE 1')
        
    Returns:
        Liste des catégories uniques
    """
    if classe not in df.columns:
        return []
    
    return sorted(df[classe].dropna().unique().tolist())

def get_mapped_categories(df: pd.DataFrame, classe: str) -> list:
    """
    Récupère les catégories mappées pour une classe donnée
    
    Args:
        df: DataFrame ETF avec mapping appliqué
        classe: Nom de la classe (ex: 'CLASSE 1')
        
    Returns:
        Liste des catégories mappées uniques
    """
    col_mapped = f"{classe}_LISIBLE"
    if col_mapped not in df.columns:
        return get_unique_categories(df, classe)
    
    return sorted(df[col_mapped].dropna().unique().tolist())

def get_drill_down_data(df: pd.DataFrame, selected_category: str, niveau_initial: str = 'CLASSE 1') -> pd.DataFrame:
    """
    Prépare les données pour le drill-down interactif des camemberts
    
    Args:
        df: DataFrame du portefeuille
        selected_category: Catégorie sélectionnée dans le camembert principal
        niveau_initial: Niveau de classification initial
        
    Returns:
        DataFrame filtré pour le drill-down
    """
    if df.empty:
        return df
    
    # Filtrer selon la catégorie sélectionnée
    if niveau_initial in df.columns:
        filtered_df = df[df[niveau_initial] == selected_category].copy()
    else:
        filtered_df = df.copy()
    
    return filtered_df

def format_currency(value: float) -> str:
    """
    Formate une valeur en devise avec séparateurs
    
    Args:
        value: Valeur numérique
        
    Returns:
        Chaîne formatée avec € et séparateurs
    """
    if pd.isna(value):
        return "0 €"
    
    return f"{value:,.2f} €".replace(",", " ").replace(".", ",")

def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formate un pourcentage
    
    Args:
        value: Valeur en pourcentage (0.15 pour 15%)
        decimals: Nombre de décimales
        
    Returns:
        Chaîne formatée avec %
    """
    if pd.isna(value):
        return "0,0%"
    
    formatted = f"{value * 100:.{decimals}f}%".replace(".", ",")
    return formatted

def calculate_portfolio_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcule les métriques principales du portefeuille
    
    Args:
        df: DataFrame du portefeuille
        
    Returns:
        Dictionnaire avec les métriques calculées
    """
    if df.empty:
        return {
            'valeur_totale': 0,
            'plus_value_totale': 0,
            'performance_globale': 0,
            'nombre_actifs': 0,
            'repartition_types': {}
        }
    
    # Colonnes requises pour les calculs
    required_cols = ['Valeur_Actuelle', 'Plus_Value', 'Type']
    for col in required_cols:
        if col not in df.columns:
            if col == 'Valeur_Actuelle':
                df['Valeur_Actuelle'] = df.get('Quantité', 0) * df.get('Prix_Actuel', df.get('Prix_Achat', 0))
            elif col == 'Plus_Value':
                df['Plus_Value'] = df.get('Valeur_Actuelle', 0) - df.get('Valeur_Achat', 0)
            elif col == 'Type':
                df['Type'] = 'ETF'  # Par défaut
    
    # Calculs
    valeur_totale = df['Valeur_Actuelle'].sum()
    plus_value_totale = df['Plus_Value'].sum()
    valeur_achat_totale = valeur_totale - plus_value_totale
    
    performance_globale = 0
    if valeur_achat_totale > 0:
        performance_globale = plus_value_totale / valeur_achat_totale
    
    # Répartition par type
    repartition_types = {}
    if 'Type' in df.columns:
        type_values = df.groupby('Type')['Valeur_Actuelle'].sum()
        repartition_types = (type_values / valeur_totale * 100).to_dict()
    
    return {
        'valeur_totale': valeur_totale,
        'plus_value_totale': plus_value_totale,
        'performance_globale': performance_globale,
        'nombre_actifs': len(df),
        'repartition_types': repartition_types
    }

def get_brokers_info(df_etf: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Récupère les informations sur les courtiers
    
    Args:
        df_etf: DataFrame des ETF avec colonnes brokers
        
    Returns:
        Dictionnaire avec infos par broker
    """
    brokers = ['XTB', 'ING', 'SCALABLE', 'EASYBOURSE', 'BOURSO', 'BOURSEDIRECT', 'ETORO']
    brokers_info = {}
    
    for broker in brokers:
        if broker in df_etf.columns:
            available_count = df_etf[broker].sum() if df_etf[broker].dtype == 'bool' else (df_etf[broker] == True).sum()
            
            brokers_info[broker] = {
                'name': broker,
                'etf_count': available_count,
                'percentage': (available_count / len(df_etf)) * 100 if len(df_etf) > 0 else 0,
                'color': get_broker_color(broker)
            }
    
    return brokers_info

def get_broker_color(broker: str) -> str:
    """
    Retourne la couleur associée à un broker
    
    Args:
        broker: Nom du broker
        
    Returns:
        Code couleur hexadécimal
    """
    colors = {
        'XTB': '#00C851',
        'ING': '#FF6900', 
        'SCALABLE': '#007CBA',
        'EASYBOURSE': '#6610f2',
        'BOURSO': '#28a745',
        'BOURSEDIRECT': '#dc3545',
        'ETORO': '#17a2b8'
    }
    
    return colors.get(broker, '#6c757d')

def calculate_expected_return(df_portfolio: pd.DataFrame, df_etf: pd.DataFrame, years: int = 10) -> Dict[str, float]:
    """
    Calcule le rendement espéré du portefeuille basé sur EXP_MACRO_RETURN
    
    Args:
        df_portfolio: DataFrame du portefeuille
        df_etf: DataFrame des ETF avec EXP_MACRO_RETURN
        years: Horizon de projection en années
        
    Returns:
        Dictionnaire avec projections
    """
    if df_portfolio.empty or df_etf.empty:
        return {'rendement_pondere': 0, 'valeur_future': 0, 'plus_value_future': 0}
    
    # Merge pour récupérer les rendements espérés
    if 'ISIN' in df_portfolio.columns and 'ISIN' in df_etf.columns:
        df_merged = df_portfolio.merge(
            df_etf[['ISIN', 'EXP_MACRO_RETURN']], 
            on='ISIN', 
            how='left'
        )
    else:
        # Fallback: rendement moyen de la base
        avg_return = df_etf['EXP_MACRO_RETURN'].mean() if 'EXP_MACRO_RETURN' in df_etf.columns else 5.0
        df_merged = df_portfolio.copy()
        df_merged['EXP_MACRO_RETURN'] = avg_return
    
    # Calculer le rendement pondéré
    df_merged['EXP_MACRO_RETURN'] = df_merged['EXP_MACRO_RETURN'].fillna(5.0)  # Default 5%
    
    valeur_totale = df_merged['Valeur_Actuelle'].sum()
    if valeur_totale == 0:
        return {'rendement_pondere': 0, 'valeur_future': 0, 'plus_value_future': 0}
    
    # Pondération par valeur
    df_merged['Poids'] = df_merged['Valeur_Actuelle'] / valeur_totale
    rendement_pondere = (df_merged['EXP_MACRO_RETURN'] * df_merged['Poids']).sum()
    
    # Projection future
    rendement_decimal = rendement_pondere / 100
    valeur_future = valeur_totale * ((1 + rendement_decimal) ** years)
    plus_value_future = valeur_future - valeur_totale
    
    return {
        'rendement_pondere': rendement_pondere,
        'valeur_future': valeur_future,
        'plus_value_future': plus_value_future
    }