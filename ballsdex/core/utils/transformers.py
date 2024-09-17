from ballsdex.core.models import (
    Achievement,
    achievements, # add these to your existing imports
)
__all__ = (
    "AchievementTransform",
    "AchievementAchievableTransformer",
) # add these to your exist __all__ list
class AchievementTransformer(TTLModelTransformer[Achievement]):
    name = "achievement"
    model = Achievement()

    def key(self, model: Achievement) -> str:
        return model.name

    async def load_items(self) -> Iterable[Achievement]:
        return achievements.values()
    
class AchievementAchievableTransformer(AchievementTransformer):
    async def load_items(self) -> Iterable[Achievement]:
        return {k: v for k, v in achievements.items() if v.achievable}.values()

    async def transform(
        self, interaction: discord.Interaction["BallsDexBot"], value: str
    ) -> Optional[Achievement]:
        try:
            achievement = await super().transform(interaction, value)
            if achievement is None or not achievement.achievable:
                raise ValueError(
                    f"This achievement is disabled and will not be shown."
                )
            return achievement
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return None

AchievementTransform = app_commands.Transform[Achievement, AchievementTransformer]
AchievementAchievableTransform = app_commands.Transform[Achievement, AchievementAchievableTransformer]

# add all these other stuff to the very end of your transformers.py file
