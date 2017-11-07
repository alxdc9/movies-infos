import os
import subprocess
import csv
import argparse
import tkinter as tk
from tkinter import filedialog

FNULL = open(os.devnull, 'w')
mediaInfo = os.path.join('bin', 'MediaInfo')
params = {'size': 'General;%FileSize%',
          'format': 'General;%Format%',
          'width': 'Video;%Width%',
          'codec': 'Video;%Format%',
          'audioformat': 'Audio;%Format%',
          'audiocodec': 'Audio;%CodecID%'}

def scan(dir, extensions):
    dir = os.path.abspath(dir)
    list = []
    for root, dirs, files in sorted(os.walk(dir)):
        for file in files:
            if file.endswith(tuple(extensions)):
                fullPath = ' "' + os.path.join(dir, root, file) + '"'
                print(fullPath)
                fullPath = ' "' + fullPath + '"'
                infos = {'name': file}
                for name, arg in params.items():
                    fct = ' --Inform='
                    cmd = mediaInfo + fct + arg + ' "' + fullPath + '"'
                    infos[name] = subprocess.check_output(cmd).decode('utf-8')[:-2]

                list.append(infos)
                print(infos)
                print()
    
    return list

def writeCSV(list):
    keys = list[0].keys()
    with open('movies-infos.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(list)
    
def parseArgs():
    parser = argparse.ArgumentParser(description='Scans all movies in a given folder and outputs a CSV file with required detauls about the movies')
    parser.add_argument('-d', '--dir', help='Directory to be scanned', default='', required=False)
    parser.add_argument('-e', '--ext', help='File extensions to look for', nargs='+', default=['.mkv', '.mp4', '.avi'], required=False)
    
    return parser.parse_args()

def browse():
    root = tk.Tk()
    root.withdraw()
    
    return filedialog.askdirectory()

if __name__ == '__main__':
    args = parseArgs()
    dir = args.dir
    extensions = args.ext

    if dir == '':
        dir = browse()

    list = scan(dir, extensions)
    writeCSV(list)
    print('Done')
