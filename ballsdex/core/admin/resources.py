from ballsdex.core.models import (
    Achievement,
    AchievementInstance, # ADD THESE IMPORTS
)

@app.register
class AchievementResource(Model):
    label = "Achievement"
    model = Achievement
    page_size = 50
    icon = "fas fa-trophy"
    page_pre_title = "achievement list"
    page_title = "Achievements"
    filters = [
        filters.Search(
            name="name",
            label="Name",
            search_mode="icontains",
            placeholder="Search for achievements",
        ),
        filters.Boolean(name="achievable", label="Achievable"),
    ]
    fields = [
        "name",
        "requirements",
        "simplified_req",
        "rewards",
        "achievable",
        "firstball",
        "created_at",
    ]

@app.register
class AchievementInstanceResource(Model):
    label = "Achievement instance"
    model = AchievementInstance
    icon = "fas fa-crown"
    page_pre_title = "achievement instances list"
    page_title = "Achievement instances"
    filters = [
        filters.Search(
            name="id",
            label="Achievement Instance ID",
            placeholder="Search for achievement IDs",
        ),
        filters.ForeignKey(model=Achievement, name="achievement", label="Achievement"),
        filters.Search(
            name="player__discord_id",
            label="User ID",
            placeholder="Search for Discord user ID",
        ),
        filters.Search(
            name="server_id",
            label="Server ID",
            placeholder="Search for Discord server ID",
        ),
    ]
    fields = [
        "id",
        "achievement",
        "player",
        "server_id",
    ]

# ADD THESE 2 RESOURCES AT THE VERY END OF YOUR RESOURCES.PY FILE
