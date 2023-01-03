import discord
import asyncio
import youtube_dl

# Create a client object
client = discord.Client()

# A queue of songs to play
song_queue = []

# A flag to indicate if a song is currently playing
is_playing = False

# A flag to indicate if the bot is currently in a voice channel
is_connected = False

# The voice client object
voice_client = None

# The current song object
current_song = None

# The volume of the bot (1.0 is default)
volume = 1.0

# A dictionary of commands and their corresponding functions
commands = {
    "!play": play,
    "!stop": stop,
    "!skip": skip,
    "!queue": queue,
    "!volume": set_volume,
}

# The play function plays a song or adds it to the queue if a song is already playing
async def play(message, song_url):
    global is_playing, song_queue, current_song
    # If a song is currently playing, add the new song to the queue
    if is_playing:
        song_queue.append(song_url)
        await message.channel.send(f"{song_url} added to the queue")
    # If no song is currently playing, start playing the new song
    else:
        # Set the current song and start playing
        current_song = await YTDLSource.from_url(song_url, loop=client.loop)
        voice_client.play(current_song, after=song_ended)
        is_playing = True
        await message.channel.send(f"Now playing: {song_url}")

# The stop function stops the current song and clears the queue
async def stop(message):
    global is_playing, song_queue, current_song
    # Stop the current song and clear the queue
    current_song.cleanup()
    song_queue.clear()
    is_playing = False
    await message.channel.send("Music stopped.")

# The skip function skips the current song and starts the next one in the queue
async def skip(message):
    global is_playing, song_queue, current_song
    # Stop the current song and start the next one in the queue
    current_song.cleanup()
    try:
        current_song = song_queue.pop(0)
        voice_client.play(current_song, after=song_ended)
        is_playing = True
        await message.channel.send("Song skipped.")
    except IndexError:
        # If the queue is empty, stop playing and reset the flag
        is_playing = False
        await message.channel.send("Queue is empty.")

# The queue function shows the current queue of songs
async def queue(message):
    global song_queue
    # If the queue is empty, send a message
    if not song_queue:
        await message.channel.send("Queue is empty")
    
# A class that represents a YouTube video
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        # Use youtube-dl to get info about the video
        data = await loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL().extract_info(url, download=not stream))
        if "entries" in data:
            data = data["entries"][0]
        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# A function to be called when the song ends
def song_ended(error):
    global is_playing
    if error:
        print(f"An error occurred: {error}")
    is_playing = False

# The on_message event handler
@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    # Split the message into a command and its arguments
    args = message.content.split()
    command = args[0].lower()
    # Check if the command is in the commands dictionary and call the corresponding function
    if command in commands:
        await commands[command](message, *args[1:])

# Run the bot
client.run("MTA1OTA5MTkxMzUxMDIyMzkwMg.GoUReR.H3po8uodbgPZyKC-Lcd6e9xbKuKYmaujGVfvPk")
