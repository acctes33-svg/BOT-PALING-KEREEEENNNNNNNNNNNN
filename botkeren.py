import discord
from discord.ext import commands
from bot_logic import gen_pass
import random, os
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def passgen(ctx, pass_length = 10):
    await ctx.send(gen_pass(pass_length))

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
   # Kita kemudian dapat mengirim file ini sebagai tolok ukur!
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

def get_anime_image_url(keyword):
    url = f"https://kitsu.io/api/edge/anime?filter[text]={keyword}"
    res = requests.get(url)
    data = res.json()
    all_anime_url = [item['attributes']['posterImage']['original'] for item in data['data']]
    anime_url = random.choice(all_anime_url)

    return anime_url

@bot.command('anime_img')
async def anime_img(ctx, keyword:str):
    '''Setelah kita memanggil perintah anime, program akan memanggil fungsi get_anime_image_url'''
    anime_url = get_anime_image_url(keyword)
    await ctx.send(anime_url)

def get_tips(how_many):
    tips_for_teen = [
        "Cobalah untuk menghindari penggunaan barang sekali pakai, seperti gelas dan botol plastik",
        "Pindah ke e-reader untuk mengurangi konsumsi kertas",
        "Pilih produk bahan makanan dan makanan ringan dengan kemasan sesedikit mungkin, beli makanan berdasarkan beratnya (tanpa kemasan), dan cobalah beralih ke tas yang dapat digunakan kembali",
        "jalan kaki jika jarak perjalanan dekat",

    ]

    return random.sample(tips_for_teen, k=how_many)

@bot.command('tipsteen')
async def tipsteen(ctx, howmany:int):
    all_tips = get_tips(howmany)
    sent_tips = '\n'.join(all_tips)
    await ctx.send(sent_tips)

def get_waste_type(waste):
    #standarisasi inputan
    waste = waste.lower().strip()
    non_recyclable_waste = ["food scraps", "dirty tissue", "diaper", "cigarette butt", "styrofoam"]
    recyclable_waste = ["plastic bottle", "plastic cup", "glass bottle", "newspaper", "cardboard", "can"]

    if waste in recyclable_waste:
        return "sampah ini bisa di daur ulang"
    elif waste in non_recyclable_waste:
        return "sampah ini tidak bisa didaaur ulang" 
    else:
        return "seperti nya ini bukan dua duanya"

@bot.command('type')
async def waste_type(ctx, *, waste:str):
    type_waste = get_waste_type(waste)

    await ctx.send(type_waste)
# cara panggil comman -> $passgen 10
bot.run("ISI TOKEN BOT MU")
