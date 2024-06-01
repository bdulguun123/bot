import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from keep_alive import keep_alive

load_dotenv()

intents = discord.Intents().all()
intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents)

rolls = {}


@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))


@bot.command()
async def stop_roll(ctx):
  rolls.clear()
  await ctx.send("Өмнөх Roll устлаа.")


@bot.command()
async def roll(ctx):
  if ctx.author.id in rolls:
    user_name = ctx.guild.get_member(ctx.author.id).display_name
    await ctx.send(f"{user_name} roll хийцэн байна алмин")
  else:
    roll_result = random.randint(0, 100)
    rolls[ctx.author.id] = roll_result
    await ctx.send(f"{ctx.author.mention} roll: {roll_result}")


@bot.command()
async def show_rolls(ctx):
  sorted_rolls = sorted(rolls.items(), key=lambda x: x[1], reverse=True)
  if not sorted_rolls:
    await ctx.send("Roll байхгүй байна.")
  else:
    output = "\n".join([
        f"{ctx.guild.get_member(user_id).display_name if ctx.guild.get_member(user_id) else 'Unknown'}: {roll}"
        for user_id, roll in sorted_rolls
    ])
    await ctx.send("Sorted rolls:\n" + output)


keep_alive()
bot.run(os.getenv('TOKEN'))
