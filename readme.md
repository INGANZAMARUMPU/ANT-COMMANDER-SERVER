pour executer cette application il vous faut un certificat https.
voici les commandes powershell pour creer un certificat sous windows

```shell
# installation de choco

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# installation mkcert
choco install mkcert

# generation du certificat (address ip ou nom de domaine de votre serveur)
mkcert -cert-file cert.pem -key-file key.pem localhost 192.168.43.135
```

Au lieu de demarrer l'application avec ```manage.py```, vous allez utiliser ```Daphne```

```bash
python pip install daphne
daphne -e ssl:8000:privateKey=cert.pem:certKey=key.pem ANT_COMMANDER.asgi:application
```