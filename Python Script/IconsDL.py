"""MIT License

Copyright (c) 2019 Zdravko Georgiev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. """

import sys
import urllib.error
import urllib.request
import threading

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

import ssl, urllib3, sys, os, re

from configparser import ConfigParser
from bs4 import BeautifulSoup as BSHTML
from colorama import init, Fore, Back, Style
from PIL import Image

configPath = "settings.ini"
config = ConfigParser()
config.read(configPath)
sg.theme("Default1")


def download(url, names):
    urllib3.disable_warnings()

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    try:
        if urllib.request.urlretrieve(url, names):
            return True
        else:
            return False
    except IOError as e:
        print(e)
        return False

def get_numbers_from_link():
    icon_pack = []
    icon_links = str(config.get("Icons", "downloadList")).strip()
    if len(icon_links) > 0:
        icon_links = icon_links.split(",")
        count = 0
        for tf in icon_links:
            count += 1
            if tf.isdigit():
                icon_pack.append(tf)
            else:
                continue
    else:
        icon_pack = list(range(config.getint("Icons", 'lastdownload'), config.getint("Icons", 'end_to')))

    return icon_pack


def convertICO(dir, type):
    for eachico in dir:
        if eachico.endswith(".png"):
            try:
                img = Image.open(eachico)
                icon_sizes = [(type, type)]
                path = os.path.join(eachico.split("\\")[0], eachico.split("\\")[1])
                ico_name = eachico.split("\\")[2] + ".ico"
                ico_dir = os.path.join(path, "ICO{}x{}".format(type, type))
                if not os.path.isdir(ico_dir):
                    os.mkdir(ico_dir)
                img.save(os.path.join(path, ico_dir, ico_name), sizes=icon_sizes)
            except:
                return


def get_valid_filename(filename):
    return re.sub(r'[\\\\/*?:"<>|]'," ",filename)

def lazyLoader(proccess):
    thread = threading.Thread(target=proccess, daemon=True)
    thread.start()
    while True:
        sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'Loading... ', time_between_frames=1)
        thread.join(timeout=.1)
        if not thread.is_alive():
            break
    sg.popup_animated(None)


layout = [
    [sg.Frame("", layout=(
        [sg.Frame("Icons-Ico Download List", background_color="#d4d0c8", pad=(10, 10), font="Helvetica 11", layout=(
            [sg.Multiline(
                tooltip=" \n   List all Icon Pack Numbers that you want to download, separated by a comma\n    Example: 2080,98,66,33.\n    These numbers can be taken from the end of the icon link -> https://icon-icons.com/pack/Social-Media/2080\n\n",
                font=("Helvetica 7"), autoscroll=True, enable_events=True, enter_submits=True,
                auto_size_text=True, size=(85, 5), key="_multi_list_",
                default_text=str(config.get("Icons", "downloadList")), background_color="#FFF")],
            [sg.InputText(config.get("Icons", "dlpath"), key="_dl_path_", enable_events=True, background_color="#FFF",
                          size=(34, 1)),
             sg.FolderBrowse(button_text="Download Directory", key="change_dl", enable_events=True,
                             button_color=('#FFF', '#444'), )]
        )
                  )],
        [sg.Frame("Download Options ", pad=(10, 10), font="Helvetica 11", layout=(
            [sg.Frame("Start from              Finish at", pad=(10, 10), background_color="#d4d0c8", layout=[
                [
                    sg.In(size=(10, 1), key="lastdownload", default_text=config.getint("Icons", "lastdownload")),
                    sg.In(size=(10, 1), key="end_to", default_text=config.getint("Icons", "end_to"))

                ]]
                      )],
            [sg.Frame("Add ICO Files", background_color="#d4d0c8", layout=[
                [sg.Checkbox(text="16x16", key="_ico16_", enable_events=True,
                             default=config.getboolean("Convert", "icosizes16")),
                 sg.Checkbox(text="24x24", key="_ico24_", enable_events=True,
                             default=config.getboolean("Convert", "icosizes24")),
                 sg.Checkbox(text="32x32", key="_ico32_", enable_events=True,
                             default=config.getboolean("Convert", "icosizes32")),
                 sg.Checkbox(text="48x48", key="_ico48_", enable_events=True,
                             default=config.getboolean("Convert", "icosizes48")),
                 sg.Checkbox(text="64x128", key="_ico64_", enable_events=True,
                             default=config.getboolean("Convert", "icosizes64")),
                 sg.Checkbox(text="128x128", key="_ico128_", enable_events=True,
                             default=config.getboolean("Convert", "icosizes128"))]
            ]
                      )],
        )
                  )],
        [sg.Col(
            layout=([[sg.Button('Start', button_color=('#FFF', '#444'), size=(20, 1), key="_start_", enable_events=True,
                                auto_size_button=False, )
                      ]]), element_justification="center", justification="center")

         ],
        [sg.Col(
            layout=([[sg.Output(size=(170, 20))]]), element_justification="center", justification="center")

        ],
    ), element_justification="center")],
]


