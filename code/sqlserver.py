# Exécution du serveur : mysqld
# Connexion en CLI : mysql -u root
# Fermeture du serveur : killall -TERM mysqld
# https://gist.github.com/hofmannsven/9164408

import subprocess
import os
import time

sqlserver = subprocess.Popen(["mysqld"],stderr = subprocess.DEVNULL)

print("Récupération des données depuis la BD..")

time.sleep(2)

os.system("mysql -u root sys -e 'SELECT * FROM host_summary'")

sqlserver.terminate()