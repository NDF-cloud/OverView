let isMobile = window.innerWidth <= 768;
let scrollTimeout;
let isScrolling = false;
let currentTab = null; // Pas d'onglet par défaut pour éviter le flash

// Titres dynamiques pour chaque onglet
const tabTitles = {
    'epargne': {
        title: 'Épargne',
        subtitle: 'Gérez vos objectifs d\'épargne'
    },
    'taches': {
        title: 'Tâches',
        subtitle: 'Organisez vos tâches et étapes'
    },
    'agenda': {
        title: 'Agenda',
        subtitle: 'Planifiez vos événements'
    },

    'notifications': {
        title: 'Notifications',
        subtitle: 'Centre de notifications'
    },
    'rapports': {
        title: 'Rapports',
        subtitle: 'Exportez vos données'
    },

};

// Fonction pour détecter si on est sur mobile
function checkMobile() {
    isMobile = window.innerWidth <= 768;
}

// Fonction pour détecter l'onglet au centre
function detectCenterTab() {
    if (!isMobile) return;

    const navTabs = document.querySelector('.nav-tabs');
    const tabs = document.querySelectorAll('.nav-tab');
    const containerCenter = navTabs.offsetLeft + navTabs.offsetWidth / 2;

    let centerTab = null;
    let minDistance = Infinity;

    tabs.forEach(tab => {
        const tabCenter = tab.offsetLeft + tab.offsetWidth / 2;
        const distance = Math.abs(tabCenter - containerCenter);

        if (distance < minDistance) {
            minDistance = distance;
            centerTab = tab;
        }
    });

    return centerTab;
}

// Fonction pour naviguer vers l'onglet au centre
function navigateToCenterTab() {
    if (!isMobile) return;

    const centerTab = detectCenterTab();
    if (centerTab && !centerTab.classList.contains('active')) {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            switchTab(centerTab.dataset.tab);
        }, 500);
    }
}

// Écouter le défilement des onglets
function setupTabScrollDetection() {
    if (!isMobile) return;

    const navTabs = document.querySelector('.nav-tabs');

    navTabs.addEventListener('scroll', () => {
        isScrolling = true;
        clearTimeout(scrollTimeout);

        scrollTimeout = setTimeout(() => {
            isScrolling = false;
            navigateToCenterTab();
        }, 150);
    });
}

// Fonction pour mettre à jour les titres dynamiques
function updateDynamicTitles(tabName) {
    const titleElement = document.getElementById('dynamicTitle');
    const subtitleElement = document.getElementById('dynamicSubtitle');

    if (tabTitles[tabName]) {
        titleElement.textContent = tabTitles[tabName].title;
        subtitleElement.textContent = tabTitles[tabName].subtitle;
    }
}

// Fonction pour charger le contenu du Dashboard
function loadDashboardContent() {
    const dashboardMainContent = document.getElementById('dashboardMainContent');
    const tabContent = document.getElementById('tabContent');
    const navTabsContainer = document.getElementById('navTabsContainer');

    // Afficher le contenu principal du Dashboard
    dashboardMainContent.style.display = 'block';
    tabContent.style.display = 'none';

    // Afficher les onglets (ils sont toujours visibles dans le Dashboard)
    navTabsContainer.style.display = 'block';

    // Retirer la classe active de tous les onglets quand on retourne au Dashboard
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Mettre à jour les titres
    document.getElementById('dynamicTitle').textContent = 'Dashboard';
    document.getElementById('dynamicSubtitle').textContent = 'Vue d\'ensemble de vos finances';

    // Charger le contenu principal du Dashboard
    fetch('/api/tab-content/dashboard')
        .then(response => response.text())
        .then(html => {
            dashboardMainContent.innerHTML = html;

            // Forcer l'initialisation des graphes après le chargement du contenu
            console.log('🎯 Dashboard chargé, initialisation des graphes...');

            // Attendre un peu que le DOM soit mis à jour
            setTimeout(() => {
                if (typeof initDashboardCharts === 'function') {
                    console.log('✅ Fonction initDashboardCharts trouvée, initialisation...');
                    initDashboardCharts();
                } else {
                    console.log('⏳ Fonction initDashboardCharts non disponible, attente...');
                    // Attendre que Chart.js soit disponible
                    if (typeof waitForChartJs === 'function') {
                        waitForChartJs(() => {
                            if (typeof initDashboardCharts === 'function') {
                                initDashboardCharts();
                            }
                        });
                    }
                }
            }, 100);
        })
        .catch(error => {
            console.error('Erreur lors du chargement du Dashboard:', error);
            dashboardMainContent.innerHTML = '<div style="text-align: center; padding: 50px;"><h3>Erreur de chargement du Dashboard</h3></div>';
        });
}

// Fonction pour afficher le contenu d'un onglet
function showTabContent(tabName) {
    if (!tabName || !tabTitles[tabName]) {
        console.warn('Onglet invalide:', tabName);
        return;
    }

    const dashboardMainContent = document.getElementById('dashboardMainContent');
    const tabContent = document.getElementById('tabContent');

    // Masquer le contenu principal du Dashboard et afficher le contenu de l'onglet
    dashboardMainContent.style.display = 'none';
    tabContent.style.display = 'block';

    // Retirer la classe active de tous les onglets
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Activer l'onglet sélectionné
    const activeTab = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }

    // Mettre à jour les titres dynamiques
    updateDynamicTitles(tabName);

    currentTab = tabName;

    // Sauvegarder l'onglet actuel dans localStorage
    localStorage.setItem('currentTab', tabName);

    // Charger le contenu dynamiquement
    loadTabContent(tabName);
}