window = sg.Window('Icon-Icons Downloader v.1.1 by r00tme', icon="",
                   element_justification="center",
                   auto_size_buttons=True,
                   background_color="#d4d0c8",
                   use_default_focus=True,
                   text_justification="center",
                   return_keyboard_events=True,
                   ).Layout(layout).Finalize()

while True:
     event, values = window.Read()
     if event == sg.WIN_CLOSED:
         exit()
     if event is not sg.TIMEOUT_KEY:
         if event == "_start_":
             config.set('Icons', 'downloadlist', str(values['_multi_list_']))
             config.set('Icons', 'dlpath', str(values['_dl_path_']))
             config.set('Icons', 'lastdownload', str(values['lastdownload']))
             config.set('Icons', 'end_to', str(values['end_to']))
             config.set('Convert', 'icosizes16', str(values['_ico16_']))
             config.set('Convert', 'icosizes24', str(values['_ico24_']))
             config.set('Convert', 'icosizes32', str(values['_ico32_']))
             config.set('Convert', 'icosizes48', str(values['_ico48_']))
             config.set('Convert', 'icosizes64', str(values['_ico64_']))
             config.set('Convert', 'icosizes128', str(values['_ico128_']))
             with open(configPath, "w+") as f:
                 config.write(f)
             break

page = 1
total = 0
temp_counter = 0
http = urllib3.PoolManager()



for icons_number in get_numbers_from_link():

    ico_paths = []
    icons_number = int(icons_number)
    count_temp = 0
    while True:
        count = 0
        url = 'https://icon-icons.com/pack/Simplicio/{}&page={}'.format(icons_number, page)
        response = http.request('GET', url)
        soup = BSHTML(response.data, "html.parser")
        images = soup.findAll('img')
        pack_name = get_valid_filename(str(re.findall("<h1>(.*?)</h1>", str(soup))[0])).replace("Pack","")
        imageData = re.findall("data-original=(\".*?)\"", str(images))
        newDir = os.path.join(config.get("Icons", "dlpath"), pack_name)


        if len(imageData) == 0:
            config.set("Icons", "lastdownload", str(int(icons_number) + 1))
            with open(configPath, "w+") as f:
                config.write(f)
            if config.getboolean("Convert", 'icosizes16'):
                sys.stdout.write("Convert 16x16 Icons\n")
                convertICO(ico_paths, type=16)
            if config.getboolean("Convert", 'icosizes24'):
                sys.stdout.write("Convert 24x24 Icons Pack\n")
                convertICO(ico_paths, type=24)
            if config.getboolean("Convert", 'icosizes32'):
                sys.stdout.write("Convert 32x32 Icons Pack\n")
                convertICO(ico_paths, type=32)
            if config.getboolean("Convert", 'icosizes48'):
                sys.stdout.write("Convert 48x48 Icons Pack\n")
                convertICO(ico_paths, type=48)
            if config.getboolean("Convert", 'icosizes64'):
                sys.stdout.write("Convert 64x64 Icons Pack\n")
                convertICO(ico_paths, type=64)
            if config.getboolean("Convert", 'icosizes128'):
                sys.stdout.write("Convert 128x128 Icons Pack\n")
                convertICO(ico_paths, type=128)
            temp_counter += 1
            icons_number += 1
            page = 1
            continue

        if not os.path.isdir(newDir):
            try:
                os.mkdir(newDir)
            except:
                sys.stdout.write("Directory %s can not be created \n" % (newDir))
                continue

            if len(get_numbers_from_link()) == temp_counter:
                print("The icon packs {} were successfully downloaded".format(pack_name))
            break

        for eachLink in imageData:

            total += 1
            count += 1
            count_temp += 1
            eachLink = str(eachLink.strip("\""))
            proper_name = eachLink.split("/")[::-1][0]

            try:
                urllib.request.urlopen(eachLink)
            except:
                continue


            if count == len(imageData):
                page += 1
                break
            else:
                passed = True
                try:
                    download(eachLink, newDir + "\\" + proper_name)
                except EOFError as e:
                    passed = False
                    sys.stdout.write("File %s can not be downloaded.%s\n" % (os.path.join(newDir, proper_name), e))
                    continue
                finally:
                    if passed:
                        ico_paths.append(os.path.join(newDir, proper_name))
                        sys.stdout.write(
                            "%06d | Pack %04d | Page %02d | %04d | %s\n" %
                            (total, int(icons_number),
                             page, count_temp,
                             os.path.join(newDir, proper_name)))