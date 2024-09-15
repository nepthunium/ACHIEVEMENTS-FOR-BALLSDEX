from ballsdex.core.models import (
    Achievement,
    AchievementInstance, # ADD THESE NEW IMPORTS
)

"Achievement": Achievement,
"AchievementInstance": AchievementInstance, # OPTIONAL, BUT FIND class Dev(commands.Cog) AND PUT THESE IN YOUR get_environment FUNCTION IF YOU WANNA USE THESE ACHIEVEMENT/ACHIEVEMENTINSTANCE MODELS IN EVALS WITHOUT IMPORTING THEM ALL THE TIME
