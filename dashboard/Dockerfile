FROM python:3.10-slim

WORKDIR /app

# Copie les deux fichiers
COPY app.py requirements.txt ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lancer Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
