# EVERY FRAME IN ORDER BOT FOR TWITTER
# By Pigeonburger, 2022
# https://github.com/pigeonburger

import os, re, glob, sqlite3 as db

# This is the frame-splitting part (this will probably take a while depending on how fast your computer is)

# Get all the mp4 files in the current folder (change file extension if needed)
eps = glob.glob("*.mp4")

# Number of frames per second you want the show to be split into
fps = 1

os.mkdir('frames')

# Supports common file season-episode formats e.g. S01E01, 01x01, Season 1 Episode 1 etc.
regx = re.compile(r"(?:.*)(?:s|season|)\s?(\d{1,2})\s?(?:e|x|episode|ep|\n)\s?(\d{1,2})", re.IGNORECASE)

for ep in eps:
    ep_regx = regx.match(ep)

    if ep_regx:
        # Parse to get the video's season and episode numbers
        season, episode = ep_regx.groups()

        # All videos will be stored in a folder called 'frames', inside another folder denoting the season number
        out_path = f'./frames/S{season.zfill(2)}'
        if not os.path.isdir(out_path):
            os.mkdir(out_path)

        # The outputted frame files will look like 00x00.jpg, where the number on the left side of the x is the episode number, and the number on the right side is the frame number.
        # Also scale down to 360p to save server space (and Twitter compresses the hell out of uploaded media anyway so no point having HD)
        os.system(f'ffmpeg -i "{ep}" -vf "fps={fps},scale=640:360" {out_path}/{episode}x%d.jpg')


# This half of the script will create the required (SQLite) database entries.

connection = db.connect("framebot.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE show (ep, frames)")
cursor.execute("CREATE TABLE bot (current_episode, last_frame)")
cursor.execute("INSERT INTO bot(current_episode, last_frame) VALUES (\"01x01\", 0)")
connection.commit()

total_seasons = int(season)

# Store the number of frames per episode in a database so that it can be retrieved faster (rather than counting this every time the bot is run)
for n in range(total_seasons):
    current_season = str(n+1).zfill(2)
    
    total_eps = len(glob.glob(f"./frames/S{current_season}/*x1.jpg"))

    for i in range(total_eps):
        current_ep = str(i + 1).zfill(2)
        frames = glob.glob(f"./frames/S{current_season}/{current_ep}x*.jpg")
        cursor.execute(f"INSERT INTO show (ep, frames) VALUES (\"{current_season}x{current_ep}\", {len(frames)})")
        
connection.commit()

# Congratulations! You're now almost ready to put the bot online!