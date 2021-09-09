import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Google import Create_Service
class SpotifytoYTM:
    def __init__(self):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.scope = "playlist-modify-public"
        self.CLIENT_SECRET_FILE =  'client_secret.json'
        self.API_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        self.service = Create_Service(self.CLIENT_SECRET_FILE,self.API_NAME,self.API_VERSION,self.SCOPES)


    def playlist_all_items(self):
        all_items = self.sp.playlist_items("1VRuzt0zHCExPrC36hxfpj")
        items = all_items["items"]
        
        while all_items["next"]:
            all_items = self.sp.next(all_items)
            items.extend(all_items["items"])

        tracklist = []

        for i in range(len(items)):
            name = items[i]["track"]["artists"][0]["name"]
            song_name = items[i]["track"]["name"]
            full_song_name = name + " " + song_name
            tracklist.append(full_song_name)

        return tracklist 


    def searchYT(self,query):
        request = self.service.search().list(
            part="snippet",
            maxResults=2,
            #pageToken="nextPageToken",
            q=query,
            type="video"
        )

        response = request.execute()
        items = response["items"]
        firstItem = items[0]["id"]
        videoId = firstItem["videoId"]

        return videoId  
    

    def create_youtube_playlist(self):
        title = str(input("Title: "))
        description = str(input("Description: "))

        request = self.service.playlists().insert(
            part="snippet,status",
            body={
              "snippet": {
                "title": title,
                "description": description,
                "tags": [
                  "sample playlist",
                  "API call"
                ],
                "defaultLanguage": "en"
              },
              "status": {
                "privacyStatus": "private"
              }
            }
        )
        response = request.execute()
        playlist_id = response["id"]

        return playlist_id


    def append_to_playlist(self,videoId):
        request =  self.service.playlistItems().insert(
            part="snippet",
            #pageToken="nextPageToken",
            body={
              "snippet": {
                "playlistId": "PLLHevtJTva8fE3wU4KNN2jzAn3lSD4",
                "position": 0,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": videoId
                }
              }
            }
        )    
        response = request.execute()


    def append_all(self):
        list = self.playlist_all_items()
        while len(list) != 0:
            for song_name in list:
                self.searchYT(song_name)
                list.remove(song_name)
        


    




sptoytm = SpotifytoYTM()
sptoytm.searchYT("hello world")