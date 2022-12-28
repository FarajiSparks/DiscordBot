import discord
import asyncio
import youtube_dl

# Create a client object
client = discord.Client()

# A queue of audio sources
queue = asyncio.Queue()

# The current audio source being played
current_source = None

# A flag to indicate if the bot is currently playing music
is_playing = False

# A dictionary of voice clients, keyed by server id
voice_clients = {}
client = discord.Client()


# A function to download audio from a YouTube video
def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# A function to create an audio source from a file
def create_audio_source(filename):
    return discord.FFmpegPCMAudio(filename)

# A function to play the next item in the queue
async def play_next(client, voice_client):
    global current_source
    global is_playing
    if not queue.empty():
        # Get the next item in the queue
        source = await queue.get()
        # Play the audio
        current_source = source
        voice_client.play(source)
        is_playing = True
    else:
        # No more items in the queue, disconnect from the voice channel
        await voice_client.disconnect()
        is_playing = False

# An event that is called when an audio source finishes playing
@client.event
async def on_voice_source_finish(voice_client, source):
    global is_playing
    is_playing = False
    # Play the next item in the queue
    await play_next(client, voice_client)

# An event that is called when a message is received
@client.event
async def on_message(message):
    global is_playing
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith("!play"):
        # Get the voice channel the user is in
        voice_channel = message.author.voice.channel
        if voice_channel:
            # Get the server id
            server_id = message.guild.id
            # Check if the bot is already in a voice channel
            if server_id in voice_clients:
                # Get the voice client for this server
                voice_client = voice_clients[server_id]
            else:
                # Join the voice channel
                voice_client = await voice_channel.connect()
                # Add the voice client to the dictionary
                voice_clients[server_id] = voice_client
            # Get the URL of the YouTube video to play
            url = message.content[6:]
            # Download the audio from the YouTube video

       
        channel.send("You are not in a voice channel!")
