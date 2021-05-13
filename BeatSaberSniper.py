from requests import get
from os import path
from json import dump
from PIL import Image
from io import BytesIO
from base64 import b64encode, b64decode
from time import strftime, gmtime
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askdirectory
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)
Tk().withdraw()

class player():
    def __init__(self, id: str = None) -> None:
        if id is None:
            self.get_id()
        else:
            self.id = id
            self.get_profile()
        
        self.name = self.profile["playerInfo"]["playerName"]
        self.play_amount = self.profile["scoreStats"]["totalPlayCount"]
        self.play_rank = self.profile["scoreStats"]["rankedPlayCount"]


    def get_id(self) -> None:
        while True:
            id = input("What is the player's id or scoresaber's url? ")
            if id == "teste":
                id = "76561198141584046"
            else:
                id = id.strip("https://new.scoresaber.com/u/").rsplit("&")[0].rsplit("/")[0]

            try:
                self.get_profile(id)
                break
            except:
                print(f"ERROR: Invalid url/player id, got '{id}'")

        self.id = id
    
    def get_profile(self, id: str = None) -> None:
        profile = get(f"https://new.scoresaber.com/api/player/{self.id if id is None else id}/full").json()
        if 'error' in profile:
            raise Exception()
        else:
            self.profile = profile
    
    def get_plays(self, amount: int, sort: str) -> list:
        remaining = amount
        plays = []
        for i in range(1, (amount-1)//(8)+2):
            print(f"Requesting {(i*8 if remaining//8 > 0 else play_amount)}/{play_amount}")
            page = get(f"https://new.scoresaber.com/api/player/{self.id}/scores/{sort}/{i}").json()['scores']
            for y in page:
                plays.append(play(
                    y["songHash"],
                    y["difficultyRaw"].split("_")[1],
                    y["difficultyRaw"].split("_")[2].replace("Solo","")
                    ))
                remaining -= 1
        
        return plays
    
    def get_avatar(self):
        return get(f"https://new.scoresaber.com{ self.profile['playerInfo']['avatar'] }").content


class play():
    def __init__(self, hash: str, difficulty: str = None, characteristic: str = None) -> None:
        self.hash = hash
        self.difficulty = difficulty
        self.characteristic = characteristic


class playlist():
    def __init__(self, songs: list = [], name: str = None, author: str = None, description: str = None, image: str = None, customData: dict = None) -> None:
        self.songs = songs
        self.name = name
        self.author = author
        self.description = description
        self.image = image
        self.customData = customData
    
    def export(self) -> dict:
        return {
            'playlistTitle': self.name,
            'playlistAuthor': self.author,
            'playlistDescription': self.description,
            'image': self.image,
            'customData': self.customData,
            'songs': [{
                'hash': i.hash,
                'difficulties': [{
                    'characteristic': i.characteristic,
                    'name': i.difficulty
                }]
            } for i in self.songs]
        }


def get_path() -> str:
    if path.exists("Playlist path.txt"):
        with open("Playlist path.txt") as file:
            p = file.read()
            if path.exists(p):
                return p
    
    while True:
        print("You haven't specified a path for your playlist folder or the path is invalid.")
        input("You will now be asked to choose where to create the playlist files. (press enter to continue)")
        p = askdirectory() + "/"
        if path.exists(p):
            with open("Playlist path.txt", "w") as file:
                file.write(p)
            return p

def sniper_image(player: player) -> str:
    avatar = Image.open(BytesIO(player.get_avatar()))
    avatar.putalpha(255)
    new_img = Image.alpha_composite(avatar, Image.open(BytesIO(b64decode("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"))))
    buffer = BytesIO()
    new_img.convert("RGB").save(buffer, format="JPEG")
    return "data:image/jpg;base64," + b64encode(buffer.getvalue()).decode()


if __name__ == '__main__':
    p = player()
    print(f"The player's name is '{p.name}', he did {p.play_amount} plays.")

    while True:
        sort = input("How do you want to sort the plays? (0: top; 1: recent) ")
        if sort in ['0', '1']:
            break
        print(f"ERROR: Invalid sort, expected '0' or '1', but got '{sort}'")
    sort = ('top', 'recent')[int(sort)]

    while True:
        play_amount = input("How many plays do you want to include? ")
        try:
            play_amount = int(play_amount)
            break
        except:
            print(f"ERROR: Invalid amount, expected an integer, but got '{play_amount}'")
    if play_amount > p.play_amount:
        print(f"\"{p.name}\" didn't do that many plays, defaulted to the max amount of {p.play_amount}")
        play_amount = p.play_amount

    pl = playlist(
        p.get_plays(play_amount, sort),
        f"\"{p.name}\" {sort} {play_amount} plays",
        "BeatSaberSniper",
        f"This playlist contains the {play_amount} {sort} plays of \"{p.name}\" - BeatSaberSniper by vale075",
        sniper_image(p),
        {'BSSniperData': {
            'DateCreated': strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
            'DateUpdated': strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()),
            'SongAmount': play_amount,
            'Type': 'Sniper',
            'SniperSort': sort,
            'SniperId': p.id,
            'SniperPlays': p.play_amount,
            'SniperRankedPlays': p.play_rank
        }}
        )
    
    file_path = get_path() + f"{p.id} {sort} {play_amount} plays" + ".bplist"
    with open(file_path, 'w') as file:
        dump(pl.export(), file)

    input(f"\nDone!\nYour file is in {file_path}\n(press enter to continue)")

