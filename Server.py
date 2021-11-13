from typing import Type
import urllib3
import flask
import string
import random
import time
from flask import request, jsonify

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################

#Initialise Flask
app = flask.Flask(__name__)

#Create all global variabels
global serverList #List to contain "server" instances
sessionList = [None, None, None, None, None]

########################################################################################################
#                                              - Classes -                                             #
########################################################################################################

class Session:
    def __init__(self, password, auth1):
        """
        `password` is the server password chosen by the host\n
        `internalPass` is the password generated using `CreatePass` for the host
        """
        self.externalPass = password
        self.internalPass = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        self.connectedUsers = [auth1]
        self.spotifyRoot = "https://api.spotify.com/v1"
        self.http = urllib3.PoolManager()

    def QueueSong(self, songURI):
        for user in self.connectedUsers:
            headers = {"Authorization": f"Bearer {user}"}
            self.http.request("POST", f"{self.spotifyRoot}/me/player/queue?uri={songURI.replace(':', '%3A')}", headers=headers)

    def AddUser(self, auth):
        self.connectedUsers.append(auth)
    def RemoveUser(self, auth):
        self.connectedUsers.remove(auth)

    def GetExternalPass(self):
        """
        returns the password to this session
        """
        return self.externalPass
    def GetInternalPass(self):
        """
        returns the internal password for the session
        """
        return self.internalPass

    def GetAlive(self):
        return len(self.connectedUsers) > 0
            
########################################################################################################
#                                            - Functions -                                             #
########################################################################################################

@app.route("/JoinSession/<id>/<password>/<auth>")
def JoinSession(id, password, auth):
    """
    Ran when `/JoinSession/<id>/<password>/<auth>` requested\n
    `id`, `password` and `auth` are all given by the client\n
    Used for a client to connect to a session under the specified `id`\n
    If the session doesn't exist it creates it with the provided password\n
    Returns either True or False under the `success` key and all other info needed based on whether its successful or not
    """
    try:
        if sessionList[int(id)]:
            if sessionList[int(id)].GetExternalPass() == password:
                sessionList[int(id)].AddUser(auth)
                print("Good")
                return jsonify({"success": True, "message": f"Joined session {id}", "internalPass": sessionList[int(id)].GetInternalPass()})
            else:
                print("Bad")
                return jsonify({"success": False, "message": "Incorrect Password"})
        else:
            sessionList[int(id)] = Session(password, auth)
            print("Good")
            return jsonify({"success": True, "message": f"Session {id} created with given password", "internalPass": sessionList[int(id)].GetInternalPass()})
    except IndexError or TypeError or ValueError:
        print("Bad")
        return jsonify({"success":False, "message": "WTF did you do wrong?"})

@app.route("/LeaveSession/<sessionID>/<sessionPass>/<auth>", methods=["POST"])
def LeaveSession(sessionID, sessionPass, auth):
    """
    Ran when `/LeaveSession/<sessionID>/<sessionPass>/<auth>` requested\n
    `sessionID`, `sessionPass` and `auth` are all given by the client\n
    Used for the specified `auth` to disconnect from the session under `id`\n
    """
    if sessionList[int(sessionID)]:
        if sessionList[int(sessionID)].GetInternalPass == sessionPass:
            sessionList[int(sessionID)].RemoveUser(auth)
            if not sessionList[int(sessionID)].GetAlive():
                sessionList[int(sessionID)] == None
            
            return "Disconnected"
        else:
            return "Incorrect password"
    else:
        return "Invalid Session"

@app.route("/AddSong/<sessionID>/<sessionPass>/<songURI>", methods=["POST"])
def AddSong(sessionID, sessionPass, songURI):
    """
    Ran when `/AddSong/<sessionID>/<sessionPass>/<songURI>` requested\n
    `sessionID`, `sessionPass` and `songURI` are all given in the request\n
    queues the song specified by `songURI` to session under `sessionID`\n
    returns a message on if it succeded or not
    """
    if sessionList[int(sessionID)]:
        if sessionList[int(sessionID)].GetInternalPass() == sessionPass:
            sessionList[int(sessionID)].QueueSong(songURI)
            return "Song queued successfully :)"
        else:
            return "The password is incorrect for this session"
    else:
        return "Sorry, the session isn't active"

########################################################################################################
#                                          - Call Functions -                                          #
########################################################################################################

if __name__ == "__main__":
    app.run(debug=False, port="6900", host="0.0.0.0")
