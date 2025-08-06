document.addEventListener('DOMContentLoaded', () => {
    // Charger les projets
    const projetList = document.getElementById('projet-list');
    if (projetList) {
        fetch('/api/projets/')
            .then(response => response.json())
            .then(data => {
                projetList.innerHTML = '';
                data.projets.forEach(projet => {
                    const projetCard = `
                        <div class="bg-white p-4 rounded shadow">
                            ${projet.image ? `<img src="${projet.image}" alt="${projet.titre}" class="w-full h-48 object-cover rounded mb-4">` : ''}
                            <h3 class="text-xl font-semibold">${projet.titre}</h3>
                            <p class="text-gray-600">${projet.description.substring(0, 100)}...</p>
                            <p class="text-sm text-gray-500">${projet.categorie ? `Catégorie: ${projet.categorie}` : ''}</p>
                            <a href="/${document.documentElement.lang}/projet/${projet.id}/" class="mt-2 inline-block text-blue-600 hover:underline">{% trans "Voir les détails" %}</a>
                        </div>
                    `;
                    projetList.innerHTML += projetCard;
                });
            })
            .catch(error => console.error('Erreur:', error));
    }

    // Charger les articles
    const articleList = document.getElementById('article-list');
    if (articleList) {
        fetch('/api/articles/')
            .then(response => response.json())
            .then(data => {
                articleList.innerHTML = '';
                data.articles.forEach(article => {
                    const articleCard = `
                        <div class="bg-white p-4 rounded shadow">
                            ${article.image ? `<img src="${article.image}" alt="${article.titre}" class="w-full h-48 object-cover rounded mb-4">` : ''}
                            <h3 class="text-xl font-semibold">${article.titre}</h3>
                            <p class="text-gray-600">${article.contenu}</p>
                            <p class="text-sm text-gray-500">${article.categorie ? `Catégorie: ${article.categorie}` : ''}</p>
                            <a href="/${document.documentElement.lang}/article/${article.id}/" class="mt-2 inline-block text-blue-600 hover:underline">{% trans "Lire l'article" %}</a>
                        </div>
                    `;
                    articleList.innerHTML += articleCard;
                });
            })
            .catch(error => console.error('Erreur:', error));
    }
});
// monportfolio/static/js/main.js
const loginForm = document.querySelector('form');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        const username = loginForm.querySelector('input[name="username"]').value;
        const password = loginForm.querySelector('input[name="password"]').value;
        if (!username || !password) {
            e.preventDefault();
            alert('{% trans "Veuillez remplir tous les champs." %}');
        }
    });
}