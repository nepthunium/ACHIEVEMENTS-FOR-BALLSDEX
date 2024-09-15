import logging
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, button
from tortoise.exceptions import DoesNotExist
from tortoise.functions import Count

from ballsdex.core.models import (
    Ball,
    BallInstance,
    Achievement,
    Player,
    AchievementInstance,
    achievements
)
from ballsdex.core.utils.paginator import FieldPageSource, Pages
from ballsdex.settings import settings

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

async def check_if_achieved(player_id: int, achievement) -> bool:
    a = await Achievement.get(name=achievement)
    filters = {"player__discord_id": player_id, "achievement": a}
    a1 = await AchievementInstance.filter(**filters)
    if a1:
        return True
    return False

log = logging.getLogger("ballsdex.packages.countryballs")

DEFAULT_AVATAR_URL = 'https://archive.org/download/discordprofilepictures/discordblue.png'

class Achievements(commands.GroupCog, group_name="achievements"):
    """
    View and manage your achievements.
    """

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    @app_commands.command()
    async def list(self, interaction: discord.Interaction):
        """
        Displays the list of achievements in the bot (and if you have achieved them or not)
        """
        achievements = await Achievement.all()
        bot_achievements = [a for a in achievements if a.achievable]

        entries = []
        for a in bot_achievements:
            result = await check_if_achieved(interaction.user.id, a.name)
            if result == True:
                owned = "👑 Achieved! 👑"
            else:
                owned = "⏳ Not achieved yet. ⏳"

            # Check if simplified_req exists and is not empty
            if a.simplified_req:
                requirements = f"- {a.simplified_req}"  # Use the simplified requirement
            else:
                # Fall back to the detailed requirements if no simplified_req exists
                requirements = str(a.requirements).split(';')
                requirements = '\n'.join(f"- {req.strip()}" for req in requirements)
            
            entries.append((f"**{a.name} ({owned}):**", f"Requirements:\n{requirements}"))
        
        if len(entries) == 0:
            await interaction.response.send_message("There are no achievements registered on this bot.", ephemeral=True)
            return
        
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else DEFAULT_AVATAR_URL
        
        source = FieldPageSource(entries, per_page=1, inline=False, clear_description=False)
        source.embed.description = "**List of Achievements**"
        source.embed.colour = discord.Colour.blurple()
        source.embed.set_thumbnail(url=avatar_url)
        pages = Pages(source=source, interaction=interaction, compact=True)
        await pages.start()

    @app_commands.command()
    async def check(self, interaction: discord.Interaction):
        """
        Check for any missing achievements you should have.
        """
        filters = {"player__discord_id": interaction.user.id}
        bot_achievements = await Achievement.all()
        message = []
        await interaction.response.send_message("Checking for achievements...", ephemeral=True)
        for a in bot_achievements:
            requirements = str(a.requirements).split(";")
            filters = {"player__discord_id": interaction.user.id, "ball__country__in": requirements}

            balls = await BallInstance.filter(**filters)

            def shiny_or_special(ball):
                if ball.shiny and ball.special:
                    ball = str(ball).split(' ', 3)[3]
                elif ball.shiny or ball.special:
                    ball = str(ball).split(' ', 2)[2]
                else:
                    ball = str(ball).split(' ', 1)[1]
                return ball

            balls = [shiny_or_special(ball) for ball in balls]

            if all(ball in balls for ball in requirements):
                player = await Player.get(discord_id=interaction.user.id)
                has_a = await check_if_achieved(interaction.user.id, a.name)

                if has_a == False:
                    rewards = str(a.rewards).split(";")

                    if rewards:
                        for r in rewards:
                            if r.startswith("✨ "):
                                split_r = r[2:].split()
                                if len(split_r) > 0:
                                    reward = split_r[0]
                                    shiny = True
                                else:
                                    continue
                            else:
                                split_r = r.split()
                                if len(split_r) > 0:
                                    reward = split_r[0]
                                    shiny = False
                                else:
                                    continue
                            try:
                                b = await Ball.get(country=reward)
                                await BallInstance.create(ball=b, player=player, shiny=shiny)
                            except DoesNotExist:
                                continue

                    await AchievementInstance.create(achievement=a, player=player)
                    message.append(f"Found and gave missing achievement: **{a.name}**\n")
        
        if message:
            await interaction.followup.send("\n".join(message), ephemeral=True)
        else:
            await interaction.followup.send("No new achievements found.", ephemeral=True)