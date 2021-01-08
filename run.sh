mkdir -p result_files
mkdir -p input_files
mkdir -p input_files/info
mkdir -p input_files/position
sudo chmod 777 -R input_files
sudo chmod 777 -R result_files
sudo rm mysql -rf
sudo rm result_files/* -f
docker-compose up -d --build
