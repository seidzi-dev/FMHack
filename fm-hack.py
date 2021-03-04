#!/usr/bin/python3
# IMPORTANT NOTE! Transmitting on some ranges may be illigal in your country.
# Author: @s3idzi(Telegram)
#Sorry for shitty code :/

import os

WAVFILE = 'inject.wav'
STATIONSFILE = 'stationsList.txt'

mainMenuObj = {
    '1': lambda: parseStations(),           #Start Attack
    '2': lambda: exit()                     #Exit
}

def showBanner():
    banner = """
.----------------.  .----------------.   .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || | ____    ____ | | | |  ____  ____  | || |      __      | || |     ______   | || |  ___  ____   | |
| | |_   ___  |  | || ||_   \  /   _|| | | | |_   ||   _| | || |     /  \     | || |   .' ___  |  | || | |_  ||_  _|  | |
| |   | |_  \_|  | || |  |   \/   |  | | | |   | |__| |   | || |    / /\ \    | || |  / .'   \_|  | || |   | |_/ /    | |
| |   |  _|      | || |  | |\  /| |  | | | |   |  __  |   | || |   / ____ \   | || |  | |         | || |   |  __'.    | |
| |  _| |_       | || | _| |_\/_| |_ | | | |  _| |  | |_  | || | _/ /    \ \_ | || |  \ `.___.'\  | || |  _| |  \ \_  | |
| | |_____|      | || ||_____||_____|| | | | |____||____| | || ||____|  |____|| || |   `._____.'  | || | |____||____| | |
| |              | || |              | | | |              | || |              | || |              | || |              | |
| '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' || '--------------' |
'----------------'  '----------------'   '----------------'  '----------------'  '----------------'  '----------------' 

[MENU]

[1] Start Attack
[2] Exit

__________________________________________________________________________________________________________________________
    """
    print(banner)

def askUser(userInput,menu):
    return menu.get(userInput, lambda: "Try again. Exiting.")()

def parseStations():
    print("[*][=======] Stations frequency: ")
    i = 0
    stationsMenuObj = {}
    for station in open(STATIONSFILE):
        stationArr = station.rstrip().split(':')
        stationsMenuObj[i] = lambda: os.system("fm_transmitter -f %s -r %s" % (stationArr[1], WAVFILE))
        print("[*] [%s] Station: %s Freq: %s " % (i, stationArr[0], stationArr[1]))
        i = i + 1
    print("[*] Exit")
    stationsMenuObj[i] = lambda: exit()

    return stationsMenuObj


if __name__ == "__main__":
    showBanner()
    menuObj = askUser(input("[*] >>>Select Option: "), mainMenuObj)
    print("___________________________________________________________")
    askUser(input("[*] >>>Select Option: "), menuObj)
    print("[*] Attack started. Press Ctrl+C to exit")
    
