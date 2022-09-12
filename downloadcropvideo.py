import pytube
import ffmpeg
import os
import csv
from pathlib import Path

listVideos = 'script-image.csv'

link = None
secondDebut = None
duration = None
i = 0
listResultatToConcat = []
with open(listVideos, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        i += 1
        link = row[0]
        secondDebut = row[1]
        duration = row[2]
        yt = pytube.YouTube(link,
        use_oauth=True,
        allow_oauth_cache=True)
        filename = yt.title.replace(" ","")
        filename = ''.join(e for e in filename if e.isalnum())
        videoFile = None
        audioFile = None
        audio = None
        audioExtension = '.aac'
        extension = '.mp4'
        videoName = filename+extension
        audioName = 'audio-'+filename+extension
        resultatVideoFolder = f'./resultat/{i}-{secondDebut+filename+extension}'
        resultatAudioFolder = f'./resultat/{i}-audio-{secondDebut+filename+audioExtension}'
        output = None
        videoFile = './videos/'+videoName
        audioFile = './videos/'+audioName
        path = Path(videoFile)
        pathExist = path.is_file()

        if not pathExist:
            streamVideo = yt.streams.filter(progressive=False, type='video',file_extension='mp4').order_by('resolution').desc().first()
            print('file not exist')
            print(streamVideo)
            streamAudio = yt.streams.get_audio_only()
            if(streamVideo.resolution == '720p' or streamVideo.resolution == "480p"):
                output = yt.streams.filter(progressive=True, type='video',file_extension='mp4').order_by('resolution').desc().first().download('videos',videoName)    
                os.system(f'ffmpeg -ss {secondDebut} -i {output} -t {duration} {resultatVideoFolder}')
            else:
                output = streamVideo.download('videos',videoName)
                audio = streamAudio.download('videos',audioName)
                os.system(f'ffmpeg -ss {secondDebut} -i {audio} -t {duration} {resultatAudioFolder}')
                os.system(f'ffmpeg -ss {secondDebut} -i {output} -t {duration} {resultatVideoFolder}')
        else:
            streamVideo = yt.streams.filter(progressive=False, type='video',file_extension='mp4').order_by('resolution').desc().first()
            print('file exist')
            print(streamVideo)
            streamAudio = yt.streams.get_audio_only()
            if(streamVideo.resolution == '720p' or streamVideo.resolution == "480p"):
                os.system(f'ffmpeg -ss {secondDebut} -i {videoFile} -t {duration} {resultatVideoFolder}')
            else:
                os.system(f'ffmpeg -ss {secondDebut} -i {audioFile} -t {duration} {resultatAudioFolder}')
                os.system(f'ffmpeg -ss {secondDebut} -i {videoFile} -t {duration} {resultatVideoFolder}')