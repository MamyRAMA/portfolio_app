@echo off
echo ====================================
echo   Portfolio Manager Pro
echo   Lancement de l'application...
echo ====================================
echo.

REM Vérifier si Streamlit est installé
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [ERREUR] Streamlit n'est pas installé.
    echo.
    echo Installation des dépendances...
    pip install -r requirements.txt
    echo.
)

echo Lancement de l'application...
echo Accédez à votre navigateur : http://localhost:8501
echo.
echo Pour arrêter l'application : Ctrl+C
echo.

streamlit run app.py

pause