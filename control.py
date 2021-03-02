####                                                                               ####
#                                                                                     #
#     CCCCCC    OOOOOO     NNN     NN  TTTTTTTTTT  RRRRRRRR      OOOOOO    LL         #
#   CCCCCCC   OOOO  OOOO  NN NN    NN      TT      RR      RR  OOOO  OOOO  LL         #
#   CC        OO      OO  NN  NN   NN      TT      RR      RR  OO      OO  LL         #
#  CC         OO      OO  NN   NN  NN      TT      RR    RR    OO      OO  LL         #
#   CC        OO      OO  NN    NN NN      TT      RRRRRR      OO      OO  LL         #
#   CCCCCCC   OOOO  OOOO  NN    NN NN      TT      RR    RR    OOOO  OOOO  LL         #
#     CCCCCC    OOOOOO    NN     NNN       TT      RR     RR     OOOOOO    LLLLLLLL   #
#                                                                                     #
####                                                                               ####
#                CONTROL LIVES ON. THE FUTURE NARROWS. VERSION 0.1                    #
####                                                                               ####
# Due to my strong personal convictions, I wish to stress that this bot in no way     #
# endorses a belief in the occult.                                                    #
####                                                                               ####

import os, sys
import json, csv 
import discord 
import pandas as pd
import numpy as np
import asyncio
import datetime
import psutil, time
import requests
from discord.ext import commands, tasks
import string
import schedule
import random

#Just some basic stuff
token = open("spheredata.txt","r").readline()

bot = commands.Bot(command_prefix='/')
checkrole = commands.has_role


#Just some basic info about the machine/process


#Just so I know it's working, and all
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the Sphere Data | Prefix: /"))
    print('Logged in as '+bot.user.name +'. The future is bleak.')

async def is_owner(ctx):
    return ctx.author.id == 184321873406984192


@bot.event
async def on_command_error(ctx, error):
    return

@bot.event
async def on_message(message):
    publishchannels = [241642176927236097, 256141113293799424, 256140787039993867, 583281331371507714]
    mention = f'<@!{bot.user.id}>' +' resistance is futile'
    message1 = message.content
    endswith = message1.endswith("?")
    rngtossup = f'<@!{bot.user.id}>'
    #By request?
    if rngtossup in message.content and endswith == True:
        rng = ('Yes.', 'No.')
        randomised = random.choice(rng)
        await message.channel.send(randomised)
    #Silly Meme!
    if mention in message.content:
        await message.channel.send("https://cdn.discordapp.com/attachments/310827329360232449/784492034479751218/struggle.mp4")
    #Channel Autopublishing
    if message.channel.id in publishchannels:
        await message.publish()

    await bot.process_commands(message)



##BOT STATS

@bot.command()
async def stats(ctx):
    pcname = os.environ['COMPUTERNAME']
    botstarttime = psutil.Process(os.getpid())
    botstarttime.create_time()
    botstartdatetime = datetime.datetime.fromtimestamp(botstarttime.create_time())
    currenttime = datetime.datetime.now()
    botuptime = currenttime - botstartdatetime
    embed2=discord.Embed(title="Control Statistics", description="Various information about the Control bot.")
    embed2.add_field(name="Hosted On...", value=pcname, inline=False)
    embed2.add_field(name="Current Uptime...", value=botuptime, inline=False)
    await ctx.send(embed=embed2)


### REVISED TRACKER COMMANDS
 ## Control has an event tracker, unfortunately due to STO lacking any APIs it's impossible to automate collecting event information. Thus, all data must be inputted manually.
 ## Because I do not have unlimited time, this has been implemented in-Discord using the /event command.
 ## The bot's been designed so only certain people can use the commands, as to avoid people breaking the event functionality. In this case, the @Control Group role of the Star Trek Online server.
 ## To change, just change the ID '783680970351837195' to one corresponding to a role on your server. 
###

@bot.group()
async def event(ctx):
    role = discord.utils.get(ctx.guild.roles, id=783680970351837195)
    if role in ctx.author.roles:
        if ctx.invoked_subcommand is None:
            eventembed=discord.Embed(title="Command Error", description="Missing or invalid argument, the following commands will work:")
            eventembed.add_field(name="/event create", value='Adds an event to the table. Usage Example: `/event create "Anniversary Event" "2021-01-26 16:00:00" "2021-03-04 18:00:00"`')
            eventembed.add_field(name="/event delete", value='Deletes an event from the table based on its **name**. Usage Example: `/event delete "Anniversary Event"`')
            await ctx.send(embed=eventembed)
    else:
        ctrlerror=discord.Embed(title="Command Error", description="This command requires you to have the `@Control Group` role on the Star Trek Online Discord.")
        await ctx.send(embed=ctrlerror)
