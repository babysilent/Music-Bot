# 🎵 Discord Music Bot - Senior Python Edition

Un bot Discord de musique haute performance, modulaire et moderne, conçu avec `discord.py` et `yt-dlp`.

## 🚀 Fonctionnalités

- **Lecture Multi-plateforme** : Support de YouTube, Spotify, SoundCloud et plus.
- **Commandes Slash** : Interface moderne et intuitive.
- **Système de Queue Avancé** : Gestion par serveur, shuffle, loop, et historique.
- **Qualité Audio** : Streaming haute fidélité via FFmpeg.
- **Effets Audio** : Filtres en temps réel (Bassboost, Nightcore, etc.).
- **Paroles** : Intégration de l'API Genius pour afficher les paroles.
- **Architecture Propre** : Code typé, commenté et facile à maintenir.

## 🛠️ Installation

### Prérequis
- Python 3.12 ou supérieur
- FFmpeg (obligatoire pour l'audio)
- Un token de Bot Discord

### Installation Locale
1. Clonez le dépôt :
   ```bash
   git clone <url-du-repo>
   cd "Music Bot"
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez l'environnement :
   - Renommez `.env.example` en `.env`
   - Remplissez les informations nécessaires (`DISCORD_TOKEN`, etc.)

4. Lancez le bot :
   ```bash
   python bot/main.py
   ```

### Installation FFmpeg
- **Windows** : Téléchargez sur [ffmpeg.org](https://ffmpeg.org/download.html), extrayez et ajoutez le dossier `bin` à votre PATH.
- **Linux** : `sudo apt update && sudo apt install ffmpeg`
- **Mac** : `brew install ffmpeg`

## 🐳 Docker
Le bot est prêt pour Docker.
```bash
docker build -t music-bot .
docker run --env-file .env music-bot
```

## 📜 Commandes Disponibles
- `/play` : Jouer une musique (URL ou recherche)
- `/pause` : Mettre en pause
- `/resume` : Reprendre
- `/skip` : Passer au suivant
- `/stop` : Tout arrêter
- `/queue` : Voir la file d'attente
- `/nowplaying` : Voir la musique actuelle
- `/volume` : Régler le son
- `/loop` : Changer le mode de boucle
- `/shuffle` : Mélanger la queue
- `/lyrics` : Afficher les paroles
- `/filter` : Appliquer un effet audio

## 🔧 Dépannage
- **Audio saccadé** : Vérifiez la connexion internet du serveur ou la charge CPU.
- **Erreur FFmpeg** : Assurez-vous que FFmpeg est correctement installé et accessible via la console.
- **Spotify ne fonctionne pas** : Vérifiez vos identifiants API sur le dashboard Spotify Developer.

---
Développé avec ❤️ par un Senior Python Dev.
