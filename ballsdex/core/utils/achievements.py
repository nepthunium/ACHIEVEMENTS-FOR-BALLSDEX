from ballsdex.core.models import Achievement, AchievementInstance

async def check_if_achieved(player_id: int, achievement) -> bool:
    a = await Achievement.get(name=achievement)
    filters = {"player__discord_id": player_id, "achievement": a}
    a1 = await AchievementInstance.filter(**filters)
    if a1:
        return True
    return False