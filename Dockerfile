FROM ubuntu
RUN mkdir /app && apt update && apt install -y python3-pip
COPY cow-app /app/cow-app

RUN pip3 install mysql-connector-python pandas numpy django openpyxl psutil
CMD cd /app/cow-app && ./run.sh
