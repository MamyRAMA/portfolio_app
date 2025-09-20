# PROMPT MAÎTRE - PORTFOLIO MANAGER PRO
## Application complète de gestion de portefeuille avec analyse ETF

**CONTEXTE :** Créer une application Streamlit complète de gestion de portefeuille d'investissement en partant du fichier `etf_base_assets.xlsx` comme source de données unique.

---

## ARCHITECTURE GLOBALE

### Structure multi-pages Streamlit
1. **Page d'accueil** (`app.py`) - Landing page intelligente avec onboarding
2. **Dashboard Portfolio** (`pages/1_📈_Dashboard.py`) - Suivi et analyse du portefeuille
3. **Gestion Portfolio** (`pages/2_📂_Gestion_Portfolio.py`) - Import/Export et CRUD des actifs
4. **Recherche ETF** (`pages/3_🔍_Recherche_ETF.py`) - Moteur de recherche et filtrage avancé
5. **Analyses Avancées** (`pages/4_🧮_Analyses_Avancées.py`) - Page roadmap pour fonctionnalités futures

### Modules utilitaires
- **`utils_categories.py`** - Fonctions de mapping des catégories d'ETF
- **`mapping_categories_etf.csv`** - Table de correspondance catégories techniques ↔ noms user-friendly

---

## SPÉCIFICATIONS DÉTAILLÉES

### 1. PAGE D'ACCUEIL (app.py)

**Design UX/UI avancé :**
- CSS moderne avec dégradés, animations et cards interactives
- Détection automatique de l'état du portefeuille (vide/existant)
- **Onboarding intelligent** pour nouveaux utilisateurs :
  - Guide pas-à-pas avec actions rapides
  - Templates pré-remplis et exemples
  - Navigation contextuelle selon le profil utilisateur
- **Tableau de bord exécutif** pour utilisateurs existants :
  - Métriques clés : valeur totale, performance globale, nombre d'actifs
  - Actions rapides vers toutes les sections
- **Section informative** : statistiques sur la base de données (2055 ETF, 7 courtiers, 5 niveaux de classification)

### 2. DASHBOARD PORTFOLIO (pages/1_📈_Dashboard.py)

**Fonctionnalités principales :**
- **Tableau de suivi complet** avec colonnes : Type, Nom, ISIN, Quantité, Prix d'achat, Prix actuel, Date d'achat, Valeur actuelle, Plus-value, Performance%
- **Ligne de total** avec agrégation des métriques
- **Visualisations interactives :**
  - **Camembert de répartition** adaptatif au thème (dark/light) avec bordures intelligentes
  - **Graphique de performance** par actif avec ligne de performance totale du portefeuille
  - **Camembert interactif avec drill-down** : clic sur "ETF" → décomposition par catégories (CLASSE 1, 2, 3)

**Import/Export de prix :**
- **Mise à jour des prix** : upload fichier multi-format (CSV, Excel, TXT) avec colonnes Nom, ISIN, Nouveau_Prix
- **Validation intelligente** : matching par ISIN ou nom avec gestion des erreurs
- **Export portefeuille** : CSV avec encodage UTF-8 propre (problème caractères € résolu)

**Simulation et projections :**
- **Évolution projetée** basée sur "EXP_MACRO_RETURN" de la base ETF
- **Horizon temporel** : jusqu'à 50 ans
- **Rendement pondéré** selon la répartition du portefeuille

### 3. GESTION PORTFOLIO (pages/2_📂_Gestion_Portfolio.py)

**Organisation en onglets :**

**📥 Import :**
- **Upload multi-format** : CSV, Excel avec détection automatique des délimiteurs
- **Colonnes obligatoires** : Type, Nom, Quantité, Prix_Achat, Date_Achat
- **Colonnes optionnelles** : ISIN, Prix_Actuel
- **Calculs automatiques** : Valeur_Achat, Valeur_Actuelle, Plus_Value, Performance_%
- **Modes d'import** : remplacer/ajouter au portefeuille existant

**📋 Création manuelle :**
- **Formulaire intuitif** avec validation en temps réel
- **Types d'actifs** : ETF, Action, Obligation, Crypto, Autre
- **Calculs automatiques** des métriques financières

**📊 Export :**
- **Export CSV** avec encodage UTF-8 parfait
- **Template de mise à jour des prix** généré automatiquement

**⚙️ Gestion :**
- **Actions sur portefeuille** : vider, modifier, supprimer par actif
- **Liste détaillée** avec expandeurs par actif

**Templates intelligents :**
- **Template avec exemples** : 4 actifs pré-configurés (ETF, Action, Crypto)
- **Template vide** : structure prête à remplir

### 4. RECHERCHE ETF (pages/3_🔍_Recherche_ETF.py)

**Interface de filtrage avancée (4 colonnes) :**

**📊 Type d'investissement :**
- **Catégorie principale** (CLASSE 1) : Actions, Obligations, etc.
- **Sous-catégorie** (CLASSE 2) : filtrage en cascade

**🌍 Région :**
- **Région** (CLASSE 3) : Europe, États-Unis, Marchés émergents
- **Zone géographique** (CLASSE 4) : codes pays détaillés

**🎓 Critères avancés :**
- **Spécialisation** (CLASSE 5) : pour investisseurs expérimentés
- **Courtier préféré** : XTB, ING, SCALABLE, EASYBOURSE, BOURSO, BOURSEDIRECT, ETORO

