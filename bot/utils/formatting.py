import math

def format_duration(seconds: int) -> str:
    """
    Formate une durée en secondes en format HH:MM:SS ou MM:SS.
    """
    if seconds == 0:
        return "Direct"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def create_progress_bar(current: int, total: int, size: int = 15) -> str:
    """
    Crée une barre de progression visuelle.
    """
    if total <= 0:
        return "🔘" + "▬" * (size - 1)
        
    percentage = current / total
    progress = math.floor(size * percentage)
    
    bar = "▬" * progress + "🔘" + "▬" * (size - progress - 1)
    return bar
