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
from ballsdex.core.utils.achievements import check_if_achieved
from ballsdex.core.utils.paginator import FieldPageSource, Pages
from ballsdex.settings import settings

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.countryballs")

DEFAULT_AVATAR_URL = 'https://archive.org/download/discordprofilepictures/discordblue.png'

class Achievements(commands.GroupCog, group_name="achievements"):
    """
    View and manage your achievements.
    """

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    rewards = app_commands.Group(name="rewards", description="Manage rewards")

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

            if a.simplified_req:
                requirements = f"- {a.simplified_req}"
            else:
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
        await interaction.followup.send("TIP: Use /achievements check to see if you have any of the above achievements!", ephemeral=True)

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
            balls = await BallInstance.filter(**filters).select_related('ball')
            balls = [ball.ball.country for ball in balls]
            if all(ball in balls for ball in requirements):
                player = await Player.get(discord_id=interaction.user.id)
                has_a = await check_if_achieved(interaction.user.id, a.name)

                if has_a == False:
                    rewards = str(a.rewards).split(";")
                    if rewards:
                        for r in rewards:
                            shiny = False
                            if r.startswith("✨ "):
                                split_r = r[2:].split()
                                if len(split_r) > 0:
                                    reward = split_r[0]
                                    shiny = True
                                else:
                                    continue
                            else:
                                reward = r.strip()
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
        
    @rewards.command(name="list")
    async def rewards_list(self, interaction: discord.Interaction):
        """
        Displays the list of achievements and their rewards
        """
        achievements = await Achievement.filter(achievable=True)
        entries = []
        for a in achievements:
            if a.rewards:
                rewards = str(a.rewards).split(';')
                reward_count = {}
                for reward in rewards:
                    cleaned_reward = reward.strip()
                    if cleaned_reward:
                        if cleaned_reward in reward_count:
                            reward_count[cleaned_reward] += 1
                        else:
                            reward_count[cleaned_reward] = 1

                rewards = '\n'.join(f"- {count}x {reward}" if count > 1 else f"- {reward}" 
                                    for reward, count in reward_count.items())
            else:
                rewards = "- No rewards for this achievement."
            
            entries.append((f"**{a.name}:**", f"Rewards:\n{rewards}"))

        if len(entries) == 0:
            await interaction.response.send_message("There are no achievements registered on this bot.", ephemeral=True)
            return
        
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else DEFAULT_AVATAR_URL

        source = FieldPageSource(entries, per_page=4, inline=False, clear_description=False)
        source.embed.description = "**List of Achievements' Rewards**"
        source.embed.colour = discord.Colour.blurple()
        source.embed.set_thumbnail(url=avatar_url)
        pages = Pages(source=source, interaction=interaction, compact=True)
        await pages.start()
