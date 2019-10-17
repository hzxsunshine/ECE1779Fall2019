#./venv/bin/gunicorn --bind 0.0.0.0:5000 --workers=1 --access-logfile access.log --error-logfile error.log app:webapp

cd
cd ./Desktop/ece1779/ECE1779Fall2019/Assignment
source ./venv/bin/activate
sudo ufw allow 5000
gunicorn -w 4 --bind 0.0.0.0:5000 wsgi:webapp
#  Compiler reads one source file from command line argument
#  Output to standard output



