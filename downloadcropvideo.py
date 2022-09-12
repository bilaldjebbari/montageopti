import pytube
import os
import csv
from pathlib import Path

listVideos = 'script-image.csv'

link = None
secondDebut = None
duration = None
i = 0
listResultatToConcat = []
# on boucle sur chaque ligne du csv
with open(listVideos, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        i += 1
        link = row[0]
        secondDebut = row[1]
        duration = row[2]
        # on recupere les informations de youtube sur la video courante
        yt = pytube.YouTube(link,
        use_oauth=True,
        allow_oauth_cache=True)
        # recuperation du nom, en enlevant les espaces et autres caracteres speciaux, pour pas se prendre la tete
        filename = yt.title.replace(" ","")
        filename = ''.join(e for e in filename if e.isalnum())
        audioExtension = '.aac'
        videoExtension = '.mp4'
        videoName = filename+videoExtension
        audioName = 'audio-'+filename+videoExtension
        # pour s'en sortir dans la phase de montage, on prefixe la video par le numero de la ligne
        # on aura aussi parfois des pistes audio, d'ou un prefixe egalement, je l'explique plus bas
        resultatVideoFolder = f'./resultat/{i}-{secondDebut+filename+videoExtension}'
        resultatAudioFolder = f'./resultat/{i}-audio-{secondDebut+filename+audioExtension}'
        videoFile = './videos/'+videoName
        audioFile = './videos/'+audioName
        path = Path(videoFile)
        pathExist = path.is_file()
        streamVideo = yt.streams.filter(progressive=False, type='video',file_extension='mp4').order_by('resolution').desc().first()
        # si on a deja le fichier, on a juste besoin de couper la video, pas de la telecharger
        # la complexite de youtube : pour les resolution 1080p et au-dela, on a besoin de telecharger la piste video et audio separement
        # pour les resolutions 720p voir 480p, on filtre sur le "progressive=True" qui renvoit seulement les streams qui contiennent les 2 pistes assemblees
        if not pathExist:            
            print('file not exist')
            print(streamVideo)
            if(streamVideo.resolution == '720p' or streamVideo.resolution == "480p"):
                yt.streams.filter(progressive=True, type='video',file_extension='mp4').order_by('resolution').desc().first().download('videos',videoName)    
                # on utilise une commande native de ffmpeg pour couper l'extrait
                # il faut donc avoir installé ffmpeg sur son poste, en ajoutant son répertoire dans les variables d'environnement
                os.system(f'ffmpeg -ss {secondDebut} -i {videoFile} -t {duration} {resultatVideoFolder}')
            else:
                streamAudio = yt.streams.get_audio_only()
                streamVideo.download('videos',videoName)
                streamAudio.download('videos',audioName)
                os.system(f'ffmpeg -ss {secondDebut} -i {audioFile} -t {duration} {resultatAudioFolder}')
                os.system(f'ffmpeg -ss {secondDebut} -i {videoFile} -t {duration} {resultatVideoFolder}')
        else:
            print('file exist')
            print(streamVideo)
            if(streamVideo.resolution == '720p' or streamVideo.resolution == "480p"):
                os.system(f'ffmpeg -ss {secondDebut} -i {videoFile} -t {duration} {resultatVideoFolder}')
            else:
                os.system(f'ffmpeg -ss {secondDebut} -i {audioFile} -t {duration} {resultatAudioFolder}')
                os.system(f'ffmpeg -ss {secondDebut} -i {videoFile} -t {duration} {resultatVideoFolder}')