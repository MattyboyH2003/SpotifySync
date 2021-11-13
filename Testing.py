import urllib3
import json

with open("ip.txt") as f: #Open serverRoot ip file
    serverRoot = f.read()

http = urllib3.PoolManager()

#Ask user for session id and password
sessionNo = input("What is the ID of the session you'd like to join? ")
password = input("What is the sessions password? ")

headers = {"sessionID":sessionNo, "sessionPass":password}
result = http.request("POST", f"{serverRoot}/SkipSong?sessionID={sessionNo}&sessionPass={password}")
print(result.data)
