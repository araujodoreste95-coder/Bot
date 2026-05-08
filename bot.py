import discord
from discord.ext import commands, tasks

TOKEN = "OTcwODI3MjIxNTMzMDg5ODcy.GKS2Rp.hBKXyqvjhm6avBNkNxC5o0IKnAw1xMuNyvecJE"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Usuários castigados
usuarios_castigados = set()

# =========================
# BOT ONLINE
# =========================


@bot.event
async def on_ready():
    print(f"{bot.user} online!")
    verificar_calls.start()

# =========================
# COMANDO DE CASTIGO
# =========================


@bot.command()
@commands.has_permissions(administrator=True)
async def castigar(ctx, membro: discord.Member):

    usuarios_castigados.add(membro.id)

    await ctx.send(
        f"{membro.mention} está de castigo e não pode entrar em calls."
    )

# =========================
# REMOVER CASTIGO
# =========================


@bot.command()
@commands.has_permissions(administrator=True)
async def perdoar(ctx, membro: discord.Member):

    usuarios_castigados.discard(membro.id)

    await ctx.send(
        f"{membro.mention} foi perdoado."
    )

# =========================
# LOOP INFINITO
# =========================


@tasks.loop(seconds=1)
async def verificar_calls():

    for guild in bot.guilds:

        for membro in guild.members:

            # Verifica se o usuário está castigado
            if membro.id in usuarios_castigados:

                # Verifica se está em call
                if membro.voice and membro.voice.channel:

                    try:
                        await membro.move_to(None)

                        print(
                            f"{membro} tentou entrar na call e foi removido."
                        )

                    except Exception as erro:
                        print(f"Erro: {erro}")

# =========================
# INICIAR BOT
# =========================

bot.run(TOKEN)
