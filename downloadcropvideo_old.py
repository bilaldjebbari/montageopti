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
        streamList = yt.streams.filter(adaptive=True, type='video').order_by('resolution').desc()
        stream = None
        audio = None
        extension = None
        output = None
        audioExtension = '.mp3'
        if len(streamList):
            stream = streamList.first()
            if(stream.resolution == '1440p' or stream.resolution == '2160p'):
                extension = '.webM'
                output = './videos/'+filename[0:10]+extension
                path = Path(output)
                pathExist = path.is_file()
                if not pathExist:
                    print(f'dans le if exist du webM : {output}')
                    output = stream.download('videos',filename+extension)
                    audio = yt.streams.filter(only_audio=True,file_extension='webm').order_by('abr').desc().first().download('videos','audio'+filename+audioExtension)
                    os.system(f'ffmpeg -ss {secondDebut} -i {audio} -t {duration} -c copy -f webm ./resultat/{i}-audio{secondDebut+filename+extension}')
                    os.system(f'ffmpeg -ss {secondDebut} -i {output} -t {duration} -c copy -f webm ./resultat/{i}-{secondDebut+filename+extension}')
                    continue
                    #video = ffmpeg.input(output)
                    #audioFile = ffmpeg.input(audio)
                    #ffmpeg.output(video, audioFile, output).run()    
            else:
                extension = '.mp4'
                output = './videos/'+filename+extension
                path = Path(output)
                pathExist = path.is_file()
                if not pathExist:
                    stream = yt.streams.filter(progressive=False, type='video', file_extension='mp4').order_by('resolution').desc().first()
                    print(stream)
                    stream = stream.download('videos',filename+extension)
        else:
            extension = '.mp4'
            output = './videos/'+filename+extension
            path = Path(output)
            pathExist = path.is_file()
            if not pathExist:
                stream = yt.streams.filter(progressive=False, type='video', file_extension='mp4').order_by('resolution').desc().first()
                print(stream)
                stream = stream.download('videos',filename+extension)
        print(secondDebut)
        os.system(f'ffmpeg -ss {secondDebut} -i {output} -t {duration} -c:v libx264 -crf 30 ./resultat/{i}-{secondDebut+filename+extension}')
#        listResultatToConcat.append(f'./resultat/{secondDebut+filename+extension}')


#concatResultat = ''
#for resultat in listResultatToConcat:
#    concatResultat = concatResultat+f'-i {resultat} '
#print(concatResultat)
#os.system(f'ffmpeg {concatResultat} -filter_complex "[0]setdar=16/9[a];[1]setdar=16/9[b];[2]setdar=16/9[c];[3]setdar=16/9[d];[a][b][c][d]concat=n=4:v=1:a=1" final.mp4')