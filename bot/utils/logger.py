import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "MusicBot") -> logging.Logger:
    """
    Configure un système de journalisation (logs) pour garder un œil sur la santé du bot.
    Les messages s'affichent dans la console et sont sauvegardés dans un fichier.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # On définit un format clair et lisible pour nos messages
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )

    # Sortie Console : pour voir ce qui se passe en temps réel
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Sortie Fichier : pour garder une trace en cas de souci (rotation auto à 5MB)
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = RotatingFileHandler(
        'logs/bot.log', 
        maxBytes=5*1024*1024, 
        backupCount=3, 
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Instance globale
log = setup_logger()
