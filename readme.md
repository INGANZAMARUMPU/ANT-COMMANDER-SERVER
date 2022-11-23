pour executer cette application il vous faut un certificat https car chrome n'accepte pas par defaut l'ouverture d'un camera sur une connexion http qui n'est pas le *localhost* et les websockets du *https* exigent un backend en *wss*. Voici les commandes powershell pour creer un certificat https sous windows

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
# installation de daphne
python pip install daphne

# execution au port 8000 avec les certificats https
daphne -e ssl:8000:privateKey=cert.pem:certKey=key.pem ANT_COMMANDER.asgi:application
```