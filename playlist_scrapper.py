from functions import fetch_playlit, check_link

print("Spotify link:")
spotify_link = input()

check = check_link(spotify_link)

if check: 
  fetch_playlit(spotify_link)
else:
  print("🕵 Vérifiez le lien donné")
