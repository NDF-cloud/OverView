let isMobile = window.innerWidth <= 768;
let scrollTimeout;
let isScrolling = false;
let currentTab = 'epargne'; // Onglet par défaut

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

// Fonction pour changer d'onglet
function switchTab(tabName) {
    // Retirer la classe active de tous les onglets
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Masquer tout le contenu
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // Activer l'onglet sélectionné
    const activeTab = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }

    // Afficher le contenu correspondant
    const activeContent = document.getElementById(`${tabName}Content`);
    if (activeContent) {
        activeContent.classList.add('active');
    }

    currentTab = tabName;
    
    // Charger le contenu dynamiquement si nécessaire
    loadTabContent(tabName);
}

// Fonction pour charger le contenu d'un onglet
function loadTabContent(tabName) {
    const contentContainer = document.getElementById(`${tabName}Content`);
    
    // Si le contenu n'est pas encore chargé, le charger
    if (contentContainer && !contentContainer.hasAttribute('data-loaded')) {
        fetch(`/api/tab-content/${tabName}`)
            .then(response => response.text())
            .then(html => {
                contentContainer.innerHTML = html;
                contentContainer.setAttribute('data-loaded', 'true');
            })
            .catch(error => {
                console.error('Erreur lors du chargement du contenu:', error);
            });
    }
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

    const defaultContent = document.getElementById('epargneContent');
    if (defaultContent) {
        defaultContent.classList.add('active');
    }
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