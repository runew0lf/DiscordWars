import logging
import asyncio
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from discord import Embed
from cogs.data.data import guild_resources
from cogs.data.data import player_resources
from cogs.data.data import resource_emoji
from cogs.data.data import resource_list
log = logging.getLogger(__name__)


class PlayerResources:
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        self.player_resources = player_resources
        self.guild_resources = guild_resources

    def check_player(self, player_id):
        if not self.player_resources.data.get('players').get(str(player_id)):
            self.player_resources.data['players'][str(player_id)] = {"resources": resource_list}
            self.player_resources.data['players'][str(player_id)]["Gathering"] = None
            self.player_resources.save()

    async def on_ready(self):
        if not self.player_resources.data.get('players'):
            self.player_resources.data['players'] = {}
            self.player_resources.save()
        self.bot.loop.create_task(self.tick())

    async def tick(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(30)
            for player in self.player_resources.data['players']:
                if self.player_resources.data['players'][player]["gathering"]:
                    resource = self.player_resources.data['players'][player]["gathering"]
                    if self.player_resources.data['players'][player]["resources"][resource] < 5:
                        self.player_resources.data['players'][player]["resources"][resource] += 1
                        if self.player_resources.data['players'][player]["resources"][resource] == 5:
                            self.player_resources.data['players'][player]["gathering"] = None
                self.player_resources.save()
            print("TICK")

    @commands.command(name="inv")
    async def resources(self, ctx):
        """Check what resources you are carrying"""
        self.check_player(ctx.author.id)
        current_resource_list = self.player_resources.data['players'][str(ctx.author.id)]['resources']
        gathering = self.player_resources.data['players'][str(ctx.author.id)]['gathering']
        if not gathering:
            gathering = "Nothing"
        else:
            gathering = f"{gathering} - {resource_emoji[gathering]}"
        embed = Embed(title=f"{ctx.author.name} -  Inventory", description=f"Gathering: {gathering}", color=ctx.me.color)
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

    @commands.command(name="gather")
    async def gather(self, ctx, resource):
        """Gathers a resource"""
        if resource not in resource_list:
            await ctx.send("I cannot find this resource to gather")
        else:
            self.check_player(ctx.author.id)
            self.player_resources.data['players'][str(ctx.author.id)]['gathering'] = resource
            await ctx.send(f"You are now gathering {resource}")

    @commands.command(name="deliver")
    async def deliver(self, ctx):
        """Delivers your resources to the guild"""
        delivery_string = ""
        self.player_resources.data['players'][str(ctx.author.id)]['gathering'] = None
        for resource in self.player_resources.data['players'][str(ctx.author.id)]['resources']:
            self.guild_resources.data['servers'][str(ctx.guild.id)]["resources"][resource] += self.player_resources.data['players'][str(ctx.author.id)]['resources'][resource]
            if self.player_resources.data['players'][str(ctx.author.id)]['resources'][resource] != 0:
                delivery_string += f"{self.player_resources.data['players'][str(ctx.author.id)]['resources'][resource]} - {resource}, "
            self.player_resources.data['players'][str(ctx.author.id)]['resources'][resource] = 0
            self.guild_resources.save()
            self.player_resources.save()
        if delivery_string == "":
            delivery_string = "Nothing"
        await ctx.send(f"You delivered the following: {delivery_string}")


def setup(bot):
    bot.add_cog(PlayerResources(bot))
    log.info('Cog loaded: PlayerResources')
