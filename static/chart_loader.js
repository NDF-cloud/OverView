// Test de chargement de Chart.js
console.log('=== CHARGEMENT CHART.JS ===');
console.log('Chart.js chargé:', typeof Chart !== 'undefined');
if (typeof Chart !== 'undefined') {
    console.log('Version Chart.js:', Chart.version);
}

// Fonction pour vérifier si Chart.js est disponible
function isChartJsLoaded() {
    return typeof Chart !== 'undefined';
}

// Fonction pour attendre que Chart.js soit chargé
function waitForChartJs(callback, maxWait = 5000) {
    const startTime = Date.now();

    function check() {
        if (isChartJsLoaded()) {
            console.log('✅ Chart.js est maintenant disponible');
            callback();
        } else if (Date.now() - startTime < maxWait) {
            console.log('⏳ En attente de Chart.js...');
            setTimeout(check, 100);
        } else {
            console.error('❌ Chart.js n\'a pas pu être chargé dans le délai imparti');
        }
    }

    check();
}