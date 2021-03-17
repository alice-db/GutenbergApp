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