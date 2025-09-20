# 📊 Portfolio Manager Pro

Application complète de gestion de portefeuille d'investissement avec analyse ETF avancée, développée avec Streamlit.

## 🎯 Fonctionnalités Principales

### 🏠 Page d'Accueil (`app.py`)
- **Onboarding intelligent** pour nouveaux utilisateurs
- **Dashboard exécutif** pour utilisateurs existants
- **Design moderne** avec CSS avancé et animations
- **Navigation contextuelle** selon l'état du portefeuille

### 📈 Dashboard Portfolio
- **Tableau de suivi complet** avec métriques financières
- **Visualisations interactives** (camemberts, graphiques de performance)
- **Projections d'évolution** basées sur les rendements espérés
- **Import/Export de prix** avec validation intelligente
- **Simulations personnalisées** jusqu'à 50 ans

### 📂 Gestion Portfolio
- **Import multi-format** (CSV, Excel) avec détection automatique
- **Création manuelle** d'actifs avec validation temps réel
- **Templates intelligents** (exemples et vide)
- **Export sécurisé** avec encodage UTF-8 parfait
- **Gestion CRUD** complète des actifs

### 🔍 Recherche ETF
- **Base de données** de 1900+ ETF
- **Filtrage avancé** en 4 colonnes :
  - Type d'investissement (Actions, Obligations, etc.)
  - Région géographique (Europe, États-Unis, Marchés émergents)
  - Critères avancés (spécialisation, courtier)
  - Critères pratiques (PEA, assurance vie, frais)
- **Cards détaillées** avec éligibilités et brokers
- **Univers d'investissement** personnalisé

### 🧮 Analyses Avancées
- **Roadmap interactive** des fonctionnalités futures
- **Démos visuelles** (frontière efficiente, corrélations)
- **Timeline de développement** Q1-Q4 2024
- **Feedback utilisateur** intégré

## 🏗️ Architecture

### Structure Multi-Pages
```
├── app.py                          # Page d'accueil
├── pages/
│   ├── 1_📈_Dashboard.py          # Dashboard portfolio
│   ├── 2_📂_Gestion_Portfolio.py  # Gestion des actifs
│   ├── 3_🔍_Recherche_ETF.py      # Recherche ETF avancée
│   └── 4_🧮_Analyses_Avancées.py  # Fonctionnalités futures
├── utils_categories.py             # Module utilitaire
├── mapping_categories_etf.csv      # Mapping des catégories
└── data/
    └── etf_base_assets.xlsx       # Base de données ETF
```

### Modules Utilitaires
- **`utils_categories.py`** : Fonctions de mapping, calculs, formatage
- **`mapping_categories_etf.csv`** : Correspondances catégories techniques ↔ user-friendly

## 📊 Base de Données ETF

### Statistiques
- **1983 ETF** analysés et classifiés
- **7 Providers** (Blackrock, Amundi, DWS, UBS, etc.)
- **7 Courtiers** (XTB, ING, Scalable, etc.)
- **5 Niveaux** de classification
- **Frais moyens** : 0.26%

### Champs Clés
```
- Identification : ISIN, NOM, PROVIDER
- Classification : CLASSE 1-5 (avec mapping lisible)
- Financier : FRAIS DE GESTION, EXP_MACRO_RETURN, ENCOURS
- Éligibilités : PEA, ASSVIE, HEDGED, SFDR
- Brokers : XTB, ING, SCALABLE, etc. (booléens)
```

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Cloner ou télécharger le projet
cd portfolio-manager-pro

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

### Dépendances Principales
- `streamlit>=1.28.0` - Interface web
- `pandas>=2.0.0` - Manipulation de données
- `plotly>=5.15.0` - Visualisations interactives
- `openpyxl>=3.1.0` - Lecture fichiers Excel

## 💡 Utilisation

