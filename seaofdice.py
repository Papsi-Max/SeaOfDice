import discord
from discord.ext import commands
import random
import asyncio

TOKEN = 'YOURTOKEN'

prefix = '!'

bot = commands.Bot(command_prefix=prefix)
client = discord.Client()

diceFaces = ["💀", "💰", "💎", "🔪", "🐵", "🐦"]
#deck = ["pirate", "pirate", "pirate", "pirate", "ile", "ile", "ile", "ile", "1TDM", "1TDM", "1TDM", "2TDM", "2TDM", "gardienne", "gardienne", "gardienne", "gardienne", "bateau1000", "bateau1000", "bateau500", "bateau500", "bateau300", "bateau300", "or", "or", "or", "or", "diamant", "diamant", "diamant", "diamand", "animaux", "animaux", "animaux", "animaux"]
deck = ["Pirate", "Pirate", "Pirate", "Pirate", "Ile", "Ile", "Ile", "Ile", "1TDM", "1TDM", "1TDM", "2TDM", "2TDM", "Or", "Or", "Or", "Or", "Diamant", "Diamant", "Diamant", "Diamand", "Animaux", "Animaux", "Animaux", "Animaux"]
#Pirate : Ok
#Ile : Ok
#TDM : Ok
#Gardienne : /
#Bateau : /
#Or : Ok
#Diamant : Ok
#Animaux : Ok


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.event
async def on_member_join(member):
    print (str(member.name) + "have join the server.")
    roleMatelos_id = 640547435445354533 #write id w/o @&
    roleMatelos = discord.utils.get(member.guild.roles, id=roleMatelos_id)
    await member.add_roles(roleMatelos)
    
