import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Read tracked user IDs from environment variables
TRACKED_USERS = [
    int(os.getenv("USER_A_ID")),
    int(os.getenv("USER_B_ID")),
    int(os.getenv("USER_C_ID")),
    int(os.getenv("USER_D_ID")),
]

ANNOUNCE_CHANNEL_ID = int(os.getenv("ANNOUNCE_CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True

client = discord.Client(intents=intents)

# Track current voice channel per user (None if not connected)
user_voice_channels = {user_id: None for user_id in TRACKED_USERS}

last_announced_channel_id = None  # To avoid duplicate alerts

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    global last_announced_channel_id

    if member.id not in user_voice_channels:
        # Not tracking this user
        return

    # Update this user's voice channel info
    user_voice_channels[member.id] = after.channel

    # Build a dict: channel_id -> list of tracked users currently in that channel
    channel_to_users = {}
    for user_id, channel in user_voice_channels.items():
        if channel is not None:
            channel_to_users.setdefault(channel.id, []).append(user_id)

    # Find any channel where 2 or more tracked users are present
    alert_channel_id = None
    for channel_id, users_in_channel in channel_to_users.items():
        if len(users_in_channel) >= 2:
            alert_channel_id = channel_id
            break  # Only alert once per event for the first qualifying channel

    if alert_channel_id is not None:
        if alert_channel_id != last_announced_channel_id:
            last_announced_channel_id = alert_channel_id
            announce_channel = client.get_channel(ANNOUNCE_CHANNEL_ID)
            if announce_channel is None:
                print(f"Error: Cannot find announce channel with ID {ANNOUNCE_CHANNEL_ID}")
                return

            # Mention users in the shared channel
            user_mentions = ' and '.join(f"<@{uid}>" for uid in channel_to_users[alert_channel_id])
            channel_obj = client.get_channel(alert_channel_id)
            channel_name = channel_obj.name if channel_obj else "a voice channel"
            await announce_channel.send(f"👀 Heads up! {user_mentions} are now in the same voice channel: **{channel_name}**")
    else:
        # No 2+ users in same channel, reset alert flag
        last_announced_channel_id = None

client.run(TOKEN)
