cd ~/Documents/cours/DAAR/TME_webAPI_DAAR/mySearchEngine &&
source ../../myTidyVEnv/bin/activate &&
python3 manage.py refreshOnSaleList >> ~/mySearchEngineLog &&
python3 manage.py refreshOnAvailableList >> ~/mySearchEngineLog &&
deactivate
