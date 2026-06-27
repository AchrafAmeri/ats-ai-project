<<<SEARCH
        .then(data => {
            console.log('Données d\'historique reçues :', data);
        })
<<<REPLACE
        .then(data => {
            const tableBody = document.getElementById('dashboard-table-body');
            
            if (!data || data.length === 0) return;

            tableBody.innerHTML = ''; // Vide le message "Aucune analyse"

            data.forEach(item => {
                const score = item.matching_score || 0;
                const candidateName = item.candidate_name || 'Candidat Inconnu';
                const date = new Date(item.created_at).toLocaleDateString('fr-FR', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                });

                // Détermination de la couleur du badge selon le score
                let badgeColor = 'bg-red-100 text-red-800';
                if (score >= 70) {
                    badgeColor = 'bg-green-100 text-green-800';
                } else if (score >= 40) {
                    badgeColor = 'bg-orange-100 text-orange-800';
                }

                // Extraction simplifiée des compétences pour l'affichage
                const skills = item.extracted_data?.skills 
                    ? item.extracted_data.skills.slice(0, 3).join(', ') + (item.extracted_data.skills.length > 3 ? '...' : '')
                    : 'Non spécifié';

                const row = `
                    <tr class="hover:bg-gray-50 transition-colors">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                                    ${candidateName.charAt(0)}
                                </div>
                                <div class="ml-4">
                                    <div class="text-sm font-semibold text-gray-900">${candidateName}</div>
                                    <div class="text-xs text-gray-500">${item.extracted_data?.email || ''}</div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${badgeColor}">
                                ${score}% Match
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            ${date}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span class="truncate block max-w-xs">${skills}</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                            <button class="text-blue-600 hover:text-blue-900">
                                <i class="fa-solid fa-chevron-right"></i>
                            </button>
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', row);
            });
        })
<<<END