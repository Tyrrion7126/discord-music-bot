import wavelink
import discord
import Functions
from discord import Embed as em

blue = discord.Color.blurple()
    
def empty(ctx, content):
    e = em(description=content, colour=blue)
    return e
    
def no_track(ctx, query):
    e = em(title="Not found", description=f"No track found matching your query: **{query}**", colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
        
    return e
    
def playnow(ctx, song):
    e = em(title="Started playing", description=f"**[{song.title}]({song.uri})**", colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)

    return e
    
def add_track(ctx, song):
    e = em(title="Track added", description=f"Added **[{song.title}]({song.uri})** to queue.", colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
    
    return e
    
async def nowplaying(ctx, vc: wavelink.Player):
    song = vc.current
    e = em(title="Now playing", description=f"**[{song.title}]({song.uri})**", colour=blue)
    e.set_thumbnail(url=await song.fetch_thumbnail())
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
    
    return e
    
def queue(ctx, vc: wavelink.Player):
    e = em(title="Songs queue", description="\n".join([f"- [{song.title}]({song.uri})" for song in vc.queue]), colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
    
    return e
    
def pause(ctx, vc: wavelink.Player):
    e = em(title="Songs paused", description=f"**[{vc.current.title}]({vc.current.uri})** now paused, use **resume** to resume song.", colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
    
    return e

def resume(ctx, vc: wavelink.Player):
    e = em(title="Songs resumed", description="Your current songs now resumed!.", colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
    
    return e

def stop(ctx, vc: wavelink.Player):
    e = em(title="Stop", description="Stopped the player, thank you for using, leaving now.", colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
    
    return e

def skip(ctx, vc: wavelink.Player):
    e = em(title="Skip", description=f"Skipped **[{vc.current.title}]({vc.current.uri})** to the next song.", colour=blue)
    e.set_footer(text=Functions.userName(ctx), icon_url=ctx.author.display_avatar)
    
    return e

"""def error(ctx, vc: wavelink.Player):
    e = em(title="Error")
    e.set_footer(text=ctx.author.name + ctx.author.discriminator)
    return e"""
