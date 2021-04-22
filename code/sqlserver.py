#!/usr/bin/env python3
# Exécution du serveur : mysqld
# Connexion en CLI : mysql -u root
# Fermeture du serveur : killall -TERM mysqld
# https://gist.github.com/hofmannsven/9164408

# import subprocess
# import os
# import time

# sqlserver = subprocess.Popen(["mysqld"],stderr = subprocess.DEVNULL)

# print("Récupération des données depuis la BD..")

# time.sleep(2)

# os.system("sudo mysql -u root sys -e 'SELECT * FROM host_summary'")

# sqlserver.terminate()

# import os
# import time

# sqlserver = subprocess.Popen(["mysqld"],stderr = subprocess.DEVNULL)

# print("Récupération des données depuis la BD..")

# time.sleep(2)

# os.system("sudo mysql -u root sys -e 'SELECT * FROM host_summary'")

# sqlserver.terminate()

import os
import sys

if sys.platform.startswith('darwin'):
    
    os.system("mysql.server start")

    os.system("mysql -u root -e 'CREATE DATABASE cards;'")

    print("Generating cards inside the database, please wait..")

    os.system("mysql -u root cards < ../resources/card_database.sql")

    input("Press enter to print something")

    os.system("mysql -u root cards -e 'SELECT * FROM mag_card'")

    os.system("mysql -u root -e 'DROP DATABASE cards;'")

    os.system("mysql.server stop")

elif sys.platform.startswith('linux'):

    os.system("sudo service mysql start")

    os.system("sudo mysql -u root -e 'CREATE DATABASE cards;'")

    print("Generating cards inside the database, please wait..")

    os.system("sudo mysql -u root cards < ../resources/card_database.sql")

    input("Press enter to print something")

    os.system("sudo mysql -u root cards -e 'SELECT * FROM mag_card'")

    os.system("sudo mysql -u root -e 'DROP DATABASE cards;'")

    os.system("sudo service mysql stop")