## Deletes the named event from the tracker.json file.
@event.command()
async def delete(ctx, arg):
    trackerfile = 'events.csv'
    role = discord.utils.get(ctx.guild.roles, id=783680970351837195)
    if role in ctx.author.roles:
        data = pd.read_csv(trackerfile)
        data = data[data.name != arg]
        data.to_csv(trackerfile, index=False)
    else:
        ctrlerror=discord.Embed(title="Command Error", description="This command requires you to have the `@Control Group` role on the Star Trek Online Discord.")
        await ctx.send(embed=ctrlerror)

## Creates a new tracker with the given name.
@event.command()
async def create(ctx, arg1, arg2, arg3):
    trackerfile = 'events.csv'
    role = discord.utils.get(ctx.guild.roles, id=783680970351837195)
    if role in ctx.author.roles:
        data = pd.read_csv(trackerfile)
        newevent = {'name':arg1, 'startdate':arg2, 'enddate':arg3}
        data = data.append(newevent, ignore_index=True)
        data.to_csv(trackerfile, index=False)
    else:
        ctrlerror=discord.Embed(title="Command Error", description="This command requires you to have the `@Control Group` role on the Star Trek Online Discord.")
        await ctx.send(embed=ctrlerror)

@bot.group()
async def tracker(ctx):
    if ctx.invoked_subcommand is None:
        listembed=discord.Embed(title="Control Tracker", description="The following trackers are available:")
        listembed.add_field(name="legendary", value="Tracks the last time the Legendary Bundle was available.", inline=False)
        listembed.add_field(name="event", value="Tracks events, with inconsistent accuracy.", inline=False)
        listembed.set_footer(text="Do '/tracker [name]' to see a tracker.")
        await ctx.channel.send(embed=listembed)


@tracker.command()
async def legendary(ctx):
    trackerfile = 'tracker.json'
    with open(trackerfile, 'r') as f:
        data = json.load(f)
        thisday = datetime.datetime.now()
        datetouse = data[ 'legendary' ][ 'startdate' ]
        converteddate = datetime.datetime.strptime(datetouse, "%Y-%m-%d %H:%M:%S")
        delta = thisday - converteddate
        deltad1 = delta.days
        deltads = str(deltad1)

        deltam = thisday - converteddate
        deltam1 = int(deltam.total_seconds() * 1000)
        deltams = str(deltam1)

        legendarytime=discord.Embed(title="Legendary Bundle Tracker", description="The last time the 10th Anniversary Legendary Bundle was seen on PC was " +deltads +" days ago.", color=0xffffff)
        legendarytime.set_footer(text="That was " +deltams +" microseconds ago!")
        await ctx.channel.send(embed=legendarytime)

@tracker.command()
async def events(ctx):
    trackerfile = 'events.csv'
    eventtracker=discord.Embed(title="Event Tracker", description="The following events are currently accounted for:")
    with open(trackerfile) as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        currentdate = datetime.datetime.now()
        for row in csv_reader:
            eventstart = row[ 'startdate' ]
            eventstartconverted = datetime.datetime.strptime(eventstart, "%Y-%m-%d %H:%M:%S")
            eventstartformat = eventstartconverted.strftime("%d/%m/%Y at %H:%M:%S (UTC)")
            eventend = row[ 'enddate' ]
            eventendconverted = datetime.datetime.strptime(eventend, "%Y-%m-%d %H:%M:%S")
            eventendformat = eventendconverted.strftime("%d/%m/%Y at %H:%M:%S (UTC)")
            eventname = row['name']
            line_count += 1

            if eventstartconverted > currentdate:
                eventdelta = eventstartconverted - currentdate
                eventdeltad = eventdelta.days
                eventdeltads = str(eventdeltad)
                eventcountdown = '\nThis event will begin in ' +eventdeltads +' days.'

            if eventstartconverted < currentdate:
                eventdelta = eventendconverted - currentdate
                eventdeltad = eventdelta.days
                eventdeltads = str(eventdeltad)
                eventcountdown = '\nThis event will end in ' +eventdeltads +' days.'

            eventtracker.add_field(name=eventname, value="Starts on: " +eventstartformat +"\nEnds on: " +eventendformat +eventcountdown, inline=False)
        
        await ctx.channel.send(embed=eventtracker)


