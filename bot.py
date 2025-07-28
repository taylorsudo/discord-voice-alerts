import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
USER_A_ID = int(os.getenv("USER_A_ID"))
USER_B_ID = int(os.getenv("USER_B_ID"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("ANNOUNCE_CHANNEL_ID"))

# Set up intents: members and voice_states are required to track voice channels
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)

# Dictionary to keep track of voice channels per user
user_voice_channels = {
    USER_A_ID: None,
    USER_B_ID: None,
}

# Flag to prevent repeated alerts while users stay in the same VC
has_announced = False

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    global has_announced

    # We only care about our two tracked users
    if member.id not in user_voice_channels:
        # Uncomment below to debug other users
        # print(f"Ignoring user {member.name} ({member.id})")
        return

    # Update the voice channel of the user
    user_voice_channels[member.id] = after.channel

    print(f"[DEBUG] {member.name} changed voice channel: {before.channel} -> {after.channel}")

    a_channel = user_voice_channels[USER_A_ID]
    b_channel = user_voice_channels[USER_B_ID]

    print(f"[DEBUG] User A channel: {a_channel}")
    print(f"[DEBUG] User B channel: {b_channel}")

    # Check if both users are in the same non-empty voice channel
    if a_channel is not None and a_channel == b_channel:
        if not has_announced:
            has_announced = True
            channel = client.get_channel(ANNOUNCE_CHANNEL_ID)
            if channel:
                await channel.send(
                    f"👀 Heads up! <@{USER_A_ID}> and <@{USER_B_ID}> are now in the same voice channel: **{a_channel.name}**"
                )
                print("[DEBUG] Alert sent!")
            else:
                print(f"[ERROR] Could not find announce channel with ID {ANNOUNCE_CHANNEL_ID}")
        else:
            print("[DEBUG] Alert already sent, skipping duplicate.")
    else:
        if has_announced:
            print("[DEBUG] Users separated or left voice channels, resetting alert flag.")
        has_announced = False

if __name__ == "__main__":
    client.run(TOKEN)
