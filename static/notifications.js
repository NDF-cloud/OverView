function confirmerSuppressionNotification(notificationId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette notification ?')) {
        fetch(`/supprimer_notification/${notificationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Recharger le contenu de l'onglet
                if (typeof loadTabContent === 'function') {
                    loadTabContent('notifications');
                } else {
                    // Recharger la page si la fonction n'est pas disponible
                    window.location.reload();
                }
            } else {
                alert('Erreur lors de la suppression de la notification');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la suppression de la notification');
        });
    }
} 