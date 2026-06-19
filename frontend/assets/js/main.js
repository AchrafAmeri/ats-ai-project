const uploadForm = document.getElementById('uploadForm');
const cvFileInput = document.getElementById('file-upload'); // Mis à jour pour correspondre à l'ID du HTML
const dropZone = document.getElementById('drop-zone');
const jobDescriptionInput = document.getElementById('jobDescription');
const fileStatus = document.getElementById('fileStatus');
const fileNameDisplay = document.getElementById('fileNameDisplay');

// Éléments de la zone de résultats
const resultsSection = document.getElementById('results');
const scoreText = document.getElementById('score-text');
const strengthsList = document.getElementById('strengths');
const improvementsList = document.getElementById('improvements');

// Fonction pour afficher une alerte d'erreur stylisée
const displayError = (message) => {
    // Suppression d'une éventuelle alerte précédente
    const existingAlert = document.getElementById('error-alert');
    if (existingAlert) existingAlert.remove();

    const alertDiv = document.createElement('div');
    alertDiv.id = 'error-alert';
    alertDiv.className = 'bg-red-50 border-l-4 border-red-500 p-4 mb-6 mt-4 rounded-md shadow-sm animate-pulse';
    alertDiv.innerHTML = `
        <div class="flex items-center gap-3">
            <i class="fa-solid fa-circle-exclamation text-red-500 text-xl"></i>
            <div class="flex-1 text-red-700 text-sm font-medium">${message}</div>
            <button onclick="this.parentElement.parentElement.remove()" class="text-red-400 hover:text-red-600 transition-colors">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
    `;
    // Insertion après le formulaire
    uploadForm.insertAdjacentElement('afterend', alertDiv);
    alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
};

// Fonction pour mettre à jour l'interface après sélection d'un fichier
const handleFileUpdate = (file) => {
    if (file) {
        fileNameDisplay.textContent = `${file.name} prêt`;
        fileStatus.classList.remove('hidden');
    }
};

// Gestion du changement via clic (input standard)
cvFileInput.addEventListener('change', (e) => {
    handleFileUpdate(e.target.files[0]);
});

// Gestion du Drag & Drop
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('border-blue-600', 'bg-blue-50');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('border-blue-600', 'bg-blue-50');
    });
});

dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        cvFileInput.files = files; // Place le fichier dans l'input caché
        handleFileUpdate(files[0]);
    }
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = cvFileInput.files[0];
    const description = jobDescriptionInput.value;

    // Reset de l'interface (erreurs et anciens résultats)
    const existingAlert = document.getElementById('error-alert');
    if (existingAlert) existingAlert.remove();
    resultsSection.classList.add('hidden');

    if (!file) {
        displayError("Oups ! N'oubliez pas de sélectionner votre CV avant de lancer l'analyse.");
        return;
    }

    console.log('--- Analyse lancée ---');

    const formData = new FormData();
    formData.append('cv', file);
    formData.append('job_description', description);

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            // Tentative de récupération du message d'erreur JSON de l'API
            let errorMessage = `Erreur serveur (${response.status})`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorMessage;
            } catch (e) { /* Pas de JSON dans la réponse d'erreur */ }
            
            throw new Error(errorMessage);
        }

        const result = await response.json();

        // Mise à jour du score
        scoreText.innerText = result.score;

        // Injection des points forts
        strengthsList.innerHTML = '';
        result.points_forts.forEach(point => {
            const li = document.createElement('li');
            li.className = 'flex items-start gap-2';
            li.innerHTML = `<i class="fa-solid fa-check text-green-500 mt-1"></i> <span>${point}</span>`;
            strengthsList.appendChild(li);
        });

        // Injection des points d'amélioration
        improvementsList.innerHTML = '';
        result.points_amelioration.forEach(point => {
            const li = document.createElement('li');
            li.className = 'flex items-start gap-2';
            li.innerHTML = `<i class="fa-solid fa-arrow-right text-orange-400 mt-1"></i> <span>${point}</span>`;
            improvementsList.appendChild(li);
        });

        // Affichage de la zone de résultat
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        console.log('Résultat de l\'analyse (Gemini) :', result);
    } catch (error) {
        console.error('Erreur lors de la communication avec l\'API :', error);
        
        let userMessage = "Une erreur réseau est survenue. Vérifiez que le serveur backend est bien lancé.";
        if (error.message) userMessage = error.message;
        
        displayError(userMessage);
    }
});