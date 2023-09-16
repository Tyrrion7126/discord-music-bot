import asyncio
import discord
import wavelink
import Functions
import Embeds
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(intents=intents, command_prefix="x.")
        
    async def on_ready(self) -> None:
        print(f'Logged in as {self.user.name}')
        self.loop.create_task(setup_node())
        
        
bot = Bot()

async def setup_node():
    await bot.wait_until_ready()
    node: wavelink.Node = wavelink.Node(uri="54.38.198.24:88", password="stonemusicgay")
    await wavelink.NodePool.connect(client=bot, nodes=[node])

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node} is ready!")
    
@bot.event
async def on_wavelink_track_end(payload: wavelink.TrackEventPayload):
    ctx = payload.player.ctx
    vc: wavelink.Player = ctx.guild.voice_client
    
    if not vc.queue.is_empty:
        next_song = await vc.queue.get_wait()
        await vc.play(next_song)
        
    else:
        while not vc.is_playing():
            await asyncio.sleep(200)
            if not vc.is_playing() and not vc.is_paused():
                await vc.disconnect()
    
@bot.command(hidden=True)
async def connect(ctx):
    if ctx.voice_client:
        await ctx.send(embed=Embeds.empty(ctx, "Already joined a voice channel."))
        
    else:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await ctx.send(embed=Embeds.empty(ctx, "Joined to your voice channel."))
        
@bot.command(hidden=True)
async def play(ctx, *, track: str):
    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            
    else:
        vc: wavelink.Player = ctx.voice_client
            
    vc.ctx = ctx
    tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(track)
        
    if not tracks:
        await ctx.send(embed=Embeds.no_track(ctx, track))
        return
        
    song: wavelink.YouTubeTrack = tracks[0]
    
    if vc.is_playing() or vc.is_paused():
        await vc.queue.put_wait(song)
        await ctx.send(embed=Embeds.add_track(ctx, song))
        
    else:
        await vc.play(song)
        await ctx.send(embed=Embeds.playnow(ctx, song))
        
@bot.command(hidden=True)
async def queue(ctx):
    vc: wavelink.Player = ctx.voice_client

    if not vc:
        await ctx.send(embed=Embeds.empty(ctx, "No channel are currently joined."))
        
    else:
        if ctx.guild.voice_client.channel != ctx.author.voice.channel:
            await ctx.send(embed=Embeds.empty(ctx, "You need to join to the same channel."))
            
        else:
            if not vc.queue.is_empty:
                await ctx.send(embed=Embeds.queue(ctx, vc))
                
            else:
                await ctx.send(embed=Embeds.empty(ctx, "No queue are currently playing."))

@bot.command(hidden=True)
async def skip(ctx):
    vc: wavelink.Player = ctx.voice_client

    if not vc:
        await ctx.send(embed=Embeds.empty(ctx, "No channel are currently joined."))
        
    else:
        if ctx.guild.voice_client.channel != ctx.author.voice.channel:
            await ctx.send(embed=Embeds.empty(ctx, "You need to join to the same channel."))
            
        else:
            if vc.is_playing():
                await vc.stop()
                await ctx.send(embed=Embeds.skip(ctx, vc))
                
            else:
                await ctx.send(embed=Embeds.empty(ctx, "No music are currently playing."))

@bot.command(hidden=True)
async def pause(ctx):
    vc: wavelink.Player = ctx.voice_client

    if not vc:
        await ctx.send(embed=Embeds.empty(ctx, "No voice channel are currently joined."))
        
    else:
        if ctx.guild.voice_client.channel != ctx.author.voice.channel:
            await ctx.send(embed=Embeds.empty(ctx, "You need to join to the same channel."))
            
        else:
            if vc.is_playing():
                await vc.pause()
                await ctx.send(embed=Embeds.pause(ctx, vc))
                
            else:
                await ctx.send(embed=Embeds.empty(ctx, "No music are currently playing."))

@bot.command(hidden=True)
async def resume(ctx):
    vc: wavelink.Player = ctx.voice_client

    if not vc:
        await ctx.send(embed=Embeds.empty(ctx, "No voice channel are currently joined."))
        
    else:
        if ctx.guild.voice_client.channel != ctx.author.voice.channel:
            await ctx.send(embed=Embeds.empty(ctx, "You need to join to the same channel."))
            
        else:
            if vc.is_paused():
                await vc.resume()
                await ctx.send(embed=Embeds.resume(ctx, vc))
                
            else:
                await ctx.send(embed=Embeds.empty(ctx, "No music are currently playing."))

@bot.command(hidden=True)
async def np(ctx):
    vc: wavelink.Player = ctx.voice_client
    
    if not vc:
        await ctx.send(embed=Embeds.empty(ctx, "No voice channel are currently joined."))
        
    elif ctx.guild.voice_client.channel != ctx.author.voice.channel:
        await ctx.send(embed=Embeds.empty(ctx, "You need to join to the same channel."))
            
    else:
        if vc.is_playing():
            await ctx.send(embed=await Embeds.nowplaying(ctx, vc))
                
        else:
            await ctx.send(embed=Embeds.empty(ctx, "No music are currently playing."))

@bot.command(hidden=True)
async def stop(ctx):
    vc: wavelink.Player = ctx.voice_client
    
    if not vc:
        await ctx.send(embed=Embeds.empty(ctx, "No voice channel are currently joined."))
        
    elif vc.is_playing():
        await vc.disconnect()
        await ctx.send(embed=Embeds.stop(ctx, vc))
        
    else:
        await ctx.send(embed=Embeds.empty(ctx, "No music are currently played."))
    
bot.run("")