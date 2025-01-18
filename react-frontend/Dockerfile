FROM node:18-alpine

# Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten installieren
COPY package.json package-lock.json ./
RUN npm install

# Frontend-App kopieren
COPY . .

# React App starten
CMD ["npm", "start"]
