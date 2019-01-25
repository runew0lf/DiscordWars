import logging
import asyncio
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from discord import Embed
from cogs.data.data import guild_resources
from cogs.data.data import resource_emoji
from cogs.data.data import resource_list
log = logging.getLogger(__name__)


class GuildResources:
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        self.guild_resources = guild_resources

    async def on_ready(self):
        for guild in self.bot.guilds:
            if not self.guild_resources.data.get('servers'):
                self.guild_resources.data['servers'] = {}
                self.guild_resources.save()
                if not self.guild_resources.data.get('servers').get(str(guild.id)):
                    self.guild_resources.data['servers'][str(guild.id)] = {"resources": resource_list}
                    self.guild_resources.save()
        self.bot.loop.create_task(self.tick())

    async def tick(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(30)

    @commands.command(name="resources")
    async def resources(self, ctx):
        """Displays the guilds current resources"""
        current_resource_list = self.guild_resources.data['servers'][str(ctx.guild.id)]['resources']
        embed = Embed(title=f"{ctx.guild.name} -  Resources", description="", color=ctx.me.color)
        embed.add_field(name=f"Food - {resource_emoji['Food']}", value=current_resource_list['Food'])
        embed.add_field(name=f"Iron - {resource_emoji['Iron']}", value=current_resource_list['Iron'])
        embed.add_field(name=f"Wood - {resource_emoji['Wood']}", value=current_resource_list['Wood'])
        embed.add_field(name=f"Stone - {resource_emoji['Stone']}", value=current_resource_list['Stone'])
        embed.add_field(name=f"Livestock - {resource_emoji['Livestock']}", value=current_resource_list['Livestock'])
        embed.add_field(name=f"Coal - {resource_emoji['Coal']}", value=current_resource_list['Coal'])
        embed.add_field(name=f"Gems - {resource_emoji['Gems']}", value=current_resource_list['Gems'])
        embed.add_field(name=f"Gold - {resource_emoji['Gold']}", value=current_resource_list['Gold'])
        embed.add_field(name=f"Herbs - {resource_emoji['Herbs']}", value=current_resource_list['Herbs'])
        embed.add_field(name=f"Grain - {resource_emoji['Grain']}", value=current_resource_list['Grain'])
        embed.add_field(name=f"Workers - {resource_emoji['Workers']}", value=current_resource_list['Workers'])
        embed.add_field(name=f"Water - {resource_emoji['Water']}", value=current_resource_list['Water'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GuildResources(bot))
    log.info('Cog loaded: GuildResources')
