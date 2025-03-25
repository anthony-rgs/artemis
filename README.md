# Artemis

<br>

## 1. Description

Named after Artemis, the goddess of the hunt, this scraper is designed to track down and collect music data from **Spotify, Apple Music, and Deezer** with precision.

Artemis retrieves information from any **playlist or album** on these platforms. The extracted data is saved in a **JSON** file with the following structure:

```json
{
  "type": "album",
  "name": "favourite-worst-nightmare",
  "length": 12,
  "link": "https://music.apple.com/fr/album/favourite-worst-nightmare/251126923",
  "tracks": [
    {
      "track_name": "Brianstorm",
      "artists": ["Arctic Monkeys"],
      "album": "Favourite Worst Nightmare",
      "album_link": "https://music.apple.com/fr/album/favourite-worst-nightmare/251126923",
      "track_link": "https://music.apple.com/fr/song/brianstorm/251126924"
    },
    {
      "track_name": "Teddy Picker",
      "artists": ["Arctic Monkeys"],
      "album": "Favourite Worst Nightmare",
      "album_link": "https://music.apple.com/fr/album/favourite-worst-nightmare/251126923",
      "track_link": "https://music.apple.com/fr/song/teddy-picker/251126938"
    },
    "..."
  ]
}
```

### How It Works

- The script **automatically scrolls** within the track container to load all data (useful for platforms that load dynamically on scroll).
- It **fetches information** while scrolling.
- A **verification function** ensures that all data is collected and that there are **no duplicates**.

### Main Features

- Extracts data from **Spotify, Apple Music, and Deezer**.
- Saves data in **JSON** (or option to disable saving).
- Logging system to show progress, success messages, and errors.
- Error management with an **auto-retry function** in case of failures.
- Option to **enable/disable log saving**.

<br>

## 2. Project Dependencies

- **selenium==4.10.0** → Browser automation
- **webdriver-manager==4.0.1** → Automatic driver management for Selenium

<br>

## 3. Installation

Run the following command to install all dependencies:

```sh
pip install -r requirements.txt
```

<br>

## 4. Running a File

To execute the script in module mode, use the following command:

```sh
python3 -m folder.file_name
```

<br>

## 5. Available Scripts

### - `dynamic_scraper.py`

This script waits for a **URL** input, and if valid, retrieves the corresponding data (playlist or album) and stores it.

### - `checks_url.py`

This script tests the **three types of URLs** possible for each platform (**Spotify, Apple Music, Deezer**) to ensure everything works correctly:

- **Playlist**
- **Album**
- **Album with multiple discs**

### - `billion_club.py` (Bonus)

Spotify has a playlist containing all tracks with **over 1 billion streams**. This script retrieves all tracks and then accesses each track page to extract the **exact play count** as well as additional track details such as album information, track image, and embed links.

The generated JSON file looks like this:

```json
{
  "type": "playlist",
  "name": "billions-club",
  "length": 901,
  "link": "https://open.spotify.com/playlist/37i9dQZF1DX7iB3RCnBnN4",
  "tracks": [
    {
      "track_name": "505",
      "artists": ["Arctic Monkeys"],
      "album": "Favourite Worst Nightmare (Standard Version)",
      "album_link": "https://open.spotify.com/album/6rsQnwaoJHxXJRCDBPkBRw",
      "track_link": "https://open.spotify.com/track/58ge6dfP91o9oXMzq3XkIS",
      "play_count": 2113222338,
      "track_img": "https://i.scdn.co/image/ab67616d00001e020c8ac83035e9588e8ad34b90",
      "track_embed": "https://open.spotify.com/embed/track/58ge6dfP91o9oXMzq3XkIS?theme=0",
      "track_iframe": "<iframe style='border-radius:12px' src='https://open.spotify.com/embed/track/58ge6dfP91o9oXMzq3XkIS?theme=0' width='100%' height='152' frameBorder='0' allowfullscreen='' allow='autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture' loading='lazy'></iframe>",
      "album_embed": "https://open.spotify.com/embed/album/6rsQnwaoJHxXJRCDBPkBRw?theme=0",
      "album_iframe": "<iframe style='border-radius:12px' src='https://open.spotify.com/embed/track/58ge6dfP91o9oXMzq3XkIS?theme=0' width='100%' height='152' frameBorder='0' allowfullscreen='' allow='autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture' loading='lazy'></iframe>"
    },
    "..."
  ]
}
```
