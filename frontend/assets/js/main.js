const uploadForm = document.getElementById('uploadForm');
const cvFileInput = document.getElementById('cvFile');
const jobDescriptionInput = document.getElementById('jobDescription');
const fileStatus = document.getElementById('fileStatus');
const fileNameDisplay = document.getElementById('fileNameDisplay');

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
        console.log('Résultat de l\'analyse (Gemini) :', result);
    } catch (error) {
        console.error('Erreur lors de la communication avec l\'API :', error);
    }
});