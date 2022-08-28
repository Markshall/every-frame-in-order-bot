# Every Frame In Order Bot

*A Python script allowing you to run your own Twitter bot that posts every frame of a TV show.*

I run a bot using this code on the Twitter account [@breaking_frames](https://twitter.com/breaking_frames), which posts 5 frames from the show "Breaking Bad" every half hour. That account is a good demonstration of what this program does.

I've also created a setup script (`setupbot.py`) which will automatically split the show into the frames and create the database necessary for storing info for the bot, so that setting it up is a little faster.

If you make an account running this bot, crediting [@pigeonburger](https://twitter.com/pigeonburger) somewhere in the bio/pinned tweet would be cool!

# Requirements

- A cool TV show
- Python version >=3.6
- `tweepy` (install using `pip install -U tweepy`) 
- A Twitter account with the twitter API consumer key + secret, and access token + secret (with Write permissions).
- [`FFmpeg`](https://ffmpeg.org) (only for initial setup - splitting the show into frames)

# Setup

1. First, you need a TV series downloaded onto your computer (e.g. as `.mp4` files). Put *every single episode from every season* all in one single folder all together. 

    If the video files you have are not in the `mp4` format, change line 10 of `setupbot.py` to the relevant extension (e.g. `*.mkv`)

2. Download the `setupbot.py` and `bot.py` files from here, and place them in the same folder as all the TV show episodes.

3. Run the `setupbot.py` file. This program will split all the videos into their individual frames (default `1fps`), placing them all inside a folder called `frames`, and enter some details into a database file called `framebot.db`, which is required for the Twitter bot to run. 

    Video processing is very CPU-intensive, so depending on the speed of your computer, this script may take a while to complete. Once it finally does finish running, you can delete the video files if you want.

4. Open the `bot.py` file for editing, and enter in your Twitter account's Consumer Key, Consumer Secret, Access Token, and Access Token Secret. Also enter the name of the show by updating the `show_name` variable a bit further below.

5. The bot is now ready to run! You'll need to use a program like `Cron` on Linux or `Task Scheduler` on Windows to execute `bot.py` every however many minutes you want. By default, the bot will post 5 frames from the show every time the script is run.

# License
This code is released under the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) license. 