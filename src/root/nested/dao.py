'''
Created on 9 Jan 2018

@author: seantmcmahon
'''

import pandas as pd

class Dao:
    
    def __init__(self):
        self.stations = {
        "Aberporth"             : pd.read_csv('stationData/aberporth.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Armagh"                : pd.read_csv('stationData/armagh.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Ballypatrick Forest"   : pd.read_csv('stationData/ballypatrickForest.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Bradford"              : pd.read_csv('stationData/bradford.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Braemar"               : pd.read_csv('stationData/braemar.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Camborne"              : pd.read_csv('stationData/camborne.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Cambridge NIAB"        : pd.read_csv('stationData/cambridgeNIAB.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Cardiff Bute Park"     : pd.read_csv('stationData/cardiffButePark.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Chivenor"              : pd.read_csv('stationData/chivenor.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Cwmystwyth"            : pd.read_csv('stationData/cwmystwyth.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Dunstaffnage"          : pd.read_csv('stationData/dunstaffnage.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Durham"                : pd.read_csv('stationData/durham.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Eastbourne"            : pd.read_csv('stationData/eastbourne.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Eskdalemuir"           : pd.read_csv('stationData/eskdalemuir.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Heathrow"              : pd.read_csv('stationData/heathrow.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Hurn"                  : pd.read_csv('stationData/hurn.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Lerwick"               : pd.read_csv('stationData/lerwick.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Leuchars"              : pd.read_csv('stationData/leuchars.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Lowestoft"             : pd.read_csv('stationData/lowestoft.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Manston"               : pd.read_csv('stationData/manston.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Nairn"                 : pd.read_csv('stationData/nairn.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Newton Rigg"           : pd.read_csv('stationData/newtonRigg.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Oxford"                : pd.read_csv('stationData/oxford.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Paisley"               : pd.read_csv('stationData/paisley.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Ringway"               : pd.read_csv('stationData/ringway.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "RossOnWye"             : pd.read_csv('stationData/rossOnWye.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Shawbury"              : pd.read_csv('stationData/shawbury.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Sheffield"             : pd.read_csv('stationData/sheffield.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Southampton"           : pd.read_csv('stationData/southampton.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Stornoway"             : pd.read_csv('stationData/stornoway.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Sutton Bonington"      : pd.read_csv('stationData/suttonBonington.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Tiree"                 : pd.read_csv('stationData/tiree.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Valley"                : pd.read_csv('stationData/valley.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Waddington"            : pd.read_csv('stationData/waddington.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Whitby"                : pd.read_csv('stationData/whitby.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Wick Airport"          : pd.read_csv('stationData/wickAirport.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python'),
        "Yeovilton"             : pd.read_csv('stationData/yeovilton.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
        
        }

        self.countryStationsMap =  {
            "Scotland"          : ["Braemar", "Dunstaffnage", "Eskdalemuir", "Lerwick", "Leuchars", "Nairn", "Paisley", "Stornoway", "Tiree", "Wick Airport"],
            "England"           : ["Bradford", "Camborne", "Cambridge NIAB", "Chivenor", "Durham", "Eastbourne", "Heathrow", "Hurn", "Lowestoft", "Manston", "Newton Rigg", "Oxford", "Ringway", "Shawbury", "Sheffield", "Southampton", "Sutton Bonington", "Waddington", "Whitby", "Yeovilton"],
            "Wales"             : ["Aberporth", "Cardiff Bute Park", "Cwmystwyth", "Ross-On-Wye"],
            "Northern Ireland"  : ["Armagh", "Ballypatrick Forest"]
        }