### Premier Lancement
1. **Explorez les ETF** via la recherche avancée
2. **Créez votre portefeuille** avec les templates ou import
3. **Suivez vos performances** dans le dashboard
4. **Optimisez votre allocation** avec les projections

### Workflows Typiques

#### Créer un Portefeuille
1. Aller dans **Gestion Portfolio** > **Import**
2. Télécharger un template (exemples ou vide)
3. Remplir avec vos données
4. Importer le fichier

#### Mettre à Jour les Prix
1. Dans le **Dashboard** > **Mettre à jour les prix**
2. Télécharger le template de prix auto-généré
3. Modifier les prix dans le fichier
4. Réimporter le fichier

#### Rechercher des ETF
1. Aller dans **Recherche ETF**
2. Utiliser les filtres (type, région, courtier, critères)
3. Consulter les résultats (max 20, triés par frais)
4. Ajouter à l'univers d'investissement

## 🎨 Design System

### CSS Moderne
- **Variables CSS** pour cohérence
- **Dégradés et animations** fluides
- **Cards interactives** avec hover effects
- **Adaptation thématique** dark/light automatique
- **Design responsive** mobile-friendly

### Composants Réutilisables
- Cards de fonctionnalités
- Métriques avec formatage intelligent
- Tableaux avec tri et filtres
- Graphiques adaptatifs au thème

## 📈 Fonctionnalités Avancées

### Calculs Financiers
- **Métriques automatiques** : valeur, plus-value, performance
- **Projections long terme** basées sur EXP_MACRO_RETURN
- **Rendement pondéré** selon répartition portfolio
- **Simulations d'horizon** personnalisées

### Import/Export Robuste
- **Multi-formats** : CSV (`;` et `,`), Excel (.xlsx, .xls)
- **Encodage UTF-8** avec BOM pour compatibilité Excel
- **Validation intelligente** avec messages d'erreur explicites
- **Templates téléchargeables** pré-formatés

### Session State Management
- **Persistance inter-pages** garantie
- **États complexes** (portfolio, univers ETF, préférences)
- **Gestion d'erreurs** robuste

## 🔮 Roadmap 2024

### Q1 2024 - Optimisation de Portefeuille
- Algorithmes Markowitz
- Frontière efficiente interactive
- Contraintes personnalisables
- Recommandations de rééquilibrage

### Q2 2024 - Corrélation & Backtesting  
- Matrice de corrélation avec heatmap
- Backtesting sur données historiques
- Métriques avancées (Sharpe, Sortino)
- Comparaisons avec benchmarks

### Q3 2024 - Analyse Sectorielle
- Décomposition automatique des ETF
- Détection de concentrations sectorielles
- Comparaisons avec indices de référence
- Alertes de diversification

### Q4 2024 - Monte Carlo
- Simulations probabilistes (10k+ scénarios)
- Planification d'objectifs financiers
- Prise en compte versements périodiques
- Distributions de résultats

## 🛠️ Développement

### Structure du Code
- **Modulaire** : séparation logique métier/présentation
- **Fonctions pures** pour les calculs
- **Cache Streamlit** optimisé pour les performances
- **Documentation inline** complète

### Bonnes Pratiques
- **Validation des données** à tous les niveaux
- **Gestion d'erreurs** explicite avec messages utilisateur
- **Performance** : limitation affichage, cache des données
- **Accessibilité** : contrastes, navigation clavier

### Tests Recommandés
- Tests fonctionnels : tous les workflows utilisateur
- Tests d'intégration : navigation inter-pages  
- Tests de données : import/export divers formats
- Tests UX : ergonomie débutant vs expert

## 📜 Licence

Ce projet est développé pour la gestion de portefeuilles d'investissement personnels et professionnels.

## 🤝 Contribution

Suggestions et améliorations bienvenues ! L'application évolue grâce aux retours utilisateurs.

---

**Portfolio Manager Pro** - Votre compagnon intelligent pour la gestion d'investissements 📊✨