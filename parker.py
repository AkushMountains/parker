# HackRU2021 Locantore, Thaker, Boccelli, Ishaq

import discord
import json
intents = discord.Intents.default()
intents.members = True
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='$')

TOKEN = " "
userdata = {}
data = {}
userdatach = {}
readdatach = {}

parkRecord = {"Haverford": set(), "Kent": set(), "Philadelphia": set(), "Schuylkill": set(), "Hartwood": set(), "Montgomery": set()}
availableParks = parkRecord.keys()

with open("config.json") as json_file:
    data = json.load(json_file)
    TOKEN = data['TOKEN']

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord and is ready to use Parker')

@client.command()
async def helper(ctx): 
      await ctx.send("```Be sure to register your dog first, or else no other commands will work. Delete will remove your dog's entire entry.\nHere's all of the commands for using Parker:\n$register [name] [age] [breed] [gender] [weight]\n$edit [name] [age] [breed] [gender] [weight]\n$checkin [park name]\n$checkout\n$bark\n$parks\n$show [@user]\n$who [@user]\n$parkcount [park name]\n$picture [image link]\n$edit [attribute] [value]\nFor $edit, valid attributes are 'Name', 'Gender', 'Age', 'Weight' or 'Breed'.```")

@client.command()
async def register(ctx, name, age, breed, gender, weight):
    with open ("dogInfo.json", "a+") as outfile:
        json.dump(userdata, outfile)
    outfile.close()
    for key in userdata:
      if (key == ctx.message.author.mention):
        message = f'Sorry, you already registered a dog. Use $edit to make changes.'
        await ctx.send(message)
        return
    message = f'{ctx.message.author.mention} has registered a {weight} lb {breed} named {name}.'
    await ctx.send(message)
    user = ctx.message.author.mention
    userdata[user] = []
    userdata[user].append({
      "Name": name,
      "Age": age,
      "Breed": breed,
      "Gender": gender,
      "Weight": weight,
      "Park" : "None",
      "Link" : "None"
    })
    with open ("dogInfo.json", "a+") as outfile:
        json.dump(userdata, outfile)
    outfile.close()
    
@client.command()
async def checkin(ctx, dogpark):
    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0]["Park"] = dogpark
    outfile.close()

    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0]["Park"] = dogpark
    outfile.close()
    
    with open ("dogInfo.json") as infile:
        readdata = json.load(infile)
    dogname = readdata[ctx.message.author.mention][0]["Name"]
    infile.close()
    
    parkRecord[dogpark].add(dogname)
    
    message = f"{dogname} is now at {dogpark}!"
    await ctx.send(message)

@client.command()
async def checkout(ctx):
    with open ("dogInfo.json") as outfile:
        userdata = json.load(outfile)
    dogparkbefore = userdata[ctx.message.author.mention][0]["Park"]
    dogname = userdata[ctx.message.author.mention][0]["Name"]
    outfile.close()

    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0]["Park"] = "None"
    outfile.close()

    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0]["Park"] = "None"
    outfile.close()
    
    parkRecord[dogparkbefore].remove(dogname)

    message = f'{dogname} is going home.'
    await ctx.send(message)

@client.command()
async def bark(ctx):
    with open ("dogInfo.json") as outfile:
        userdata = json.load(outfile)
    dogname = userdata[ctx.message.author.mention][0]["Name"]
    outfile.close()
    message = f'{dogname} says ruf-ruf.'
    await ctx.send(message)

@client.command()
async def picture(ctx, link):
    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0]["Link"] = link
    outfile.close()

    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0]["Link"] = link
    outfile.close()

    message = f'{ctx.message.author.mention} has added a picture of their dog. Look!\n'
    await ctx.send(message)
    await ctx.send(link)

@client.command()
async def show(ctx, member: discord.Member): 
    with open ("dogInfo.json") as infile:
        readdatash = json.load(infile)
    
    dogshow = readdatash[member.mention][0]["Name"]
    dogbreed = readdatash[member.mention][0]["Breed"]
    dogparkshow = readdatash[member.mention][0]["Park"]
    dogage = readdatash[member.mention][0]["Age"]
    dogweight = readdatash[member.mention][0]["Weight"]
    doggender = readdatash[member.mention][0]["Gender"]
    doglink = readdatash[member.mention][0]["Link"]
    infile.close()

    message = f"{dogshow} is {member.mention}'s dog, who is a(n) {dogage} year old {dogbreed}. {dogshow} is a(n) {dogweight}lbs {doggender}. The park they are currently at is: {dogparkshow}. Here they are below!\n"
    await ctx.send(message)
    await ctx.send(doglink)

@client.command()
async def edit(ctx, attr, val): 
    attr = str(attr)
    if (attr == "Name" or attr == "Gender" or attr == "Breed"):
      val = str(val)
    elif (attr == "Weight" or attr == "Age"):
      val = int(val)
    else:
      message = f"You didn't enter a real attribute. Please use $helper for usage.\n"
      await ctx.send(message)
      return
    
    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0][attr] = val
    outfile.close()

    with open ("dogInfo.json", "w") as outfile:
        json.dump(userdata, outfile)
    userdata[ctx.message.author.mention][0][attr] = val
    outfile.close()

    message = f"You've successfully edited {attr} to {val}.\n"
    await ctx.send(message)
 
@client.command()
async def who(ctx, member: discord.Member): 
    with open ("dogInfo.json") as infile:
        readdatawho = json.load(infile)
    dogwho = readdatawho[member.mention][0]["Name"]
    message = f"{dogwho} is {member.mention}'s dog.\n"
    await ctx.send(message)

@client.command()
async def parks(ctx): 
    await ctx.send("Here's a list of all the parks:\n")
    for park in availableParks:
      await ctx.send(park)
      
@client.command()
async def parkcount(ctx, parkRequest): 
    if (len(parkRecord[parkRequest]) > 0):
      await ctx.send(f"Dogs currently at {parkRequest}:\n")
      for dog in parkRecord[parkRequest]:
        await ctx.send(dog)
    else: 
      await ctx.send(f"There are currently no other dogs at {parkRequest}.\n")

client.run(TOKEN)
