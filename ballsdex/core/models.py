# ADD THIS STUFF TO YOUR MODELS.PY

achievements: dict[int, Achievement] = {}

async def convert_req_to_list(
    model: Type[Achievement],
    instance: Achievement,
    created: bool,
    using_db: "BaseDBAsyncClient | None" = None,
    update_fields: Iterable[str] | None = None,
):
    if instance.requirements:
        instance.requirements = ";".join(
            [x.strip() for x in instance.requirements.split(";")]
        )

async def convert_rew_to_list(
    model: Type[Achievement],
    instance: Achievement,
    created: bool,
    using_db: "BaseDBAsyncClient | None" = None,
    update_fields: Iterable[str] | None = None,
):
    if instance.rewards:
        instance.rewards = ";".join(
            [x.strip() for x in instance.rewards.split(";")]
        )

class Achievement(models.Model):
    name = fields.CharField(max_length=48, unique=True)
    requirements = fields.TextField(
        null=True,
        default=None,
        description="Requirements for getting this achievement seperated by semicolons (please enter the correct name of the ball else wont work properly)",
    )
    simplified_req = fields.CharField(max_length=48, null=True, description="(Optional) This will be displayed in /achievements list. Use this if you have too many requirements")
    rewards = fields.TextField(
        null=True,
        default=None,
        description="Reward(s) for getting the achievement",
    )
    achievable = fields.BooleanField(default=True)
    firstball = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)

    instances: fields.BackwardFKRelation[AchievementInstance]

    def __str__(self) -> str:
        return self.name
    
Achievement.register_listener(signals.Signals.pre_save, convert_req_to_list)
Achievement.register_listener(signals.Signals.pre_save, convert_rew_to_list)
    
class AchievementInstance(models.Model):
    achievement_id: int

    achievement: fields.ForeignKeyRelation[Achievement] = fields.ForeignKeyField("models.Achievement")
    player: fields.ForeignKeyRelation[Player] = fields.ForeignKeyRelation(
        "models.Player", related_name="achievements"
    )  # type: ignore
    server_id = fields.BigIntField(
        description="Discord server ID where this achievement was achieved", null=True
    )

    class Meta:
        unique_together = ("player", "id")

    @property
    def is_achievable(self) -> bool:
        return (
            self.achievable
            and self.achievement.achievable
        )
    
    def __str__(self) -> str:
        return self.to_string()

    def to_string(self, bot: discord.Client | None = None) -> str:
        return f"#{self.pk:0X}: {self.achievement.name}"
