# On importe json
import json

# On importe discord.py
import discord

from discord.utils import get

# ajouter un composant de discord.py
from discord.ext import commands

# créer le bot
bot = commands.Bot(command_prefix='!')
warnings = {}

with open('warnings.json', 'r') as infile:
    warnings = json.load(infile)
    print(warnings)


# détecter quand il est prêt ("allumé")
@bot.event
async def on_ready():
    print("Bot Allumée")
    await bot.change_presence(status=discord.Status.online,
                    activity=discord.Game("Aidez les perssone !"))

# détecter quand quelqu'un enleve un emoji du un message
@bot.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji.name
    canal = payload.channel_id
    message = payload.message_id

    python_role = get(bot.get_guild(payload.guild_id).roles, name="[MEMBRE/JOUEUR]")
    membres = bot.get_guild(payload.guild_id).get_member(payload.user_id)

    #vérifier si l'emoji qu'on a ajoutée est "check"
    if canal == 453591163396423680 and message == 473935123922944000 and emoji == "✅":
        print("Grade suprimée")
        await membres.remove_roles(python_role)
        await membres.send("Tu a déclin au règle du serveur acepte les règle et tu pouras t'amuser ! :smiley:")


# détecter quand quelqu'un ajoute un emoji du un message
@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    canal = payload.channel_id
    message = payload.message_id

    python_role = get(bot.get_guild(payload.guild_id).roles, name="[MEMBRE/JOUEUR]")
    membres = bot.get_guild(payload.guild_id).get_member(payload.user_id)

    #vérifier si l'emoji qu'on a ajoutée est "check"
    if canal == 453591163396423680 and message == 473935123922944000 and emoji == "✅":
        print("Grade ajouté")
        await membres.add_roles(python_role)
        await membres.send("Tu a accepter les règle amuse toi bien sur le server :smiley:")

@bot.event
async def on_member_join(ctx):
    await ctx.send("Bienvenue sur le serveur discord oublie pas de accepter le réglement et de faire !regles pour regarder les règles !")

# créer la commande !regles
@bot.command()
async def regles(ctx):
    await ctx.send("Règle : ")
    await ctx.send("Ne pas insulter !")
    await ctx.send("Respecter le staff !")
    await ctx.send("Ne pas afficher d'image trop choquante !")
    await ctx.send("Ne pas spam sinon MUTE 2H !")
    await ctx.send("3 MUTE = Ban de 1 jours")
    await ctx.send("3 Ban = Ban perm")
    await ctx.send("Merci de votre compréhension")


# créer la commande !bienvenue @pseudo
@bot.command()
async def bienvenue(ctx, member: discord.Member):
    # recupere le nom
    pseudo = member.mention
    await ctx.send(f"Bienvenue à {pseudo} sur le serveur discord oublie pas de accepter le réglement et de faire !regles pour regarder les règles !")

# verifier l'erreur
@bienvenue.error
async def on_command_error(ctx, error):
    # detecter l'errreur
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande est : !bienvenue @pseudo")

# créer la commande !warning
@bot.command()
@commands.has_role("[ADMIN]", "SuperModo", "[FONDATEUR]", "Modérateur")
async def warning(ctx, membre: discord.Member):
    pseudo = membre.mention
    id = membre.id


    # si la personne n'a pas de warning
    if id not in warnings:
        warnings[id] = 0
        print("Le membre n'a aucun avertisement")

    warnings[id] += 1
    print("ajout de l'avertissement", warnings[id], "/3")


    # Vérifier le nombre d'avertissement
    if warnings[id] == 3:
        #remet a zero les warnings
        warnings[id] = 0
        #message
        await membre.send("Vous avez était Ban ! Raison : trop d'avertisement")
        # le ban
        await membre.ban()

    # mettre a jour le fichier json
    with open('warnings.json', 'w') as outfile:
        json.dump(warnings, outfile)

    await ctx.send(f"Le joueur {pseudo} a reçu une alerte ! Attention a bien respecter les règle")

@warning.error
async def on_command_error(ctx, error):
    # detecter cette erreur
    if isinstance(error, commands.MissingRequiredArgument):
        # envoyer un message
        await ctx.send("Tu dois faire !warning @pseudo")


# Donner le joton pour qu'il se connecte
jeton = "NzExNjQ3MzUwOTc1ODg5NTE5.XsQ7QQ.5MOwq3QiUO2dqrUAE2rJZhot1Gk"

# Lancement du bot
print("Lancement du bot")

# connecter au serveur
bot.run(jeton)

