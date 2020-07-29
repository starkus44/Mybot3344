import discord
from discord.ext import commands
from discord.utils import get
from discord.utils import get
from discord import utils
from discord.utils import get
import youtube_dl
import os
import datetime

client = commands.Bot( command_prefix = '?' )

client.remove_command( 'help' )

@client.event
async def on_ready():
	print( 'Бот успешно законектился' )
	await client.change_presence( status = discord.Status.online, activity = discord.Game( '🐺Ем тех кто нарушает правила🐺' ) )

@client.command( pass_context = True )

async def hello( ctx, arg ):
	author = ctx.message.author

	await ctx.send( f' { author.mention } Привет я бот написаный игроками Саша12K Wmefilop15 Хомячок' )

#Clear Command
@client.command( pass_context = True)
@commands.has_permissions( administrator = True )

async def clear( ctx, amount = 10000):
	await ctx.channel.purge( limit = amount )

	author = ctx.message.author
	await ctx.send( f'Успешно удалил { author.mention }' )

#kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	await ctx.send( f' Игрок { member.mention } Успешно Кикнут' )
    
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )
async def ban( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )
	await ctx.send( f' Игрок { member.mention } Успешно Забанен' )

# Unban
@client.command( pass_context = True)
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		await ctx.send( f'Игрок { user.mention } Успешно Разбанен')

		return


@client.command( pass_context = True)
async def info(ctx):
   await ctx.send('Список Комманд бота Вульфа написаного игроками Саша12K Wmefilop15 Хомячок')
   await ctx.send("?clear - Очистка чата ")
   await ctx.send("?kick - Удаление участника с сервера ")
   await ctx.send("?ban -  Ограничение доступа к серверу ")
   await ctx.send("?unban - Удаление ограничения доступа к серверу ")
   await ctx.send("?mute - отключить микрофон пользователю  ")
   await ctx.send("?ping - Посмотреть свою скорость интернета")


@client.command()
@commands.has_permissions( administrator = True )

async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'MUTED' )

	await member.add_roles( mute_role )
	await ctx.send( f'Игрок { member.mention } был замучен за нарушение прав' )

@client.event

async def on_member_join( member ):
	channel = client.get_channel( 730347490716549172 )

	role = discord.utils.get( member.guild.roles, id = 729384212188102676 )

	await member.add_roles( role )
	await channel.send( embed = discord.Embed( description = f'Пользователь ``{ member.name }``, Присоединился к нам!', 
		color = 0x0c0c0) ) 

@client.command()
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send(f'Бот Присоединился к каналу: { channel }')

@client.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await connect.channel()
		await ctx.send(f'Бот отключился от канала: { channel }')

@clear.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument):
		await ctx.send( f'{ ctx.author.name }, обязательно укажите аргумент' ) 

#ms command
@client.command(aliases = ['пинг', 'времядосервера'])
async def ping(ctx):
    emb = discord.Embed(title = 'Пинг', description = f'Пинг состовляет {round(client.latency * 1000)}ms', colour = discord.Colour.orange())
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_thumbnail(url='https://media.discordapp.net/attachments/709950747546091641/709956904306081882/-1_Stats.png?width=888&height=856')
    await ctx.send(embed = emb )

@client.command()
async def play(ctx, url : str):
	song_there = os.path.isfile('song.mp3')

	try:
		if song_there:
			os.remove('song.mp3')
			print('[log] Старый Файл Удален')
	except PermissionError:
		print('[log] Не удалось удалить файл')
		
		await ctx.send('Пожалуйста ожидайте')

		voice = get(client.voice_clients, guild = ctx.guild)						

		ydl_opts = {
			'format' : 'bestaudio/best',
			'postprocessors' : [{
				'key' : 'FFmpegExtractAudio',
				'preferredcodec' : 'mp3',
				'preferredquality' : '192'
			}],
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print('[log] Загружаю музыку...')
			ydl.download([url])

		for file in os.listdir('./'):
			if file.endswith('.mp3'):
				name = file
				print('[log] Переименовываю файл: {file}')
				os.rename(file, 'song.mp3')

		voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила своё проигрывание'))
		voice.source = dicsord.PCMVolumeTransformer(voice.source)
		voice.source.volume = 0.07

		song_name = name.rsplit('-', 2)
		await ctx.send(f' Сейчас проигрывает музыка: {song.name[0]}')

@client.command(aliases = ['Fun', 'веселуха'])
async def fun(ctx):
    emb = discord.Embed(title = 'Fun', description = f'Это должно быть смешно ', colour = discord.Colour.green())
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_thumbnail(url='https://media.discordapp.net/attachments/731438950211780669/731498604564578344/image0.png')
    await ctx.send(embed = emb )
    
@client.command(aliases = ['pay'])
async def __pay(ctx, member: discord.Member = None, amount: int = None):
  if member is None:
    await ctx.send(embed = discord.Embed(
      description = f"Укажите пользователя"
      ))
  else:
    if amount is None:
      await ctx.send(embed = discord.Embed(
      description = f"Укажите сумму"
      ))
    elif amount < 1:
      await ctx.send(embed = discord.Embed(
      description = f"Сумма не может быть меньше 1"
      ))
    elif member.id == ctx.author.id:
      await ctx.send(embed = discord.Embed(
      description = f"Вы не можете отправить деньги самому себе"
      ))
    else:
      if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.message.author.id)).fetchone()[0] < amount :
        await ctx.send(embed = discord.Embed(
      description = f"У вас недостаточно средств"
      ))
      else:
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
        cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
        connection.commit()
        await ctx.send(embed = discord.Embed(
        description = f"Успешно переведено **{amount}** :dollar:"
        ))

@client.command(aliases = ['Твои', 'Коины'])
async def stats(ctx):
    emb = discord.Embed(title = 'Твои Коины', description = f'Недаработано', colour = discord.Colour.green())
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_thumbnail(url='https://media.discordapp.net/attachments/730152962147614750/735117575364804698/OIP.png')
    await ctx.send(embed = emb )

@client.command(aliases = ['Помянем', 'Его'])
async def bb(ctx):
    emb = discord.Embed(title = 'Я', description = f'Твою мать в кино водил', colour = discord.Colour.orange())
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_thumbnail(url='https://media.discordapp.net/attachments/730152962147614750/735117575364804698/OIP.png')
    await ctx.send(embed = emb )

# Get token
token = open( 'token.txt', 'r' ).readline()     

client.run( token )
