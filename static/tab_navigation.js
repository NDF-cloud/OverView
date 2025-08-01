let isMobile = window.innerWidth <= 768;
let scrollTimeout;
let isScrolling = false;
let currentTab = 'epargne'; // Onglet par défaut

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
    'dashboard': {
        title: 'Dashboard',
        subtitle: 'Vue d\'ensemble de vos finances'
    },
    'notifications': {
        title: 'Notifications',
        subtitle: 'Centre de notifications'
    },
    'rapports': {
        title: 'Rapports',
        subtitle: 'Exportez vos données'
    }
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

// Fonction pour changer d'onglet
function switchTab(tabName) {
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
    
    // Charger le contenu dynamiquement
    loadTabContent(tabName);
}

// Fonction pour charger le contenu d'un onglet
function loadTabContent(tabName) {
    const contentContainer = document.getElementById('tabContent');
    
    // Charger le contenu complet de la page
    fetch(`/api/tab-content/${tabName}`)
        .then(response => response.text())
        .then(html => {
            // Créer un DOM temporaire pour parser le HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Extraire le contenu principal (sans les en-têtes et barres d'onglets)
            const mainContent = doc.querySelector('.container') || doc.querySelector('main') || doc.querySelector('.content');
            
            if (mainContent) {
                // Supprimer les éléments de navigation et en-têtes
                const elementsToRemove = mainContent.querySelectorAll('.nav-tabs-container, .header, .nav-tabs, .tab-navigation');
                elementsToRemove.forEach(el => el.remove());
                
                // Injecter le contenu principal
                contentContainer.innerHTML = mainContent.innerHTML;
            } else {
                // Fallback : utiliser tout le contenu du body
                const bodyContent = doc.querySelector('body');
                if (bodyContent) {
                    // Supprimer les scripts et styles
                    const scriptsAndStyles = bodyContent.querySelectorAll('script, style, link');
                    scriptsAndStyles.forEach(el => el.remove());
                    
                    contentContainer.innerHTML = bodyContent.innerHTML;
                } else {
                    contentContainer.innerHTML = html;
                }
            }
        })
        .catch(error => {
            console.error('Erreur lors du chargement du contenu:', error);
            contentContainer.innerHTML = '<div style="text-align: center; padding: 50px;"><h2>Erreur de chargement</h2><p>Impossible de charger le contenu de cet onglet.</p></div>';
        });
}

// Initialiser les onglets
function initTabs() {
    // Ajouter les événements de clic
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const tabName = tab.dataset.tab;
            switchTab(tabName);
        });
    });

    // Activer l'onglet par défaut
    const defaultTab = document.querySelector('[data-tab="epargne"]');
    if (defaultTab) {
        defaultTab.classList.add('active');
    }

    // Charger le contenu par défaut
    loadTabContent('epargne');
}

// Initialiser au chargement
window.addEventListener('load', () => {
    checkMobile();
    setupTabScrollDetection();
    initTabs();
});

// Réinitialiser lors du redimensionnement
window.addEventListener('resize', () => {
    checkMobile();
    setupTabScrollDetection();
});

// Activer le mode sombre si configuré
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
} 