@bot.command()
async def game(ctx):
    embed = discord.Embed(title="Bienvenue sur [Nom du jeu], pirate!", description="Venez défier la chance et réaliser la meilleure combinaison de dés possible!", color=0x0c1a26)
    embed.add_field(name="Menu", value="**!play** - Tentez votre chance\n**!rules** - Besoin de comprendre les règles?\n**!highscore** - Alors!? C'est qui l'patron?\n**!help** - T'es perdu matelot?", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def play(ctx):    
    players = []
    tmpPlayers = []
    playersScore = []
    tmpPlayersScore = []
    winnerEmojis = ["👑", "👏", "🎉"]
    ready = False
    timeOut = False
    startPlease = False
    endGame= False
    
    msgHere = ''
    
    guild = ctx.message.guild
    msgAuthor = ctx.message.author
    players.append(msgAuthor)
    
    await ctx.send("Ceux qui veulent rejoindre la partie, tapez ?join")
    
    while not ready:
        print ("Recherche de joueurs...")
        try:
            msg = (await bot.wait_for("message", timeout=60.0))
            
        except asyncio.TimeoutError:
            timeOut = True
            print ("timeOut")
        
        else:        
            if msg.content.startswith("?join"):
                if msg.author in players:
                    await ctx.send(msg.author.mention + ", tu fais déjà parti des joueurs.")
                    print (msg.author.name + " est déjà dans la liste")
                    
                else:
                    players.append(msg.author)
                    await ctx.send(msg.author.mention + ", bienvenue à bord, Pirate.")
                    print (msg.author.name + " join the game!")
                    
            if msg.content.startswith("?start"):
                startPlease = True
        
        if len(players) == 5 or startPlease or timeOut:
            if len(players) > 0: #Pour les tests
            # if len(players) > 1:
                print ("Conditions passed!")
                ready = True
                break    # break here
                
            else:
                print ("Conditions NOT passed!")
                break    # break here
            
    if ready:
        print ("On est en dehors du While")
        
        tmpRole = await guild.create_role(name="[NOM DU JEU] - JOUEURS")
        print ("La secte est créé...")
        for player in players:
            await player.add_roles(tmpRole)
            print (player.name + " rejoint la secte.")
            
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.get_role(tmpRole.id): discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        ctx = await guild.create_text_channel('[NOMDUJEU] ENJEU', overwrites=overwrites)
        print ("La création du salon textuel pour le rituel est achevé...")
        
        for player in players:
            msgHere += player.mention + ', '
            
        await ctx.send(msgHere + "vous voici dans le salon de jeu")
        playersNb = len(players)
        random.shuffle(players)     #On mélange les joueurs
        
        #On lance le jeu
        while not endGame:
            print ("Il reste " + str(len(players)) + " joueurs qui n'ont pas encore jouer.")
            if len(players) == 0:
                players = tmpPlayers
                tmpPlayers = []
                print ("Plus assez de joueur... La liste des joueurs est reset!")  

                await ctx.send('#### ##### SCORES DE LA PARTIE ##### ####')
                playersScore = await scoreIG(ctx, players, playersScore)
                await ctx.send(playersScore)
            
            n = 0
            for score in playersScore:
                if score >= 6000:
                    print (players[n].name + " est le grand gagnant de cette arene!")
                    msgWinner = await ctx.send(players[n].mention + ", tu es le premier a atteindre les 6000 points! Tu es le grand vainqueur!")
                    for emoji in winnerEmojis:
                        await msgWinner.add_reaction(emoji)
                    
                    channel = bot.get_channel(613767668096565261) #596020756857749526
                    msgWinnerAll = await channel.send(players[n].name + " vient de gagner à [NOMDUJEU]!")
                    for emoji in winnerEmojis:
                        await msgWinnerAll.add_reaction(emoji)
                    
                    print ("Le combat est terminé")
                    endGame = True
                    break    # break here
                    
                else:
                    n += 1
                    
            if endGame:
                break    # break here
            
            await ctx.send('#### ##### PROCHAIN JOUEUR ##### ####')
            tmpPlayers.append(players[0])    #On le sauvegarde dans une liste temporaire
            
            playerScore = await dice(ctx, players[0])
            playersScore.append(playerScore)
            players.remove(players[0])    #On l'enleve de la liste de base pour passer au joueur suivant!
                    
            if playerScore == -1:
                print ("Le combat est interrompu")
                endGame = True
                break    # break here
        #On stop le jeu
        
        
        try:
            await ctx.send(msgAuthor.mention + ", opération terminé Capitaine. Je remets tout en ordre si vous me l'ordonnez (?reset)")
            msgToReset = (await bot.wait_for("message", timeout=60.0))
            
        except asyncio.TimeoutError:
            print ("timeOut")
            
        else:
            if msgToReset.content.startswith("?reset"):
                await ctx.delete()
                print ("Toutes les preuves du rituel sont supprimées")
                await tmpRole.delete()
                print ("La secte a été supprimé")
        
    else:
        await ctx.send("Ne pars pas seul en mer inconnue " + players[0].mention + "! Trouves toi un équipage et revient vite!")
        print ("Le jeu ne peut pas se lancer...")
        
        

async def dice(ctx, player):
    launch = False
    while not launch:
        try:
            await ctx.send(player.mention + " c'est à toi de jouer!")
            await ctx.send("Utilise la commande ?dice pour commencer ton tour!")
            msg = (await bot.wait_for("message", timeout=60.0))
            
        except asyncio.TimeoutError:
            print (player.name + "est jetté de force dans la fosse aux lions.")
            return 0
            break    # break here
            
        else:
            if msg.content.startswith("?dice"):
                launch = True
                break    # break here
                
            if msg.content.startswith("?stop"):
                return -1
                break    # break here
            
    dicesFace = []
    specialCards = deck
    specialCardsUsed = []
    playerScore = 0
    
    firstThrow = True
    skullIsland = False
    noPoint = False
    
    endOfTurn = False
    
    random.shuffle(specialCards) #On mélange les cartes
    
    
    #PlayerTurn ---------------------------  
    print (player.name + " entre dans l'arene.")
    msgAuthor = player
    
    #PickCard Zone ---------------------------   
    cardPicked = specialCards[-1]
    specialCardsUsed += [cardPicked]
    specialCards.remove(cardPicked)
    
    if len(specialCards) == 0:
        specialCards = specialCardsUsed
        random.shuffle(specialCards) #On mélange les cartes
        specialCardsUsed = []
        
    await ctx.send(msgAuthor.mention + ' La carte que tu as tiré est la carte : ' + cardPicked)
    # if cardPicked == "Pirate":
    #PickCard Zone ---------------------------
    
    while not endOfTurn:
        msgDice = ''
        reactionsEmoji = []
        emojiTDM = ["🖤", "💖", "💛", "💚", "💙", "💜", "💔", "💘"]    
        checkEmoji = '✅'
        tmpEmojisTDM = []
        diceTDM = False
        
        #DiceRoll Zone ---------------------------
        for newDices in range(len(dicesFace), 8):   #On réutilise les champs vides            
            tmpRandomDiceFace = random.choice(diceFaces)
            dicesFace.append(random.choice(tmpRandomDiceFace)) #On ajoute chaque résultat à "dicesFace"
            
            if tmpRandomDiceFace == "💀":
                diceTDM = True
            
        for dices in range(0, 8):            
            if dices == (len(range(0, 8))-1):
                msgDice += 'Dé ' + str(dices+1) + ' : ' + str(dicesFace[dices]) + '.'
            else:
                msgDice += 'Dé ' + str(dices+1) + ' : ' + str(dicesFace[dices]) + ', '
            
            if dicesFace[dices] == "💀":     #Si le dés est une TDM
                tmpEmojiTDM = random.choice(emojiTDM)   #On choisi aléatoirement un des emojis TDM
                tmpEmojisTDM += [tmpEmojiTDM]    #On le sauvegarde dans une liste temporaire
                reactionsEmoji += [tmpEmojiTDM]     #On l'ajoute dans la liste des réactions
                emojiTDM.remove(tmpEmojiTDM)    #On l'enleve de la liste de base pour éviter les doublons
            else:
                reactionsEmoji += ["{}\N{COMBINING ENCLOSING KEYCAP}".format(dices+1)]      #On ajoute l'émoji numéro correspondant au numéro du dé
        #DiceRoll Zone ---------------------------
            
        msg = await ctx.send(msgAuthor.mention + ' Ton résultat est :\n' + msgDice)
        
        #Si carte 1TDM, on ajoute a la liste des dés 1 dé TDM
        if cardPicked == "1TDM":
            dicesFace += ["💀"]
        
        if cardPicked == "2TDM":
            dicesFace += ["💀"]
            dicesFace += ["💀"]
        
        #SkullIsland Zone ---------------------------
        if skullIsland and not diceTDM:
            await ctx.send('Pas de 💀 cette fois, ' + str(dicesFace.count("💀")) + " c'est déjà pas mal!")
            print ('#Fin du tour -- Pas de TDM pendant skullIsland')
            endOfTurn = True  #Fin du tour
            break    # break here
            
        if firstThrow and dicesFace.count("💀") >= 4:    #Si firstThrow et + de 3 TDM
            skullIsland = True 
            await ctx.send("Bienvenue sur l'ile de la mort, fais un maximum de dé 💀 pour faire perdre des points à tes adversaires (1💀 = -100 points). Si tu n'arrives pas à faire au moins 1💀 lors de ton lancer, c'est la fin de ton tour!")
        #SkullIsland Zone ---------------------------
        
        if dicesFace.count("💀") >= 3 and skullIsland == False:   #Si + de 3 TDM
            if cardPicked == "ile":
                await ctx.send('3💀, Tu gardes tes dés mais au suivant!')
                print ('#Fin du tour -- 3+ TDM + Carte ile')
                endOfTurn = True  #Fin du tour
                break    # break here
                
            else:
                await ctx.send('3💀, au suivant!')
                noPoint = True
                print ('#Fin du tour -- 3+ TDM')
                endOfTurn = True  #Fin du tour
                break    # break here
            
        else:   #si - de 3 TDM
            #Si carte TDM, on retire les dés bonus après les calculs
            if cardPicked == "1TDM":
                dicesFace.remove("💀")
                
            if cardPicked == "2TDM":
                dicesFace.remove("💀")
                dicesFace.remove("💀")
            
            reactionsEmoji += [checkEmoji]
            
            for emoji in reactionsEmoji:
                await msg.add_reaction(emoji)
                
            def check(reaction, user):
                return user == msgAuthor and str(reaction.emoji) == checkEmoji
                
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                
            except asyncio.TimeoutError:
                await ctx.send('👎 Trop long!')
                print ('#Fin du tour -- Timeout')
                endOfTurn = True  #Fin du tour
                break    # break here
                
            else:
                await ctx.send('👍 Ton choix est scellé!')
                cache_msg = await ctx.fetch_message(msg.id)
                playerNoReaction = 0
                playerReactions = 0
                diceListNumber = 0
                #Reaction Verification Zone ---------------------------
                for i in cache_msg.reactions:
                    users = await i.users().flatten()
                    if msgAuthor in users:
                        playerNoReaction += 1
                        playerReactions += 1
                        
                    else:
                        if i.emoji in tmpEmojisTDM:
                            playerReactions += 1
                            
                        elif i.emoji == checkEmoji:
                            playerNoReaction += 1
                            playerReactions += 1
                        
                
                print ("playerNoReaction = " + str(playerNoReaction))
                print ("playerReaction = " + str(playerReactions))
                if playerNoReaction == 1 or playerReactions == 9:
                    await ctx.send('Ton tour est validé!')
                    print ('#Fin du tour -- Le joueur a choisi de garder ses dés')
                    endOfTurn = True  #Fin du tour
                    break    # break here
                    
                elif playerReactions > 7:
                    await ctx.send('Ton tour est terminé!')
                    print ('#Fin du tour -- 6+ dés gardés')
                    endOfTurn = True  #Fin du tour
                    break    # break here
                
                else:
                    for i in cache_msg.reactions:                
                        users = await i.users().flatten()
                        if msgAuthor not in users:  #On supprime le dé que "msgAuthor" n'a pas choisi
                            if i.emoji in tmpEmojisTDM: #Sauf si l'émoji est une TDM, dance cas on garde le dé dans la liste
                                diceListNumber += 1
                            elif i.emoji == checkEmoji:
                                diceListNumber += 1
                            else:
                                dicesFace.pop(diceListNumber)
                        
                        else:   #On garde le dé dans la liste
                            diceListNumber += 1
                #Reaction Verification Zone ---------------------------
        
        firstThrow = False
        #On recommence du début
    #PlayerTurn ---------------------------
    
    #print (dicesFace) #Résultat du tour
    
    nbFacesTDM = dicesFace.count("💀")
    nbFacesGold = dicesFace.count("💰")
    nbFacesDiamond = dicesFace.count("💎")
    nbFacesKnife = dicesFace.count("🔪")
    nbFacesMonkey = dicesFace.count("🐵")
    nbFacesBird = dicesFace.count("🐦")
    
    #Si carte Or, + 1 dé or
    if cardPicked == "Or":
        nbFacesGold += 1
    
    #Si carte Diamant, + 1 dé diamant    
    if cardPicked == "Diamant":
        nbFacesDiamond += 1
        
    #Si carte animaux, les dés Birds s'ajoute aux dés Monkey. Le nombre de dé Birds devient 0
    if cardPicked == "Animaux":
        nbFacesMonkey += nbFacesBird
        nbFacesBird = 0
        print ("nbFacesMonkey : " + str(nbFacesMonkey))
    
    if not noPoint and not skullIsland:
        listNbsFaces = [nbFacesGold, nbFacesDiamond, nbFacesKnife, nbFacesMonkey, nbFacesBird]
        
        playerScore += nbFacesGold*100 + nbFacesDiamond*100
        
        for i in listNbsFaces:
            if i < 3:
                playerScore += 0
                
            if i == 3:
                playerScore += 100
                
            if i == 4:
                playerScore += 200
                
            if i == 5:
                playerScore += 500
                
            if i == 6:
                playerScore += 1000
                
            if i == 7:
                playerScore += 2000
                
            if i == 8:
                playerScore += 4000
                
        if nbFacesKnife not in [1,2] and nbFacesMonkey not in [1,2] and nbFacesBird not in [1,2]:
            countFacesWinningPoints = nbFacesGold + nbFacesDiamond + nbFacesKnife + nbFacesMonkey + nbFacesBird
            
        else:
            countFacesWinningPoints = 0
        
        if countFacesWinningPoints==8:
            await ctx.send('Tu as trouvé le coffre au trésor!')
            print ('#Coffre au trésor trouvé')
            playerScore += 500

            
        if cardPicked == "Pirate":
            playerScore = playerScore * 2
                
    elif not noPoint and skullIsland:
        playerScore += nbFacesTDM*100
        
        if cardPicked == "Pirate":
            playerScore = playerScore * 2
            
    await ctx.send('#### ##### SCORE ##### ####')
    await ctx.send('Ton score, pour ce tour, est de : ' + str(playerScore))
    return playerScore
    
    
async def scoreIG(ctx, players, playersScore):
    tmpPlayersScore = []
    for player in range(0, len(players)):
        tmpPlayersScore.append(0)
        
    for k in range(0, len(players)):
        for i in range(k, len(playersScore), len(players)):
            print (i, k, playersScore)
            tmpPlayersScore[k] += playersScore[i]
            
    return tmpPlayersScore

    
@bot.command(pass_context=True)
async def emoji(ctx):
    msg = await ctx.send("working")
    reactions = ['💩']
    for emoji in reactions: 
        await msg.add_reaction(emoji)
        
        
@bot.command(pass_context=True)
async def whoshere(ctx):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name="Gaming", type=discord.ChannelType.voice)
    membersName = voice_channel.members
    
    memberName = []
    memberID = []

    for member in membersName:
        memberName.append(member.display_name)
        memberID.append(member.id)
        
    allMemberName = ', '.join(memberName)
    nbMembers = len(memberName)
    
    if (nbMembers == 0):
        msg = await ctx.send("Nobody here")
        return
    
    elif (nbMembers == 1):
        msg = await ctx.send(allMemberName + " is here")
        
    else:
        msg = await ctx.send(allMemberName + " are here")
    
    await voice_channel.edit(user_limit=nbMembers)
    membersLimit = voice_channel.user_limit


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="<YOUR-USERNAME>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

    embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)

bot.run(TOKEN)  # Where 'TOKEN' is your bot token

# import discord
# from discord.ext import commands
# import random

# TOKEN = 'NjEzMzgyMTAzNzczNjEwMDMz.XVwHnw.N0xp9VfXMGoOSguwAvW7H8t3Y1M'

# client = discord.Client()

# diceFaces = ["Tête-de-mort", "Pièce d'or", "Sabres", "Diamant", "Singe", "Perroquet"]

# class MyClient(discord.Client):
    # async def on_ready(self):
        # print('Logged in as')
        # print(self.user.name)
        # print(self.user.id)
        # print('------')

    # async def on_message(self, message):
        # we do not want the bot to reply to itself
        # if message.author.id == self.user.id:
            # return

        # if message.content.startswith('!hello'):
            # msg = await message.channel.send('Hello {0.author.mention}'.format(message))
            # reactions = ['💩']
            # for emoji in reactions:
                # await msg.add_reaction(emoji)
                
        # if message.content.startswith('!dice'):
            

# client = MyClient()
# client.run(TOKEN)
