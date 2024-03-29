pip install pandas
pip install lxml
pip install openpyxl

mkdir media
mkdir media/planilhas

chmod 777 media/planilhas
chmod 777 media/

apt install mysql-server
mysql_secure_installation
mysql
DROP USER root@localhost;
flush privileges;
CREATE USER 'amox_admin'@'localhost' IDENTIFIED BY '@AmoxSql#2021';
FLUSH PRIVILEGES;
GRANT SELECT ON * . * TO 'amox_admin'@'localhost';
CREATE SCHEMA amox_db;
GRANT ALL PRIVILEGES ON amox_db . * TO 'amox_admin'@'localhost';

apt install python3-venv
apt install python3
apt install pip
python3 -m venv venv
source venv/bin/activate
pip install django
pip install mysqlclient

python manage.py collectstatic
python manage.py makemigrations AmoxProject
python manage.py migrate AmoxProject
python manage.py runserver
