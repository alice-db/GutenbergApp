cd ~/Documents/cours/DAAR/TME_webAPI_DAAR/mySearchEngine &&
source ../../myTidyVEnv/bin/activate &&
python3 manage.py RefreshBook >> ~/mySearchEngineLog &&
python3 manage.py RefreshCatalog >> ~/mySearchEngineLog &&
python3 manage.py RefreshTermes >> ~/mySearchEngineLog &&
python3 manage.py RefreshJaccard >> ~/mySearchEngineLog &&
deactivate
