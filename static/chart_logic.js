// Fichier : static/chart_logic.js
document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('evolutionChart');
    if (!chartCanvas) return;
    const objectifId = chartCanvas.dataset.objectifId;
    if (!objectifId) return;
    fetch(`/api/chart_data/${objectifId}`)
        .then(response => {
            if (!response.ok) { throw new Error('Erreur réseau ou autorisation'); }
            return response.json();
        })
        .then(chartData => {
            const ctx = chartCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [
                        {
                            label: 'Entrées cumulées (FCFA)',
                            data: chartData.data_entrees,
                            fill: true,
                            borderColor: '#667eea',
                            backgroundColor: 'rgba(102, 126, 234, 0.2)',
                            tension: 0.4
                        },
                        {
                            label: 'Sorties cumulées (FCFA)',
                            data: chartData.data_sorties,
                            fill: false,
                            borderColor: '#e74c3c',
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: { y: { beginAtZero: true } },
                    plugins: {
                        legend: {
                            position: 'top'
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Erreur lors de la récupération des données du graphique:", error));
});