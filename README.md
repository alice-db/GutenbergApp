# GutenbergApp
A search engine based on the Gutenberg library

# Start server
`python3 manage.py runserver`

# Migrate Database 
`python3 manage.py makemigrations mygutenberg`
`python3 manage.py migrate`

# Run script 
###### Create catalog
`python3 manage.py RefreshCatalog`
###### Refresh catalog
`python3 manage.py RefreshAll`
###### Refresh english books
`python3 manage.py RefreshEnglish`
###### Refresh french books
`python3 manage.py RefreshFrench`


# JAR FILE
Run with db.Sqlite3
mvn clean install assembly:single

# A FAIRE
-> Recherche simple
-> Continuer RegEx
-> Classement
-> Mettre à jour les urls de la base
-> Mettre à jour les termes
-> Enregistrer de nouveaux livres
-> Enregistrer de nouveaux termes



