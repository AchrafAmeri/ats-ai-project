const uploadForm = document.getElementById('uploadForm');
const cvFileInput = document.getElementById('cvFile');
const jobDescriptionInput = document.getElementById('jobDescription');
const fileStatus = document.getElementById('fileStatus');
const fileNameDisplay = document.getElementById('fileNameDisplay');

// Éléments de la zone de résultats
const resultsSection = document.getElementById('results');
const scoreText = document.getElementById('score-text');
const strengthsList = document.getElementById('strengths');
const improvementsList = document.getElementById('improvements');

cvFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileNameDisplay.textContent = file.name;
        fileStatus.classList.remove('hidden');
    }
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = cvFileInput.files[0];
    const description = jobDescriptionInput.value;

    if (!file) {
        console.error("Erreur : Aucun fichier sélectionné");
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
            throw new Error(`Erreur HTTP: ${response.status}`);
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
    }
});