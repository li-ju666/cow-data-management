mkdir -p log
touch log/query_log.txt
mkdir -p result_files
mkdir -p upload_files
mkdir -p upload_files/se
mkdir -p upload_files/nl
sudo chmod 777 -R upload_files
sudo chmod 777 -R result_files
sudo chmod 777 -R log
# sudo rm mysql -rf
# sudo rm result_files/* -f
docker-compose up --build
