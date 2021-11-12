import urllib3
import json

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################

with open("ip.txt") as f: #Open root ip file
    serverRoot = f.read()

with open("auth.txt") as f: #Open root ip file
    auth = f.read()

spotifyRoot = "https://api.spotify.com/v1"

#Server Things
http = urllib3.PoolManager()
"""
SessionNo = input("What is the ID of the session you'd like to join? ")
password = input("What is the sessions password? ")

if SessionNo and password:
    result = http.request("GET", f"{serverRoot}/JoinSession/{SessionNo}/{password}")
else:
    print("Bad input")
    quit()

print(result.data.decode("utf-8"))
result = json.loads(result.data.decode('utf-8'))

#If succesfully joined server
if result["success"]:
    print(f"You have sucessfully joined session {SessionNo}")
else:
    print(f"Unable to join session")
"""

search = input("What would you like to search for?\n")

headers = {"Authorization": f"Bearer {auth}"}
fields = {"type": "track", "q": search}
result = http.request("GET", f"{spotifyRoot}/search", headers=headers, fields=fields)

if result.status != 200:
    print(result.status)
    print(result.data)
    
result = json.loads(result.data.decode('utf-8'))

counter = 1
for track in result["tracks"]["items"][:5]:
    print(f"{counter}:", track["name"], track["artists"][0]["name"])
    counter += 1

songNo = int(input("\nWhich song would you like? (number) \n"))
songURI = result["tracks"]["items"][songNo-1]["uri"]

headers = {"Authorization": f"Bearer {auth}"}

result = http.request("POST", f"{spotifyRoot}/me/player/queue?uri={songURI.replace(':', '%3A')}", headers=headers)

print("Song queued on spotify")