// Fonction pour changer d'onglet (maintenue pour compatibilité)
function switchTab(tabName) {
    showTabContent(tabName);
}

// Fonction pour charger le contenu d'un onglet
function loadTabContent(tabName) {
    const contentContainer = document.getElementById('tabContent');

    // Afficher un indicateur de chargement sans flash
    const loadingHtml = `
        <div style="text-align: center; padding: 50px;">
            <div style="display: inline-block; width: 50px; height: 50px; border: 3px solid #f3f3f3; border-top: 3px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            <p style="margin-top: 20px; color: #666;">Chargement...</p>
        </div>
    `;
    contentContainer.innerHTML = loadingHtml;

    // Styles pour l'animation de chargement
    const style = document.createElement('style');
    style.textContent = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
    document.head.appendChild(style);

    // Faire une requête AJAX pour charger le contenu
    fetch(`/api/tab-content/${tabName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur de chargement');
            }
            return response.text();
        })
        .then(html => {
            contentContainer.innerHTML = html;

            // Réinitialiser les scripts dans le contenu chargé
            const scripts = contentContainer.querySelectorAll('script');
            scripts.forEach(script => {
                const newScript = document.createElement('script');
                if (script.src) {
                    newScript.src = script.src;
                } else {
                    newScript.textContent = script.textContent;
                }
                script.parentNode.replaceChild(newScript, script);
            });

            // Initialiser les analytics si c'est l'onglet analytics
            if (tabName === 'analytics' && typeof initAdvancedAnalytics === 'function') {
                setTimeout(() => {
                    initAdvancedAnalytics();
                }, 500);
            }


        })
        .catch(error => {
            console.error('Erreur lors du chargement:', error);
            contentContainer.innerHTML = `
                <div style="text-align: center; padding: 50px;">
                    <h3 style="color: #e74c3c;">Erreur de chargement</h3>
                    <p style="color: #666;">Impossible de charger le contenu de l'onglet ${tabName}</p>
                    <button onclick="switchTab('${tabName}')" style="margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">Réessayer</button>
                </div>
            `;
        });
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Charger le thème en premier
    loadTheme();
    initThemeToggles();

    // Détecter la taille de l'écran
    checkMobile();

    // Écouter les changements de taille d'écran
    window.addEventListener('resize', checkMobile);

    // Configurer la détection de défilement des onglets
    setupTabScrollDetection();

    // Ajouter les événements de clic aux onglets
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const tabName = this.dataset.tab;
            switchTab(tabName);
        });
    });

    // Ajouter l'événement pour les boutons Home (délégué d'événement)
    document.addEventListener('click', function(e) {
        if (e.target && e.target.id === 'homeButton') {
            e.preventDefault();
            loadDashboardContent();
            // Nettoyer l'URL
            window.history.pushState({}, '', window.location.pathname);
        }
    });

    // Déterminer ce qui doit être chargé AVANT d'afficher quoi que ce soit
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');

            // Faire apparaître le contenu progressivement
    const dashboardContent = document.getElementById('dashboardContent');
    const navTabsContainer = document.getElementById('navTabsContainer');
    const container = document.querySelector('.container');
    const fixedHeader = document.querySelector('.fixed-header');

    if (tabParam && tabTitles[tabParam]) {
        // Charger directement l'onglet spécifié
        showTabContent(tabParam);
        dashboardContent.classList.add('ready');
        navTabsContainer.classList.add('ready');
        container.classList.add('ready');
        fixedHeader.classList.add('ready');
    } else if (window.location.hash) {
        const tabName = window.location.hash.substring(1);
        if (tabTitles[tabName]) {
            showTabContent(tabName);
            dashboardContent.classList.add('ready');
            navTabsContainer.classList.add('ready');
            container.classList.add('ready');
            fixedHeader.classList.add('ready');
        } else {
            // Charger le Dashboard par défaut
            loadDashboardContent();
            dashboardContent.classList.add('ready');
            navTabsContainer.classList.add('ready');
            container.classList.add('ready');
            fixedHeader.classList.add('ready');
        }
    } else {
        // Charger le Dashboard par défaut (page d'accueil)
        loadDashboardContent();
        dashboardContent.classList.add('ready');
        navTabsContainer.classList.add('ready');
        container.classList.add('ready');
        fixedHeader.classList.add('ready');
    }
});

// Fonction pour basculer le mode sombre
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    let theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);

    // Mettre à jour tous les boutons theme-toggle
    const themeToggles = document.querySelectorAll('#theme-toggle');
    themeToggles.forEach(toggle => {
        toggle.textContent = theme === 'dark' ? 'Désactiver le Mode Nuit' : 'Activer le Mode Nuit';
    });
}

// Fonction pour charger le thème depuis le localStorage
function loadTheme() {
    const theme = localStorage.getItem('theme');
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
}

// Fonction pour initialiser les boutons theme-toggle
function initThemeToggles() {
    const themeToggles = document.querySelectorAll('#theme-toggle');
    themeToggles.forEach(toggle => {
        const theme = localStorage.getItem('theme');
        toggle.textContent = theme === 'dark' ? 'Désactiver le Mode Nuit' : 'Activer le Mode Nuit';

        toggle.addEventListener('click', toggleDarkMode);
    });
}