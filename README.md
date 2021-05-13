# BeatSaberSniper

Creates a playlist based on someone's Scoresaber recent or top played songs.
You can choose the number of songs you want in the playlist and the songs will be ordered accordingly.
It will also highlight the difficulty that was played by the player and will create a custom icon based on the player's avatar.

## Downloading songs
This tool does not download the songs, you can use the plugin playlist manager to do so: https://github.com/rithik-b/PlaylistManager

## Playlist path
The first time you use the script it will ask you for a path that is then stored in `Playlist path.txt`. You can put any valid path, but it is recommended to use the Beat Saber playlist folder :

### Steam
The default path is
`C:\Program Files (x86)\Steam\steamapps\common\Beat Saber\Playlists\`

If you have your games installed on a different drive, it might be
`F:\SteamLibrary\steamapps\common\Beat Saber\Playlists\`

### Oculus
`C:\Program Files\Oculus\Software\Software\hyperbolic-magnetism-beat-saber\Playlists\`

# Features to be added
* Make it a more general playlist maker (top-ranked songs, recently ranked songs, top played, downloads, latest, etc...)
* Add the ability to update all already made playlists, so if your ~~worst enemy~~ opponent just made a new high score, you can quickly ~~demolish him~~ catch up to him (and also update the more general playlists when implemented)
* Automatically detect Beat Saber directory
