import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up a client_id and client_secret
# Not secure but since you can get your own client_id and client_secret for free I do not think anyone will "steal" it.
client_id = 'd148768cc9cd4b96af6cc68c20cd2a45'
client_secret = 'a4981a3376d3475a98900869897fff58'

# Request user input for the usernames of people whom want to compare playlists.
# Username for person 1

try:
    username1 = input('Enter the username: ')
except IOError:
    print('Error with username one.')

# Username for person 2
try:
    username2 = input('Enter the second username: ')
except IOError:
    print('Error with username two.')

#username1 = ''
#username2 = ''


# Authenticate with the Spotify API
credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

'''
# Step 4: Search for a playlist
query = 'throwbacks'
results = sp.search(query, type='playlist')
playlists = results['playlists']['items']

for playlist in playlists:
    playlist_name = playlist[0]
    playlist_id = playlist[0]
    print(playlist_name, playlist_id)
'''


# Access and print playlist details
playlists = sp.user_playlists(username1)
playlists2 = sp.user_playlists(username2)


# function for getting the int input from the user for the playlist number
def userinput():
    while True:
        try:
            playlistnum = int(input("Enter the playlist number you want to compare: "))
            break  # Exit the loop if the input is successfully converted to an integer
        except ValueError:
            print("Invalid input. Please enter just the number.")

    return playlistnum


def playlistOutput(playlists):
    user = []
    for i, playlist in enumerate(playlists['items'], start=1):
        if not playlist['public']:
            continue  # Skip if playlist is not public
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        user.append(playlist_id)
        print(f"{i}. {playlist_name} ({playlist_id})")
    return user
              
def playlistSelection(playlist):
    playlistNum = userinput()
    while True:
        if 0 < int(playlistNum) <= len(playlist):
            break
        print('The playlist number you selected is not in range.')
    return playlistNum

def getPlaylist(id):
    playlist = sp.playlist(id)
    return playlist

def printSongs(playlist,print=True):
    songs = []
    for track in playlist['tracks']['items']:
        song_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        songs.append(song_name)
        if print:
            print(song_name, 'by', artist_name)
    return songs

# user 1
user1 = playlistOutput(playlists)
playlistNum = playlistSelection(playlists)

# user 2 
user2 = playlistOutput(playlists2)
playlistNum2 = playlistSelection(playlists2)




# Define the playlist ID
# Inputs from user will be 1 - x but array is 0 - x-1
playlist_id = user1[int(playlistNum)-1]
playlist_id2 = user2[int(playlistNum2)-1]

# Step 7: Retrieve the playlist by its ID
playlist = getPlaylist(playlist_id)
playlist2 = getPlaylist(playlist_id2)

user1Songs = printSongs(playlist, False)

user2songs = printSongs(playlist2, False)


set1 = set(user1Songs)
matches = [str2 for str2 in user2songs if str2 in set1]
if len(matches) > 0:
    print(matches)
else:
    print('No tracks in common.')