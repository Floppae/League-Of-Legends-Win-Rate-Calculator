import tkinter
#Several methods and functions to get certain information from your UI
import customtkinter
#Nicer UI
#Specific callback function you can use on the downloader
import requests
import time

#ERRORS: AGE RESTRICTION ERROR
#   SOLUTION: CHANGE INNERTUBE CLASS LINE 223 CLIENT TO ANDROID_CREATOR INSTEAD OF ANDROID_MUSIC
#   Apparently Android_music and other clients resulted in being no streamingData in vid_info and ended up throwing an AgeRestrictedError
#   Location: PyTube - Main - InnerTube

#System Settings
customtkinter.set_appearance_mode("System")
#Dark Mode or Light Mode
customtkinter.set_default_color_theme("blue")

#Define app frame
window = customtkinter.CTk()
window.geometry("720x480")
window.title("League of Legends Win Rate Calculator")

#UI Elements
title = customtkinter.CTkLabel(window, text = "Fill Out the Information Below")
title.pack(padx = 10, pady = 10)

#Name Input
name_label = customtkinter.CTkLabel(window, text = "Summoner Name:")
name_label.pack()
name = tkinter.StringVar()
nameBox = customtkinter.CTkEntry(window, width = 350, 
                              height = 40, 
                              textvariable = name)
nameBox.pack()

#Region Input
region_label = customtkinter.CTkLabel(window, text = "Region:")
region_label.pack()
region = tkinter.StringVar()
regionBox = customtkinter.CTkEntry(window, width = 350, 
                              height = 40, 
                              textvariable = region)
regionBox.pack()

#API Key input
API_label = customtkinter.CTkLabel(window, text = "API Key:")
API_label.pack()
api = tkinter.StringVar()
apiBox = customtkinter.CTkEntry(window, width = 350, 
                              height = 40, 
                              textvariable = api)
apiBox.pack()

#Count input
count_label = customtkinter.CTkLabel(window, text = "Number Of Games:")
count_label.pack()
count = tkinter.StringVar()
countBox = customtkinter.CTkEntry(window, width = 350, 
                              height = 40, 
                              textvariable = count)
countBox.pack()



#Finished Processing
finishLabel = customtkinter.CTkLabel(window, 
                                     text="")
finishLabel.pack()




def begin():
    try:
        def get_matches(region, puuid, count,api_key):
            api_url = "https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids" + "?type=ranked&" + "start=0&" + "count=" + str(count) +"&api_key=" + api_key
            resp = requests.get(api_url)
            return resp.json()

        region = regionBox.get()
        puuid_region = ""
        if region == "americas":
            puuid_region = "na1"
        
        #need to add bunch of elifs for different regions
            
        name = nameBox.get()
        api_key = apiBox.get()

        def get_puuid(region, name, api_key):
            api_url = "https://"+region+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name
            api_url = api_url+"?api_key="+api_key
            resp = requests.get(api_url)
            info = resp.json()
            return(info['puuid'])

        puuid = get_puuid(puuid_region,name,api_key)
        count = countBox.get()

        matches = get_matches(region, puuid, count, api_key)

        def getMatchData(region,match_id,api_key):
            api_url = "https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key

            while True:
                resp = requests.get(api_url)
                if resp.status_code == 429:
                    print("zzzzzzzz mimimmimimi retrieval limit exceeded... proceeding in 10 seconds")
                    time.sleep(10)
                    continue
                data = resp.json()
                #print(data)
                return data
            
        def did_win(puuid,match_data):
            participant_index = match_data['metadata']['participants'].index(puuid)
            win = match_data['info']['participants'][participant_index]['win']
            #print(win)
            return win

        game_no = 1
        wins = 0
        losses = 0

        for match_id in matches:
            print(str(game_no) + " Games Processed")
            print(match_id)
            match_data = getMatchData(region,match_id,api_key)
            print(did_win(puuid,match_data))
            if did_win(puuid,match_data) == True:
                wins += 1
            else:
                losses += 1
            print("")
            game_no += 1
        count = float(count)
        winRate = (wins/count)*100
        print("Your win rate for the last "+ str(count) + " games is: " + (str(winRate)) + "%")
        title.configure(text = name, text_color = "white")
        finishLabel.configure(text = "Win Rate: "+(str(winRate))+ "%")

    except Exception as e:
        finishLabel.configure(text = "Processing Failed...Check Fields", text_color = "red")

#Download Button
process = customtkinter.CTkButton(window, 
                                   text = "Process", 
                                   command = begin)
process.pack(padx = 10, pady = 10)

#Run app
window.mainloop()