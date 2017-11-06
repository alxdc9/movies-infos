import os
import subprocess
import csv
FNULL = open(os.devnull, 'w')

path = input("Entrer chemin Films: ")
list = []
for root, dirs, files in sorted(os.walk(path)):
    for file in files:
        if file.endswith(".mkv"):
            fullPath = os.path.join(path, root, file)
            print(fullPath)
            size = subprocess.check_output('mediainfo --Inform="General;%FileSize%"' + ' "' + fullPath).decode("utf-8")[:-2]
            format = subprocess.check_output('mediainfo --Inform="General;%Format%"' + ' "' + fullPath + '"').decode("utf-8")[:-2]
            width = subprocess.check_output('mediainfo --Inform="Video;%Width%"' + ' "' + fullPath + '"').decode("utf-8")[:-2]
            codec = subprocess.check_output('mediainfo --Inform="Video;%Format%"' + ' "' + fullPath + '"').decode("utf-8")[:-2]
            audioformat = subprocess.check_output('mediainfo --Inform="Audio;%Format%"' + ' "' + fullPath + '"').decode("utf-8")[:-2]
            audiocodec = subprocess.check_output('mediainfo --Inform="Audio;%CodecID%"' + ' "' + fullPath + '"').decode("utf-8")[:-2]
            list.append({'nom': file, 'taille': size, 'format': format, 'largeur': width, 'codec': codec, 'format_audio': audioformat, 'codec_audio': audiocodec})

print(list)

keys = list[0].keys()
with open('films.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(list)