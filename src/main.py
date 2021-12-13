import discord
import os
import numpy as np
import matplotlib.pyplot as plt
from discord.ext.commands import Bot
TOKEN = os.environ['DISCORD_TOKEN']

BOT_PREFIX = ("=")
bot = discord.Client()
bot = Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
	guild_count = 0
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
		print("Statistics is in " + str(guild_count) + " guilds.")

@bot.command()
async def stats(ctx, arg):
  datalist = [float(x) for x in arg.split(',')]
  datmean = np.mean(datalist)
  datmedian = np.median(datalist)
  datsd = np.std(datalist)

  embed = discord.Embed(title = "Statistics Results")
  embed.add_field(name = "Mean", value = datmean)
  embed.add_field(name = "Median", value = datmedian)
  embed.add_field(name = "Standard Deviation", value = datsd, inline = False)
  
  plt.boxplot(datalist)
  plt.title(f'{ctx.message.author}\'s Graph')
  plt.savefig(fname='plot')
  file = discord.File("plot.png")
  embed.set_image(url="attachment://plot.png")

  await ctx.send(embed=embed, file=file)
  
  plt.clf()
  os.remove('plot.png')

  
bot.run(TOKEN)