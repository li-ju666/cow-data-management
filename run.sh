sudo mkdir -p result_files
sudo mkdir -p input_files
sudo mkdir -p input_files/info
sudo mkdir -p input_files/position
sudo rm mysql -rf
sudo rm result_files/* -f
docker-compose up
