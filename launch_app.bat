@echo off
echo Lancement de l'application Flask...
echo.

REM Essayer d'utiliser Python portable
if exist "python-portable\python.exe" (
    echo Utilisation de Python portable...
    python-portable\python.exe -m pip install flask
    if %errorlevel% equ 0 (
        echo Flask installe avec succes!
        python-portable\python.exe app.py
        goto :end
    )
)

REM Essayer d'utiliser l'environnement virtuel
if exist "venv_new\Scripts\python.exe" (
    echo Utilisation de l'environnement virtuel...
    venv_new\Scripts\python.exe -m pip install flask
    if %errorlevel% equ 0 (
        echo Flask installe avec succes!
        venv_new\Scripts\python.exe app.py
        goto :end
    )
)

REM Essayer d'utiliser Python systeme
echo Tentative avec Python systeme...
python -m pip install flask
if %errorlevel% equ 0 (
    echo Flask installe avec succes!
    python app.py
    goto :end
)

REM Essayer avec py launcher
echo Tentative avec py launcher...
py -m pip install flask
if %errorlevel% equ 0 (
    echo Flask installe avec succes!
    py app.py
    goto :end
)

echo Erreur: Impossible d'installer Flask ou de lancer l'application
echo Veuillez installer Python et Flask manuellement

:end
pause

