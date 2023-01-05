# Sparkproject

Application de recommendation des d’Artistes Musicales en utilisaon Spark.

## Setup :
Installation des bibliothèques :
- !pip install findspark
- !pip install pyspark
- !pip install django

Changez le path de téléchargement du dataSet dans /recommenderApp/views.py
- Mettez le path du dossier qui contient les fichiers txt sur votre pc

Starting the Project :
- py manage.py runserver 8080

## DataSet :
artist_data: contient l'ID de l'artiste et le nom de l'artiste pour chaque artiste, séparés par un caractère de tabulation.
artist_alias: contient des mappages d'ID d'artiste pour des noms d'artistes mal orthographiés ou variant. Chaque ligne contient deux ID d'artiste séparés par un caractère de tabulation.
user_artist_data: contient l'ID de l'utilisateur, l'ID de l'artiste et le nombre de lectures pour chaque chanson jouée par chaque utilisateur.
