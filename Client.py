import urllib3
import json

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################

with open("ip.txt") as f: #Open serverRoot ip file
    serverRoot = f.read()

with open("auth.txt") as f: #Open auth token file
    auth = f.read()

spotifyRoot = "https://api.spotify.com/v1"

#Server Things
http = urllib3.PoolManager()

#Ask user for session id and password
sessionNo = input("What is the ID of the session you'd like to join? ")
password = input("What is the sessions password? ")

#if provided
if sessionNo and password:
    result = http.request("GET", f"{serverRoot}/JoinSession/{sessionNo}/{password}/{auth}")
else:
    print("Bad input")
    quit()

result = json.loads(result.data.decode('utf-8'))
print(result)

#If succesfully joined server
if result["success"]:
    print(f"You have sucessfully joined session {sessionNo}")
    internalPass = result["internalPass"]
else:
    print(f"Unable to join session")
    quit()

while True:
    counter = 1
    search = input("What would you like to search for?\n")

    headers = {"Authorization": f"Bearer {auth}"}
    fields = {"type": "track", "q": search}
    result = http.request("GET", f"{spotifyRoot}/search", headers=headers, fields=fields)

    if result.status != 200:
        print(result.status)
        print(result.data)
        
    result = json.loads(result.data.decode('utf-8'))

    for track in result["tracks"]["items"][:5]:
        print(f"{counter}:", track["name"], track["artists"][0]["name"])
        counter += 1

    songNo = int(input("\nWhich song would you like? (number) \n"))
    songURI = result["tracks"]["items"][songNo-1]["uri"]

    result = http.request("POST", f"{serverRoot}/AddSong/{sessionNo}/{internalPass}/{songURI}")

    print(result.data)


"""
https://accounts.spotify.com/authorize?response_type=token&client_id=96cfd701a29e4e768dbfac8a9fe8d618&scope=app-remote-control&redirect_uri=https://www.google.com/&show_dialog=true
"""