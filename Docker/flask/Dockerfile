# On utilise une image Python3.7.2
FROM python:3.7.2-stretch

# On va travailler dans /app
WORKDIR /app

# On ajoute le répertoire courant (contennt le code de l'application) dans app 
ADD . /app

# On installe les dépendances nécessaires
RUN pip install -r requirements.txt

# On lance uwsgi (et donc l'application)
CMD ["uwsgi", "app.ini"]
