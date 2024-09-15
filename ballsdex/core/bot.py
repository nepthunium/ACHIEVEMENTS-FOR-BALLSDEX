from ballsdex.core.models import (
    Achievement, # ADD THIS IMPORT
)

PACKAGES = ["config", "players", "countryballs", "info", "admin", "trade", "balls", "battle", "achievements"] # ADD ACHIEVEMENTS PACKAGE TO PACKAGES LIST

achievements.clear()
for achievement in await Achievement.all():
    achievements[achievement.pk] = achievement
table.add_row("Achievements", str(len(achievements))) # FIND YOUR LOAD_CACHE FUNCTION AND ADD THIS THERE
