#system packages
import os
import pwd
import time
import json
import datetime
from dateutil import parser

#Web packages
import requests

#Data wrestling
import numpy as np
import pandas as pd

#Visualisation
import matplotlib.pyplot as plt
import wordcloud


class Wordcloud ():

    regions = {"Baden-Württemberg":1,
               "Bayern":2,
               "Berlin":3,
               "Brandenburg":4,
                "Bremen":5, 
                "Hamburg":6, 
                "Hessen":7, 
                "Mecklenburg-Vorpommern":8, 
                "Niedersachsen":9, 
                "Nordrhein-Westfalen":10, 
                "Rheinland-Pfalz":11, 
                "Saarland":12, 
                "Sachsen":13, 
                "Sachsen-Anhalt":14, 
                "Schleswig-Holstein":15, 
                "Thüringen":16
                }

    ressorts = [
        "ausland",
        "inland",
        "wirtschaft",
        "sport",
        "investigativ",
        "faktenfinder"
        ]
    
    df = pd.DataFrame(columns=["topline","title","firstSentence","tags"])

    def __init__(self,region,ressort):
        self.region = region
        self.ressort = ressort

    def _get_json(self):
        
        """
        gets a response from the tagesschau API and saves it to a json file
        """

        reg = list(self.regions.keys())[list(self.regions.values()).index(self.region)]
        res = self.ressorts[self.ressort]
        date = datetime.date.today()

        url = "https://www.tagesschau.de/api2/news/?regions={}&ressort={}".format(self.region,res)
        filename = "TGS-{}-{}-{}.json".format(reg,res,date)

        rep = requests.get(url)
        rep_dict = rep.json()
        with open(filename,'w') as f:
            json.dump(rep_dict,f)

    def _update_database(self):
        """
        WARNING - TAKES ~16 MINUTES TO COMPLETE

        Create full database directory for all regions on a specific day and for
        one specific ressort

        """
        date = datetime.date.today()
        dir = "TGSDATA-{}-{}".format(date,self.ressorts[self.ressort])
        parent_dir = "/home/{}/Projects/Python/TGSViewer".format(pwd.getpwuid(os.getuid())[0])
        path = os.path.join(parent_dir,dir)
        try:
            os.mkdir(path=path)
            os.chdir(path)
            for i in self.regions.values():
                reg = reg = list(self.regions.keys())[list(self.regions.values()).index(i)]
                res = self.ressorts[self.ressort]
                url = "https://www.tagesschau.de/api2/news/?regions={}&ressort={}".format(i,self.ressorts[self.ressort])
                filename = "TGS-{}-{}-{}.json".format(reg,res,date)
                rep = requests.get(url)
                rep_dict = rep.json()
                with open(filename,'w') as f:
                    json.dump(rep_dict,f)
                print("Saving response from:\n",
                    url,
                    "\t=>\t",
                    filename,
                    "\n")
                time.sleep(60)

            print("Database entry \"TGSDATA-{}-{}\" created here:\n{}".format(date,self.ressorts[self.ressort],path))
                
        except OSError as error:
            print(error)

    def _database_to_df(self,dir):
        """
        Make a pd.Dataframe from a whole directory of TGS.jsons;
        Not really necessary bc the .jsons are the same :-(
        """
        os.chdir("/home/ouroboros/Projects/Python/TGSViewer/{}".format(dir))
        for i in os.listdir("."):
            with open(i,'r') as f:
                content = json.load(f)
            for i in content["news"]:
                dt = parser.parse(i["date"])
                self.df.loc[dt] = [i["topline"],i["title"],i["firstSentence"],i["tags"]]
            print(self.df)

    def _json_to_df(self, date = datetime.date.today()):
        
        """
        turns the json to a pd.Dataframe for ease of everything. Current
        WIP for a CLI news reader too.

        date = today by default, pass "YYYY-MM-DD" string to function
        to access specific date file
        """

        reg = list(self.regions.keys())[list(self.regions.values()).index(self.region)]
        res = self.ressorts[self.ressort]
        filename = "TGS-{}-{}-{}.json".format(reg,res,date)

        with open(filename,'r') as f:
            content = json.load(f)
        
        for i in content["news"]:
            dt = parser.parse(i["date"])
            self.df.loc[dt] = [i["topline"],i["title"],i["firstSentence"],i["tags"]]
        
        indexTimeDelta = self.df.head(1).index - self.df.tail(1).index

        print(indexTimeDelta[0])

    def visualise(self):
        
        """
        Visualise news data from specific timeframe
        """

        df = self.df
        words = ""
        wordcloud.STOPWORDS = [
            "auf",
            "ab",
            "an",
            "beim"
            "der",
            "die",
            "das",
            "dem",
            "den",
            "deren",
            "dessen",
            "es",
            "eine",
            "einen",
            "ein",
            "eins",
            "zwei",
            "drei",
            "vier",
            "fünf",
            "sechs",
            "sieben",
            "acht",
            "neun",
            "zehn",
            "von",
            "gegen",
            "für",
            "zu",
            "vor",
            "nach",
            "lehnt",
            "beschließt",
            "will",
            "ist",
            "Kein",
            "in",
            "beim",
            "aus",
            "weiteren",
            "Müssen",
            "bei",
            "der",
            "Warum",
            "warum",
            "gehen",
            "weiter",
            "erneut",
            "bis",
            "wohl",
            "waren",
            "steigt",
            "Worum",
            "sieht",
            "ausgehen",
            "weist",
            "versteckte",
            "getötete",
            "erträglich",
            "keinen",
            "hohem",
            "Offenbar",
            "Mit",
            "Soll",
            "härtere",
            "könnte",
            "spielen",
            "im",
            "neue",
            "tritt",
            "zurück",
            "verhört",
            "ins",
            "langsam",
            "nicht",
            "Mehr",
            "Wie",
            "und",
            "nimmt",
            "ihre",
            "geben",
            "da",
            "unter",
            "wird",
            "Wenn",
            "Neues",
            "Tausende",
            "Kommt",
            "Was",
            "hofft",
            "rücken",
            "Alle",
            "fordert",
            "Wir",
            "identifiziert",
            "werden"
        ]
        
        stopwords = set(wordcloud.STOPWORDS)
        
        for i in df["title"]:
            i.split(" ")
            words += "".join(i)+" "

        wdc = wordcloud.WordCloud(
            width = 800,
            height=400,
            background_color='white',
            stopwords=stopwords
        ).generate(words)

        plt.figure(figsize=(8,8),facecolor=None)
        plt.imshow(wdc)
        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.show()

        

#Wordcloud(region=3,ressort=1)._get_json()
#Wordcloud(region=3,ressort=1)._json_to_df()
#Wordcloud(region=3,ressort=1)._update_database()
#Wordcloud(region=3,ressort=1)._database_to_df("TGSDATA-2024-05-06-inland")
#Wordcloud(region=3,ressort=1).visualise()

