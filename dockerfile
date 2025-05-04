# Utilise une image Python officielle
FROM python:alpine

# Crée un dossier de travail
WORKDIR /app

# Copie les fichiers dans l'image
COPY ./volatibot/ .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut
CMD ["python", "main.py"]
