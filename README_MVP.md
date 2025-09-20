# Portfolio Manager Pro - MVP

Application simplifiée de gestion de portefeuille d'investissement ETF développée avec Streamlit.

## 🎯 Vue d'Ensemble

Ce MVP (Minimum Viable Product) offre une solution complète mais simplifiée pour :
- 📊 Visualiser et analyser un portefeuille d'ETFs
- 🔍 Explorer une base de données de 1983 ETFs 
- 📂 Gérer ses positions (ajout, modification, suppression)
- 🧮 Effectuer des analyses de diversification et d'optimisation

## ✨ Fonctionnalités

### 🏠 Page d'Accueil
- Navigation simplifiée via la sidebar
- Aperçu des données disponibles
- Statistiques rapides du portfolio
- Guide de démarrage intégré

### 📈 Dashboard Portfolio  
- Métriques essentielles (valeur, performance, positions)
- Répartition par classe d'actifs (graphiques Plotly)
- Détail des positions avec plus-values
- Évolution simulée du portfolio
- Actions rapides vers les autres pages

### 📂 Gestion Portfolio
- **Recherche et ajout** : Recherche d'ETFs avec filtres, sélection interactive
- **Mes positions** : Vue d'ensemble avec résumé financier, suppression possible
- **Import/Export** : Sauvegarde en CSV, import de portfolios existants

### 🔍 Recherche ETF
- Base de données complète de 1983 ETFs
- Filtres avancés : classe d'actifs, fournisseur, éligibilité PEA, frais
- Recherche textuelle (nom, ISIN, fournisseur)  
- Analyses statistiques du marché ETF
- Sélection multiple pour ajout au portfolio

### 🧮 Analyses Avancées
- **Allocation** : Répartition par classe d'actifs et fournisseur
- **Diversification** : Score automatique avec recommandations
- **Coûts** : Frais pondérés, coût annuel et projection 10 ans
- **Optimisation** : Suggestions d'amélioration personnalisées

## 🗂️ Structure Simplifiée

```
portfolio_app/
├── app.py                    # Page d'accueil et navigation
├── utils_data.py            # Utilitaires de données simplifiés
├── requirements.txt         # Dépendances minimales
├── data/
│   └── etf_base_assets.xlsx # Base ETF (1983 ETFs)
├── mapping_categories_etf.csv # Mapping des catégories
└── pages/
    ├── 1_Dashboard.py       # Dashboard simplifié
    ├── 2_Gestion_Portfolio.py # Gestion positions
    ├── 3_Recherche_ETF.py     # Moteur recherche
    └── 4_Analyses_Avancees.py # Analyses et optimisation
```

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Installer les dépendances
pip install -r requirements.txt
```

### Lancement
```bash
# Lancer l'application MVP
streamlit run app.py
```

L'application sera accessible à : **http://localhost:8501**

## 📊 Données Disponibles

### Base ETF (1983 ETFs)
- ISIN, Nom, Fournisseur
- Frais de gestion, Encours sous gestion  
- Classifications (CLASSE 1, 2, 3)
- Éligibilité PEA, devise
- Liens vers documentation

### Mapping des Catégories
- Classification hiérarchique en 3 niveaux
- Descriptions lisibles des catégories
- 18 catégories mappées (Actions, Obligations, etc.)

## 🛠️ Technologies

- **Streamlit** : Interface utilisateur (sans CSS complexe)
- **Plotly** : Graphiques interactifs uniquement
- **Pandas** : Manipulation des données
- **NumPy** : Calculs statistiques simples

## 📱 Guide d'Utilisation

### Premier Usage
1. **Explorez** la base ETF via "Recherche ETF"
2. **Ajoutez** des positions via "Gestion Portfolio" 
3. **Visualisez** votre dashboard
4. **Analysez** avec les outils avancés

### Workflow Recommandé
1. 🔍 **Recherche** → Filtrer et sélectionner des ETFs
2. ➕ **Ajout** → Créer des positions avec prix
3. 📊 **Suivi** → Consulter dashboard et métriques
4. 🧮 **Optimisation** → Utiliser les analyses pour améliorer

## 💡 Fonctionnalités Clés du MVP

### Simplicité
- Interface épurée sans CSS complexe
- Navigation intuitive via sidebar
- Actions claires et directes

### Efficacité  
- Chargement rapide des données (cache Streamlit)
- Filtres performants sur 1983 ETFs
- Calculs automatiques des métriques

### Fonctionnalité
- Toutes les fonctions essentielles présentes
- Export/Import CSV intégré
- Analyses pertinentes pour investisseurs particuliers

## 🔧 Personnalisation

### Modification Facile
- Code simple et commenté
- Structure modulaire (utils_data.py)
- Ajout de nouveaux filtres ou métriques aisé

### Extension Possible
- Ajout de nouvelles pages Streamlit
- Intégration d'APIs externes
- Nouvelles analyses dans utils_data.py

## 📈 Analyses Disponibles

### Métriques Portfolio
- Valeur totale, plus-values, performance globale
- Nombre de positions, position moyenne

### Diversification
- Score de diversification automatique  
- Répartition par classe d'actifs
- Concentration par fournisseur

### Optimisation
- Analyse des frais (pondérés, coût annuel)
- Suggestions personnalisées
- Comparaison avec allocations cibles

## 🚫 Limitations du MVP

- Pas de données temps réel (simulation pour l'évolution)
- Analyses basiques (pas de corrélations complexes)
- Interface uniquement Streamlit (pas de CSS avancé)
- Pas de persistence entre sessions (données en session_state)

## 🔮 Évolutions Possibles

### Court Terme
- Persistence des données (base SQLite)
- Plus de types de graphiques
- Filtres ETF supplémentaires

### Long Terme  
- Intégration APIs financières
- Analyses de corrélation avancées
- Interface mobile
- Multi-utilisateurs

## 📄 Licence

MIT License - Voir fichier LICENSE

## 🆘 Support

- Code documenté et commenté
- Structure simple à comprendre
- Fonctions utilitaires réutilisables

---

**MVP développé pour les investisseurs particuliers** 🚀  
*Simple, efficace, facilement modifiable*