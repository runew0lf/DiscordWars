from discord.ext import commands
import logging
from discord.ext.commands import AutoShardedBot
from cogs.utils import pyson
from cogs.utils import checks
config = pyson.Pyson('data/config/startup.json')

log = logging.getLogger(__name__)


class Owner:
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(aliases=['sp', 'prefix'])
    @checks.is_guild_owner()
    async def set_prefix(self, ctx, prefix: str=None):
        ''': Change the prefix of the bot, up to two chars.'''
        if not prefix:
            prefix = self.bot.config.data.get('servers').get(str(ctx.guild.id)).get('prefix')
            await ctx.send(f'current prefix is {prefix}')
            return
        else:
            if len(prefix) >= 3:
                await ctx.send('Prefix length too long.')
                return

            self.bot.config.data['servers'][str(ctx.guild.id)]['prefix'] = prefix
            self.bot.config.save()
            await ctx.send(f'Prefix updated to {prefix}')


def setup(bot):
    bot.add_cog(Owner(bot))
    log.info("Cog loaded: Owner")
