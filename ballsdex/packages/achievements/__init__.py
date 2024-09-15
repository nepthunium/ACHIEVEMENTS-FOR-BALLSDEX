from typing import TYPE_CHECKING

from ballsdex.packages.achievements.cog import Achievements

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot


async def setup(bot: "BallsDexBot"):
    await bot.add_cog(Achievements(bot))
