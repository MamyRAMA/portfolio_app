#!/bin/bash
echo "===================================="
echo "  Portfolio Manager Pro"  
echo "  Lancement de l'application..."
echo "===================================="
echo

# Vérifier si Streamlit est installé
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERREUR] Streamlit n'est pas installé."
    echo
    echo "Installation des dépendances..."
    pip3 install -r requirements.txt
    echo
fi

echo "Lancement de l'application..."
echo "Accédez à votre navigateur : http://localhost:8501"
echo
echo "Pour arrêter l'application : Ctrl+C"
echo

streamlit run app.py