# Moderation Commands

@bot.command()
async def avatar(ctx, *, avatar : discord.Member=None):
    avatarembed = discord.Embed()
    avatarembed.set_image(url=avatar.avatar_url)
    avatarembed.set_author(name=avatar.name +'#' +avatar.discriminator, url=discord.Embed.Empty, icon_url=avatar.avatar_url)
    await ctx.channel.send(embed=avatarembed)

@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user : discord.Member=None, *, reason):
    await user.kick(reason=reason)
    kick = discord.Embed(title=f"Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
    await ctx.message.delete()
    await ctx.channel.send(embed=kick)
    await user.send(embed=kick)
    


#### WIKI COMMANDS!
 ## To generate a shiplist, use this: https://sto.gamepedia.com/Special:CargoExport?tables=Ships&&fields=name%2C+image%2C+faction%2C+ranklevel%2C+tier%2C+type%2C+hullmod%2C+shieldmod%2C+turnrate%2C+impulse%2C+inertia%2C+powerall%2C+powerweapons%2C+powershields%2C+powerengines%2C+powerauxiliary%2C+powerboost%2C+fore%2C+aft%2C+equipcannons%2C+devices%2C+boffs%2C+consolestac%2C+consoleseng%2C+consolessci%2C+uniconsole%2C+t5uconsole%2C+hangars%2C+abilities&&order+by=%60name%60%2C%60image%60%2C%60cargo__Ships%60.%60faction__full%60%2C%60ranklevel%60%2C%60tier%60&limit=5000&format=json
 ## I'd automate it but, the wiki API is limited to 500 entries for standard users (IIRC), so it can't *quite* pull the entire ship list.
####


# Ship Info!
@bot.command()
async def ship(ctx, arg):
    shipz = 'shipexport.json'
    with open(shipz, 'r') as f:
        data = json.load(f)
 #   arg1 = arg.title()
    for i in data:
        if i['name'] == arg:
            faction = str(i['faction'])
            consolestac = str(i['consolestac'])
            consolessci = str(i['consolessci'])
            consoleseng = str(i['consoleseng'])

            shiptier = str(i['tier'])
            shiptype = str(i['type'][0])

            foreweap = str(i['fore'])
            aftweap = str(i['aft'])

            boffs = i['boffs']
            boffs2 = ('%s' % ', '.join(map(str, boffs)))

            shipembed=discord.Embed(title=i['name'] +' Stats', description="Tier " +shiptier +" " +shiptype)
            shipembed.add_field(name="Power Bonus", value="To Do", inline=True)
            shipembed.add_field(name="Weapon Hardpoints", value='**Fore:** ' +foreweap +'\n**Aft:** ' +aftweap, inline=True)
            shipembed.add_field(name="Consoles", value='**Tactical Consoles:** ' +consolestac +'\n' +'**Science Consoles:** ' +consolessci +'\n' +'**Engineering Consoles:** ' +consoleseng, inline=True)
            shipembed.add_field(name="Bridge Officers", value=boffs2, inline=False)
            await ctx.send(embed=shipembed)



# Random Ship Selector
@bot.command(aliases=['rs'])
async def randomship(ctx, *args):
    se = 'shipexport.json'
    a = len(args)
    number = 1

    if a > 0: 
        try:
            number = int(args[0])
        except ValueError:
            return
        
    with open(se, 'r') as f:
        data = json.load(f)
        test = len(data)

        if a < 1:
            x = random.randint(1, test)
            test2 = data[x]['name']
            baseurl = data[x]['image']
            img = requests.get("https://sto.gamepedia.com/api.php?action=imageserving&format=json&wisTitle=" + baseurl)
            img = img.json()
            image = img['image']['imageserving']
            pagename = test2.replace(" ", "_")
            pageurl = "https://sto.gamepedia.com/" + pagename
            shiptier = str(data[x]['tier'])
            shiptype = str(data[x]['type'][0])

            shipembed=discord.Embed(title=test2, url=pageurl, description="Tier " +shiptier +" " +shiptype)
            shipembed.set_thumbnail(url=image)
            await ctx.send(embed=shipembed)

        if a > 0 and number < 11:
            r = range(number)
            shipembed=discord.Embed(title='List of Randomised Starships')
            for n in r:
                x = random.randint(1, test)
                test2 = data[x]['name']

                shiptier = str(data[x]['tier'])
                shiptype = str(data[x]['type'][0])

                shipembed.add_field(name=test2, value="Tier " +shiptier +" " +shiptype, inline=False)
            
            await ctx.send(embed=shipembed)

@bot.command(pass_context = True)
async def testcommand2(ctx, *args):
    se = 'shipexport.json'
    a = len(args)
    number = 1

    if a > 0: 
        try:
            number = int(args[0])
        except ValueError:
            return
        
    with open(se, 'r') as f:
        data = json.load(f)
        test = len(data)

        if a < 1:
            x = random.randint(1, test)
            test2 = data[x]['name']
            baseurl = data[x]['image']
            img = requests.get("https://sto.gamepedia.com/api.php?action=imageserving&format=json&wisTitle=" + baseurl)
            img = img.json()
            image = img['image']['imageserving']
            pagename = test2.replace(" ", "_")
            pageurl = "https://sto.gamepedia.com/" + pagename
            shiptier = str(data[x]['tier'])
            shiptype = str(data[x]['type'][0])

            shipembed=discord.Embed(title=test2, url=pageurl, description="Tier " +shiptier +" " +shiptype)
            shipembed.set_thumbnail(url=image)
            await ctx.send(embed=shipembed)

        if a > 0:
            r = range(number)
            shipembed=discord.Embed(title='List of Randomised Starships')
            for n in r:
                x = random.randint(1, test)
                test2 = data[x]['name']

                shiptier = str(data[x]['tier'])
                shiptype = str(data[x]['type'][0])

                shipembed.add_field(name=test2, value="Tier " +shiptier +" " +shiptype, inline=False)
            
            await ctx.send(embed=shipembed)


# RNG Commands

@bot.command()
async def droprate(ctx, arg1):
    count = 0
    rolls = 0

    try:
        arg = float(arg1)
    except ValueError:
        return

    if arg > 0.001 and arg < 100:

        while count < 1:
            if random.random() * 100 < arg:
                count = count+1
                rolls = rolls+1
                if rolls > 200:
                    gamblingembed = discord.Embed(title="Processing Complete", description="It took " +str(rolls) +" rolls to get a drop with the given percentage. My condolences.")
                elif rolls > 400:
                    gamblingembed = discord.Embed(title="Processing Complete", description="It took " +str(rolls) +" rolls to get a drop with the given percentage. That would cost A LOT.")
                else: 
                    gamblingembed = discord.Embed(title="Processing Complete", description="It took " +str(rolls) +" rolls to get a drop with the given percentage.")
                await ctx.send(embed=gamblingembed)

            else:
                rolls = rolls+1
    else:
        await ctx.send('Number needs to be higher than 0.001 (technical reasons, sorry) but below 100.')


@bot.command()
async def coinflip(ctx):
    coins = ('Tails', 'Heads')
    rng = random.choice(coins)
    await ctx.send(rng)

@bot.command()
async def diceroll(ctx, *args):
    a = len(args)

    if a > 0: 
        try:
            rolls = int(args[0])
        except ValueError:
            return
        if a > 1:
            try:
                dicenum = int(args[1])
            except ValueError:
                return

    if a < 1:
        x = random.randint(1, 6)
        y = str(x)
        output = "Rolled a standard 6-side die once, results are:\n" +y
        await ctx.send(output) 

    if a == 1:
        if rolls < 11:
            numofrolls = str(args[0])
            output = "Rolled a standard 6-side die " +numofrolls +" times, results are:\n"
            r = range(rolls)
            for n in r:
                x = random.randint(1, 6)
                x = str(x)
                output = output +x +"\n" 
            await ctx.send(output)
        else:
            await ctx.send("For anti-spam purposes, you can only roll the dice up to 10 times at once.")

    if a > 1:
        if rolls < 11:
            numofrolls = str(args[0])
            dicesides = str(args[1])
            output = "Rolled a " +dicesides +"-sided die " +numofrolls +" times, results are: \n"
            r = range(rolls)
            for n in r:
                x = random.randint(1, dicenum)
                x = str(x)
                output = output +x +"\n"
            await ctx.send(output)
        else:
            await ctx.send("For anti-spam purposes, you can only roll the dice up to 10 times at once.")

@bot.command()
async def choice(ctx, *args):
    rng = random.choice(args)
    await ctx.send(rng)

@bot.command()
async def choicex(ctx, *args):
    try:
        rolls = int(args[0])
    except ValueError: 
        return
    inputs = args[1:]

    r = range(rolls)
    counter = 0
    output = "Output complete:\n"
    for n in r:
        rng = random.choice(inputs)
        counter = counter+1
        count = str(counter)
        output = output +count +": " +rng +"\n" 
    await ctx.send(output)

### ROLES

@bot.group()
async def role(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Test")


@role.command()
async def PC(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="PC")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **PC** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.remove_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **PC** Role.")
        await ctx.send(embed=removeembed)

@role.command()
async def PS4(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="PS4")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **PS4** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.add_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **PS4** Role.")
        await ctx.send(embed=removeembed)

@role.command()
async def XB1(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="XB1")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **XB1** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.remove_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **XB1** Role.")
        await ctx.send(embed=removeembed)

@role.command()
async def PvP(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="PvP")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **PvP** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.remove_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **PvP** Role.")
        await ctx.send(embed=removeembed)

@role.command()
async def RP(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="RP")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **RP** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.remove_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **RP** Role.")
        await ctx.send(embed=removeembed)

@role.command()
async def Elites(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Elites")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **Elites** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.remove_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **Elites** Role.")
        await ctx.send(embed=removeembed)

@role.command()
async def Shipwright(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Shipwright")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **Shipwright** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.remove_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **Shipwright** Role.")
        await ctx.send(embed=removeembed)

@role.command()
async def Helper(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Helper")
    if role not in user.roles:
        await discord.Member.add_roles(user, role)
        addembed = discord.Embed(title="Role Added", description=":white_check_mark: You have added the **Helper** Role.")
        await ctx.send(embed=addembed)
    else:
        await discord.Member.remove_roles(user, role)
        removeembed = discord.Embed(title="Role Removed", description=":negative_squared_cross_mark: You have removed the **Helper** Role.")
        await ctx.send(embed=removeembed)




@bot.command()
async def acc(ctx, arg1, arg2):
    try:
        x = int(arg1)
    except ValueError:
        return

    try:
        y = int(arg2)
    except ValueError:
        return

    z = (x-y)/(x-y+100)

    accembed = discord.Embed(title="Accuracy Overflow Calculation", description="")

    crith = (z * 12.5)
    checkthis = crith
    crith = str(round(crith, 2))
    critd = (z * 50)
    critd = str(round(critd, 2))
    if checkthis > 0:
        accembed.add_field(name="Critical Hit Chance", value=crith +"%", inline=True)
        accembed.add_field(name="Critical Hit Severity", value=critd +"%", inline=True)
        await ctx.send(embed=accembed)
    else:
        await ctx.send("Enemy defense is higher than your accuracy, so there wouldn't be any Accuracy Overflow.")


## Experimental Damage Calculation Command. Heavily WIP!

@bot.command()
async def dmg(ctx, *args):
    weapontypedict = {
        "beam":200,
        "dbb":260,
        "quad":198,
        "dhc":288,
        "dc":192,
        "cannon":162,
        "heavycannon":243,
        "turret":101
    }

    mkdict = {
        "mk1":8.163254,
        "mk2":18.367322,
        "mk3":28.571390,
        "mk4":38.775458,
        "mk5":48.979525,
        "mk6":59.183593,
        "mk7":69.387661,
        "mk8":79.591729,
        "mk9":89.795797,
        "mk10":99.999864,
        "mk11":110.203932,
        "mk12":120.408,
        "mk13":175.204,
        "mk14":230.000,
        "mk15":284.796
    }
    mkinput = str(args[1])
    weapinput = str(args[0])
    if mkinput in mkdict: 
        mkdamage = mkdict.get(mkinput)

    if weapinput in weapontypedict:
        basedamage = weapontypedict.get(weapinput)

    markcat1 = int(mkdamage)
    weapondamage = int(basedamage)

    cat1percent = (markcat1 + 50)/100 # level 30 bonus / 100 skill points in energy weapons / fleet bonus / endeavour bonus / accolade bonus
    weaponspower = float(args[2])
    weaponpower = ((weaponspower)+100)/200
    calc = str(weapondamage * weaponpower * (1+cat1percent))

    await ctx.send(calc)



bot.run(token)      

