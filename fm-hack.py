#!/usr/bin/python3
# IMPORTANT NOTE! Transmitting on some ranges may be illigal in your country.
#Sorry for shitty code :/

import os
import requests
from bs4 import BeautifulSoup

config = {
    'stationsFile': 'stationsList.txt',
    'wavFile': 'inject.wav',
    'binaryPath': '/usr/bin/fm_transmitter',
    'stationsDataURL': 'https://top-radio.ru'
}

mainMenuObj = {
    '1': lambda: injectWav(False,
                           askUser(True, parseLinks(sendReq(config['stationsDataURL'] + "/ukraina")), 
                           keys = ['execFunct','link'])),                                                                               
    '2': lambda: injectWav(True),                              
    '3': lambda: setFile('wavFile'),                                                                                            
    '0': lambda: exit()                                                                                                          
}

BANNER = """
 _______  __   __  __   __  _______  _______  ___   _ 
|       ||  |_|  ||  | |  ||   _   ||       ||   | | |
|    ___||       ||  |_|  ||  |_|  ||       ||   |_| |
|   |___ |       ||       ||       ||       ||      _|
|    ___||       ||       ||       ||      _||     |_ 
|   |    | ||_|| ||   _   ||   _   ||     |_ |    _  |
|___|    |_|   |_||__| |__||__| |__||_______||___| |_|

----------------'  '----------------'  '----------------' 

[MENU]

[1] Parse stations frequency and inject WAV
[2] Enter frequency manualy
[3] Set WAV file
[0] Exit

"""

def showScreen(screen):
    print(screen)

def askUser(isKeySensetive, menu, keys = []):
    print("________________________________________________")
    userInput = input("[*] Select Option: ")
    if isKeySensetive:
        executionObj = menu[str(userInput)]
        return executionObj.get(keys[0], lambda: "Try again. Exiting.")(executionObj[keys[1]])
    else:
        return menu.get(userInput, lambda: "Try again. Exiting.")()

def parseStations():
    print("[*][=======] Stations frequency: ")
    i = 0
    stationsMenuObj = {}
    for station in open(config['stationsFile']):
        stationArr = station.rstrip().split(':')
        stationsMenuObj[str(i)] = {
            'execFunct': lambda freq: os.system("%s -f %s -r %s" % (config['binaryPath'],freq, config['wavFile'])),
            'freq': stationArr[1]
        }
        print("[*] [%s] Station: %s Freq: %s " % (i, stationArr[0], stationArr[1]))
        i = i + 1
    print("[*] [%s] Exit" % i)
    stationsMenuObj[str(i)] = lambda: exit()
    return stationsMenuObj

def injectWav(isManual, stationsObj = {}):
    if isManual:
        freq = input("[*] Enter freq. (Eg. 101.1): ")
        print("[*] Attack started. Press Ctrl+c to exit")
        os.system("%s -f %s -r %s" % (config['binaryPath'],freq, config['wavFile']))
    else:
        askUser(True, stationsObj, keys = ['execFunct','freq'])
        print("[*] Attack started. Press Ctrl+c to exit")

def setFile(filename):
    config[filename] = input("[*] Specify path to %s file: " % filename)

def checkTransmitterBinary(path):
    if os.path.isfile(path):
        print("[*] Transmitter binary found!")
        return True
    else:
        print("[*] fm_transmitter binary is missing in /usr/bin/")
        return False

def sendReq(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    req = requests.get(url, headers)
    return req.text

def parseLinks(html):
    htmlObj = BeautifulSoup (html, 'html.parser')
    links = {}
    i = 0
    for element in htmlObj.find_all(class_="threecolumn"):
        for aelem in element:
            links[str(i)] = {
                'execFunct': lambda link: parseFreq(sendReq(config['stationsDataURL'] + link)),
                'link': "/%s" % aelem.a['href']
            }
            print("[*] [%s] [%s] " % (i, aelem.a['href'].capitalize()))
            i = i + 1
    return links

def parseFreq(html):
    htmlObj = BeautifulSoup (html, 'html.parser')
    i = 0
    k = 0
    stationsMenuObj = {}
    freqArr = {}
    for element in htmlObj.find(class_="stations-list"):
        for freq in element.find_all(class_="frequency"):
            frequency = freq.get_text().replace(" FM","").replace(" УКВ","").rstrip()
            stationsMenuObj[str(i)] = {
                'execFunct': lambda freq: os.system("%s -f %s -r %s" % (config['binaryPath'], freq, config['wavFile'])),
                'freq': frequency
            }
            freqArr[i] = frequency
            i = i + 1
        

        for name in element.find_all(class_="name"):
            print("[*] [%s] Station: %s Freq: %s " % (k, name.get_text().rstrip(), freqArr[k]))
            k = k + 1

    print("[*] [%s] Exit" % k)
    stationsMenuObj[str(k)] = lambda: exit()
    return stationsMenuObj
    #print(stationsMenuObj)

if __name__ == "__main__":
    showScreen(BANNER)
    if checkTransmitterBinary(config['binaryPath']):
        askUser(False,mainMenuObj)
    else:
        setFile('binaryPath')
        askUser(False,mainMenuObj)
    
