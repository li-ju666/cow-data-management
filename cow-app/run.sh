#rm -rf log
mkdir -p log
touch log/query_log.txt
python3 manage.py runserver 0.0.0.0:8000
