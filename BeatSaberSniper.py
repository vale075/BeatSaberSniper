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
    player_profile = requests.get(f"https://new.scoresaber.com/api/player/{player_id}/full").json()
    if 'error' in player_profile:
        print(f"ERROR: Invalid url/player id, got '{player_id}'")
        continue
    break

player_name = player_profile["playerInfo"]["playerName"]
max_play_amount = player_profile["scoreStats"]["totalPlayCount"]
print(f"The player's name is '{player_name}', he did {max_play_amount} plays.")


while True:
    sort_n = input("How do you want to sort the plays? (0: top; 1: recent) ")
    if sort_n in ["0", "1"]:
        break
    print(f"ERROR: Invalid sort, expected '0' or '1', but got '{sort_n}'")
sort_n = int(sort_n)
sort = ["top", "recent"][sort_n]


while True:
    play_amount = input("How many plays do you want to include? ")
    try:
        play_amount = int(play_amount)
        break
    except:
        print(f"ERROR: Invalid amount, expected an integer, but got '{play_amount}'")

if play_amount > max_play_amount:
    print(f"'{player_name}' didn't do that many plays, defaulted to the max amount of {max_play_amount}")
    play_amount = max_play_amount
play_remaining = play_amount


plays = []
for i in range(1, (play_amount-1)//(8)+2):
    print(f"Requesting {(i*8 if play_remaining//8 > 0 else play_amount)}/{play_amount}")
    url = f"https://new.scoresaber.com/api/player/{player_id}/scores/{sort}/{i}"
    page = requests.get(url).json()['scores']

    for y in page:
        plays.append({
            "songName": y["songName"],
            "hash": y["songHash"],
            "difficulties":[{
                    "characteristic":y["difficultyRaw"].split("_")[2].replace("Solo",""),
                    "name":y["difficultyRaw"].split("_")[1]
            }]})
        play_remaining -= 1


pl_title = f'"{player_name}" {sort} {play_amount} plays'
playlist = {
    'playlistTitle': pl_title,
    'playlistAuthor': 'BeatSaberSniper',
    'playlistDescription': f'BeatSaberSniper by vale075 - This playlist contains the {play_amount} {sort} plays of "{player_name}"',
    'songs': plays
}

file_path = path + f"{player_id} {sort} {play_amount} plays" + ".bplist"
with open(file_path, "w") as file:
    json.dump(playlist, file)

print(f"Done, your file is in {file_path}")