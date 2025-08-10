// Fichier : static/dashboard_charts.js
// Gestion des graphes du dashboard

console.log('🎯 DASHBOARD CHARTS - Chargement...');

// Fonction pour attendre que Chart.js soit disponible
function waitForChartJs(callback, maxWait = 10000) {
    const startTime = Date.now();

    function check() {
        if (typeof Chart !== 'undefined') {
            console.log('✅ Chart.js disponible, version:', Chart.version);
            callback();
        } else if (Date.now() - startTime < maxWait) {
            console.log('⏳ En attente de Chart.js...');
            setTimeout(check, 100);
        } else {
            console.error('❌ Chart.js non disponible après délai');
        }
    }

    check();
}

// Fonction pour créer le graphique des objectifs
function createObjectifsChart() {
    console.log('🎨 Création du graphique objectifs...');

    const canvas = document.getElementById('objectifsChart');
    if (!canvas) {
        console.error('❌ Canvas objectifsChart non trouvé');
        return null;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ Contexte 2D impossible pour objectifsChart');
        return null;
    }

    // Récupérer les données depuis les attributs data du canvas
    const objectifsActifs = parseInt(canvas.dataset.objectifsActifs) || 0;
    const objectifsInactifs = parseInt(canvas.dataset.objectifsInactifs) || 0;

    console.log('📊 Données objectifs:', { objectifsActifs, objectifsInactifs });

    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Objectifs Actifs', 'Objectifs Inactifs'],
            datasets: [{
                data: [objectifsActifs, objectifsInactifs],
                backgroundColor: ['#667eea', '#e9ecef'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    console.log('✅ Graphique objectifs créé');
    return chart;
}

// Fonction pour créer le graphique des tâches
function createTachesChart() {
    console.log('🎨 Création du graphique tâches...');

    const canvas = document.getElementById('tachesChart');
    if (!canvas) {
        console.error('❌ Canvas tachesChart non trouvé');
        return null;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ Contexte 2D impossible pour tachesChart');
        return null;
    }

    // Récupérer les données depuis les attributs data du canvas
    const tachesTerminees = parseInt(canvas.dataset.tachesTerminees) || 0;
    const tachesEnCours = parseInt(canvas.dataset.tachesEnCours) || 0;

    console.log('📊 Données tâches:', { tachesTerminees, tachesEnCours });

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Terminées', 'En cours'],
            datasets: [{
                label: 'Tâches',
                data: [tachesTerminees, tachesEnCours],
                backgroundColor: ['#28a745', '#ffc107'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    console.log('✅ Graphique tâches créé');
    return chart;
}

// Fonction principale pour initialiser tous les graphes
function initDashboardCharts() {
    console.log('🚀 Initialisation des graphes du dashboard...');

    // Créer les graphes
    const objectifsChart = createObjectifsChart();
    const tachesChart = createTachesChart();

    // Stocker les références pour pouvoir les détruire plus tard si nécessaire
    window.dashboardCharts = {
        objectifs: objectifsChart,
        taches: tachesChart
    };

    console.log('✅ Tous les graphes du dashboard initialisés');
}

// Fonction pour détruire les graphes existants
function destroyDashboardCharts() {
    if (window.dashboardCharts) {
        if (window.dashboardCharts.objectifs) {
            window.dashboardCharts.objectifs.destroy();
        }
        if (window.dashboardCharts.taches) {
            window.dashboardCharts.taches.destroy();
        }
        window.dashboardCharts = null;
    }
}

// Initialisation automatique quand le DOM est prêt (désactivée pour le dashboard)
// document.addEventListener('DOMContentLoaded', function() {
//     console.log('📋 DOM chargé, initialisation des graphes...');
//     waitForChartJs(initDashboardCharts);
// });

// Fonction pour réinitialiser les graphes (utile pour les mises à jour)
function refreshDashboardCharts() {
    console.log('🔄 Rafraîchissement des graphes...');
    destroyDashboardCharts();
    setTimeout(() => {
        waitForChartJs(initDashboardCharts);
    }, 100);
}

// Exposer les fonctions globalement
window.initDashboardCharts = initDashboardCharts;
window.destroyDashboardCharts = destroyDashboardCharts;
window.refreshDashboardCharts = refreshDashboardCharts;