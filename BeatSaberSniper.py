import json
import requests
import os

def get_path():
    if os.path.exists("Playlist path.txt"):
        with open("Playlist path.txt") as file:
            p = file.read()
            if os.path.exists(p):
                return p
    
    print("You haven't specified a path for your playlist folder or the path is invalid.")
    while True:
        p = input("Where do you want the playlists to be created? ")
        if p[-1] != "\\":
            p += "\\"
        if os.path.exists(p):
            with open("Playlist path.txt", "w") as file:
                file.write(p)
            return p
        print("The path you specified is invalid or doesn't exist yet, please double check or creat the folders and try again.")


path = get_path()

while True:
    player_id = input("What is the player's id or scoresaber's url? ").strip("https://new.scoresaber.com/u/").rsplit("&")[0].rsplit("/")[0] #"76561198410694791"
    player_profile = requests.get("https://new.scoresaber.com/api/player/{}/full".format(player_id)).json()
    if 'error' in player_profile:
        print("ERROR: Invalid url/player id, but got '{}'".format(player_id))
        continue
    break
player_name = player_profile["playerInfo"]["playerName"]
max_song_amount = player_profile["scoreStats"]["totalPlayCount"]
print("The player's name is '{}', he played {} songs.".format(player_name, max_song_amount))


while True:
    sort_n = input("How do you want to sort the songs? (0: top; 1: recent) ")
    if sort_n in ["0", "1"]:
        break
    print("ERROR: Invalid sort, expected '0' or '1', but got '{}'".format(sort_n))
sort_n = int(sort_n)
sort = ["top", "recent"][sort_n]


while True:
    song_amount = input("How many songs do you want to include? ")
    try:
        song_amount = int(song_amount)
        break
    except:
        print("ERROR: Invalid amount, expected an integer, but got '{}'".format(song_amount))

if song_amount > max_song_amount:
    print("'{}' didn't played that many songs, defaulted to the max amount of {}".format(player_name, max_song_amount))
    song_amount = max_song_amount
song_remaining = song_amount


songs = []
for i in range(1, (song_amount-1)//(8)+2):
    print(f"Requesting {(i*8 if song_remaining//8 > 0 else song_amount)}/{song_amount}")
    url = "https://new.scoresaber.com/api/player/{}/scores/{}/{}".format(player_id, sort, i)
    page = requests.get(url).json()['scores']

    for i in range(8 if song_remaining//8 > 0 else song_remaining):
        songs.append({"songName": page[i]["songName"], "hash": page[i]["songHash"]})
        song_remaining -= 1


pl_title = '{} {} {} songs'.format(player_name, song_amount, sort)
playlist = {
    'playlistTitle': pl_title,
    'playlistAuthor': 'Scoresaber Scraper',
    'playlistDescription': 'Scoresaber Scraper - {} {} plays of "{}"'.format(song_amount, sort, player_name),
    'songs': songs
}

file_path = path + pl_title + ".bplist"
print(file_path)
with open(file_path, "w") as file:
    json.dump(playlist, file)

print("Done, your file is named {}.bplist".format(pl_title))