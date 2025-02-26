# artemis

✅ step 1 :
fetch toutes les musiques à plus d'1 milliard de stream sur spotify

✅ step 2 :
rendre le fetch dynamique

✅ step 3 :
sauvegarder dans un json

step 4 :
gestion des erreurs

step 5 :
ajout de tests

step 6 :
fetch les informations d'un son en précis (streams and image en plus grosse résolution)

step 7 :
création d'un nouveau json dans un nouveau folder juste pour le billion club data

step 8 :
Envoi des données sur Hermès qui lui filtrera les données et les ajoutera à Athéna

<!-- notes -->

Les données des playlists Spotify ne sont pas chargées directement en HTML. Elles sont injectées dynamiquement via JavaScript.

Avec BeautifulSoup uniquement → Tu obtiens une page vide ou incomplète, car BS4 ne peut voir que le HTML statique. -> bs4 n'est pas vraiment compatible avec la méthode utilisée ici, autant utiliser selenium pour scrapper

Avec Selenium + WebDriver → Tu ouvres le navigateur, attends que le JavaScript charge la page et récupères le HTML complet avant de scraper.

Convention de nommage -> PEP 8
