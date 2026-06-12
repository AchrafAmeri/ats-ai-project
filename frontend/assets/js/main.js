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

uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const file = cvFileInput.files[0];
    const description = jobDescriptionInput.value;

    console.log('--- Analyse lancée ---');
    console.log('Fichier CV sélectionné :', file ? file.name : 'Aucun fichier');
    console.log('Objet File :', file);
    console.log('Description du poste :', description);
});