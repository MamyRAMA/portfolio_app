#!/bin/bash
# Script de setup GitHub pour Portfolio Manager Pro

echo "🚀 Configuration GitHub pour Portfolio Manager Pro"
echo "=================================================="

# Vérifier si git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Initialiser le repository git
echo "📦 Initialisation du repository Git..."
git init

# Ajouter tous les fichiers
echo "📁 Ajout des fichiers..."
git add .

# Premier commit
echo "💾 Premier commit..."
git commit -m "🎉 Initial commit: Portfolio Manager Pro v1.0

✨ Fonctionnalités:
- Dashboard avancé avec projections financières
- Recherche ETF intelligente (1983+ ETF)
- Gestion de portefeuille complète
- Design adaptatif (mode sombre/clair)
- Interface multi-pages avec Streamlit

🛠 Technologies:
- Streamlit 1.49+
- Pandas 2.0+
- Plotly 5.15+
- CSS moderne avec variables adaptatives

📈 Calculs financiers validés:
- Intérêts composés avec contributions mensuelles
- Rendements pondérés par allocation
- Projections jusqu'à 40 ans"

echo ""
echo "✅ Repository Git initialisé avec succès!"
echo ""
echo "📋 ÉTAPES SUIVANTES:"
echo "==================="
echo ""
echo "1️⃣  Créer le repository sur GitHub:"
echo "   - Allez sur https://github.com/new"
echo "   - Nom du repository: portfolioapp"
echo "   - Description: Portfolio Manager Pro - Application complète de gestion de portefeuille"
echo "   - Définir comme Public ou Private selon vos préférences"
echo "   - ❗ NE PAS cocher 'Add a README file' (on en a déjà un)"
echo "   - ❗ NE PAS cocher 'Add .gitignore' (on en a déjà un)"
echo "   - Cliquer 'Create repository'"
echo ""
echo "2️⃣  Connecter le repository local:"
echo "   Remplacez [VOTRE-USERNAME] par votre nom d'utilisateur GitHub"
echo ""
echo "   git remote add origin https://github.com/[VOTRE-USERNAME]/portfolioapp.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3️⃣  Commandes Git utiles pour la suite:"
echo "   git status                    # Voir l'état des fichiers"
echo "   git add .                     # Ajouter tous les changements"
echo "   git commit -m 'message'       # Committer les changements"
echo "   git push                      # Envoyer vers GitHub"
echo "   git pull                      # Récupérer depuis GitHub"
echo ""
echo "🎯 EXEMPLE COMPLET:"
echo "==================="
echo "git remote add origin https://github.com/MonUsername/portfolioapp.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "🌟 Une fois sur GitHub, n'oubliez pas de:"
echo "   - Ajouter une description au repository"
echo "   - Configurer les topics (streamlit, portfolio, etf, finance)"
echo "   - Activer GitHub Pages si besoin"
echo ""
echo "💡 Le repository contiendra:"
echo "   ✅ Code source complet"
echo "   ✅ Documentation README détaillée"  
echo "   ✅ Fichier .gitignore configuré"
echo "   ✅ Requirements.txt"
echo "   ✅ Base de données ETF"
echo ""
echo "🚀 Votre Portfolio Manager Pro sera disponible sur GitHub!"