**⚙️ Critères pratiques :**
- **Éligibilité PEA** : Plan d'Épargne en Actions
- **Assurance vie** : éligibilité contrats
- **Protection change** : ETF hedgés
- **Frais maximum** : slider 0-2%

**Affichage des résultats :**
- **Limitation à 20 ETF** triés par frais croissants
- **Métriques de synthèse** : nombre trouvé, frais moyen, éligibilités PEA/hedgé
- **Cards détaillées par ETF** avec :
  - Informations générales (ISIN, Provider, Mode de distribution C/D)
  - **Éligibilités intelligentes** : PEA, Assurance vie, Protection change
  - **Classification SFDR** : Article 8 (durable), Article 9 (impact), Article 6 masqué
  - Coûts et performance (frais, encours, rendement attendu)
  - Classification complète (5 niveaux)
  - **Broker badges** colorés : vert (disponible) / rouge (indisponible)

**Univers d'investissement :**
- **Sélection d'ETF** pour constitution d'un univers personnalisé
- **Gestion de l'univers** : ajout/suppression, visualisation

### 5. SYSTÈME DE MAPPING DES CATÉGORIES

**Fichier mapping_categories_etf.csv :**
```
CLASSE,CATEGORIE_ORIGINALE,CATEGORIE_LISIBLE,DESCRIPTION
CLASSE 1,Equity,Actions,Investissement en actions d'entreprises
CLASSE 1,Fixed Income,Obligations,Titres de créance à revenus fixes
CLASSE 2,Actions Généraliste,Actions Généralistes,Actions diversifiées tous secteurs
CLASSE 2,Obligations d'Etat,Obligations Souveraines,Dette des États
CLASSE 3,Europe,Europe,Zone européenne
CLASSE 3,United States,États-Unis,Marché américain
[... 35+ mappings intelligents ...]
```

**Fonction utils_categories.py :**
- **load_category_mapping()** : chargement avec cache Streamlit
- **apply_category_mapping()** : application automatique sur DataFrame
- **get_drill_down_data()** : préparation données pour interactivité camembert

### 6. DESIGN SYSTEM ET UX

**CSS moderne avec variables :**
```css
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}
```

**Adaptation thématique automatique :**
- **Détection dark/light mode** pour camemberts
- **Bordures adaptatives** selon le thème système
- **Légendes cohérentes** avec le design global

**Navigation intelligente :**
- **Boutons contextuels** selon l'état de l'application
- **Switch entre pages** avec `st.switch_page()`
- **Breadcrumbs visuels** dans chaque section

### 7. GESTION DES DONNÉES

**Source unique :** `etf_base_assets.xlsx`
**Champs essentiels exploités :**
- **Identification** : ISIN, NOM, PROVIDER
- **Classification** : CLASSE 1-5 (avec mapping)
- **Financier** : FRAIS DE GESTION, FRAIS E/S, EXP_MACRO_RETURN, ENCOURS
- **Caractéristiques** : CAPITALISATION/DISTRIBUTION, PEA, ASSVIE, HEDGED, SFDR
- **Brokers** : XTB, ING, SCALABLE, EASYBOURSE, BOURSO, BOURSEDIRECT, ETORO (booléens)

**Session State Streamlit :**
- **st.session_state.portfolio** : DataFrame du portefeuille utilisateur
- **st.session_state.univers_etf** : ETF sélectionnés pour l'univers
- **Persistance inter-pages** garantie

### 8. FONCTIONNALITÉS AVANCÉES

**Export/Import robuste :**
- **Encodage UTF-8** avec BOM pour compatibilité Excel
- **Multi-formats** : CSV (';' et ','), Excel (.xlsx, .xls)
- **Validation des colonnes** avec messages d'erreur explicites
- **Templates téléchargeables** pré-formatés

**Visualisations interactives :**
- **Plotly avec thème adaptatif**
- **Drill-down sur camembert** : ETF → décomposition par catégories
- **Graphiques de performance** avec ligne de tendance portfolio
- **Formatting intelligent** : 1 décimale pour %, quantités entières, valeurs €

**Simulation financière :**
- **Projections basées sur EXP_MACRO_RETURN**
- **Calcul pondéré** selon répartition portfolio
- **Horizon long terme** (jusqu'à 50 ans)
- **Scénario principal** avec rendements espérés

---

## GUIDE D'IMPLÉMENTATION

### Ordre de développement :
1. **Structure de base** : app.py + configuration pages
2. **Module utils_categories.py** + mapping CSV
3. **Page Recherche ETF** avec filtrage complet
4. **Dashboard Portfolio** avec visualisations
5. **Gestion Portfolio** avec import/export
6. **Analyses Avancées** (page roadmap)
7. **Refinement UX/UI** et CSS avancé

### Points critiques :
- **Session state management** entre pages
- **Gestion erreurs** import/export avec messages clairs
- **Performance** : cache des données ETF, limitation affichage
- **Compatibilité** : caractères spéciaux, encodage UTF-8
- **Responsive design** : colonnes adaptatives, mobile-friendly

### Validation finale :
- **Tests fonctionnels** : tous les workflows utilisateur
- **Tests d'intégration** : navigation inter-pages
- **Tests de données** : import/export divers formats
- **Tests UX** : ergonomie débutant vs expert

**RÉSULTAT ATTENDU :** Application Streamlit production-ready avec architecture modulaire, UX professionnelle, et toutes les fonctionnalités d'un gestionnaire de portefeuille moderne pour investisseurs particuliers et professionnels.