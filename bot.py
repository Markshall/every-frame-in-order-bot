# EVERY FRAME IN ORDER BOT FOR TWITTER
# By Pigeonburger, 2022
# https://github.com/pigeonburger

import tweepy, sqlite3 as db, os

# Put your Twitter API keys and stuff here
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, 
    CONSUMER_SECRET, 
    ACCESS_TOKEN, 
    ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# Connect to the SQLite database that was created in setupbot.py
connection = db.connect("framebot.db")
cursor = connection.cursor()

# Enter the name of the show you're posting frames for here:
show_name = ""

# Put the number of frames the bot should post each time this script is run here.
iters = 5

while iters > 0:
    # Get the current season & episode the bot is currently on.
    current_ep = cursor.execute("SELECT current_episode FROM bot").fetchone()[0]
    
    # Get season and episode number
    ep_season, ep_num = current_ep.split('x')

    # Get the total frames from that episode.
    total_frames = cursor.execute(f"SELECT frames FROM show WHERE ep = \"{current_ep}\"").fetchone()[0]

    # Get the number of the last frame that was uploaded, then add one to that number to get the number of the next frame to post.
    next_frame = cursor.execute("SELECT last_frame FROM bot").fetchone()[0] + 1

    # If the next_frame number is bigger than the number of total frames in the episode, then the current_episode db value needs to be updated.
    if next_frame > total_frames:
        next_ep = str(int(ep_num)+1).zfill(2)

        # If another episode in the same season is found, update the database to reflect that.
        if os.path.isfile(f"./frames/S{ep_season}/{next_ep}x1.jpg"):
            cursor.execute(f'UPDATE bot SET current_episode = "{ep_season}x{next_ep}"')
            cursor.execute(f'UPDATE bot SET last_frame = 0')
            connection.commit()
            continue # var iters does not change, loop again
            
        # Otherwise, we need to go to a new season.
        
        else:
            next_season = str(int(ep_season) + 1).zfill(2)

            cursor.execute(f'UPDATE bot SET current_episode = "{next_season}x01"')
            cursor.execute(f'UPDATE bot SET last_frame = 0')
            connection.commit()
            continue # var iters does not change, loop again

        # Need to add a check here to see if the entire series is finished or not....

    # Get the file path for the next frame to upload.
    frame_path = f"./frames/S{ep_season}/{ep_num}x{next_frame}.jpg"

    # The message to attach to the tweet
    msg = f"{show_name} - Season {ep_season} Episode {ep_num} - Frame {next_frame} of {total_frames}"

    # Send the Tweet
    api.update_status_with_media(msg, frame_path)

    # Update the database to reflect the most recently uploaded frame.
    cursor.execute(f"UPDATE bot SET last_frame = {next_frame}")
    connection.commit()

    # That's one complete loop of the total number to upload finished.
    iters -= 1
    
# Automatically exit the script when finished.
