from requests import get

class player():
    def __init__(self, id: str = None) -> None:
        if id is None:
            self.get_id()
        else:
            self.id = id


    def get_id(self) -> None:
        while True:
            id = input("What is the player's id or scoresaber's url? ").strip("https://new.scoresaber.com/u/").rsplit("&")[0].rsplit("/")[0] #"76561198410694791"
            profile = get(f"https://new.scoresaber.com/api/player/{id}/full").json()
            if 'error' in profile:
                print(f"ERROR: Invalid url/player id, got '{id}'")
                continue
            break
        self.id = id
        self.profile = profile