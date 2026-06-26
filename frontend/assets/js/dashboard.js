document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:8000/api/v1/history';

    fetch(API_URL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des données');
            }
            return response.json();
        })
        .then(data => {
            console.log('Données d\'historique reçues :', data);
        })
        .catch(error => {
            console.error('Erreur fetch:', error);
        });
});