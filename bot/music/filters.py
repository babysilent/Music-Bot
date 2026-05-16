class AudioFilters:
    """
    Définition des filtres FFmpeg pour les effets audio.
    """
    FILTERS = {
        'bassboost': 'bass=g=20,dynaudnorm=f=200',
        'nightcore': 'asetrate=44100*1.25,atempo=1.25,aresample=44100',
        'reverb': 'aecho=0.8:0.88:60:0.4',
        'vaporwave': 'asetrate=44100*0.8,atempo=0.8,aresample=44100',
        'karaoke': 'stereoflow=center=1',
        'lowpass': 'lowpass=f=500',
        'highpass': 'highpass=f=5000'
    }

    @classmethod
    def get_filter(cls, filter_name: str) -> str | None:
        return cls.FILTERS.get(filter_name.lower())
