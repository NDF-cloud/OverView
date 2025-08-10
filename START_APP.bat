@echo off
echo ========================================
echo    LANCEMENT DE L'APPLICATION WEB
echo ========================================
echo.
echo Demarrage du serveur web...
echo URL: http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

REM Lancer le serveur web
python-portable\python.exe launch_web.py

pause

