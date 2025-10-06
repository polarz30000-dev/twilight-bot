import discord
from discord.ext import commands

# Configuración del bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal de destino (donde se reenviará la información)
CANAL_DESTINO_ID = 1402819732352270396

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    # Ignorar mensajes del propio bot
    if message.author == bot.user:
        return

    # Verificar si el mensaje tiene embeds (los de Guild Manager sí los tienen)
    if message.embeds and isinstance(message.channel, discord.TextChannel):
        try:
            # Obtener el canal donde se reenviará la información
            canal_destino = bot.get_channel(CANAL_DESTINO_ID)
            if not canal_destino:
                print("❌ No se encontró el canal de destino.")
                return

            # Tomar el primer embed (Guild Manager normalmente envía uno)
            embed_original = message.embeds[0]

            # Crear un nuevo embed similar
            embed_nuevo = discord.Embed(
                title=f"📩 Nuevo ticket detectado en: {message.channel.name}",
                color=discord.Color.blue()
            )

            # Copiar título, descripción y campos del embed original
            if embed_original.title:
                embed_nuevo.add_field(name="Título original", value=embed_original.title, inline=False)
            if embed_original.description:
                embed_nuevo.add_field(name="Descripción", value=embed_original.description, inline=False)

            for field in embed_original.fields:
                embed_nuevo.add_field(name=field.name, value=field.value, inline=field.inline)

            # Añadir información del autor del mensaje (Guild Manager o usuario)
            embed_nuevo.set_footer(text=f"Autor del ticket: {message.author} | ID: {message.author.id}")

            # Enviar el nuevo embed al canal destino
            await canal_destino.send(embed=embed_nuevo)
            print(f"📨 Ticket reenviado desde {message.channel.name} a {canal_destino.name}")

        except Exception as e:
            print(f"⚠️ Error al reenviar el embed: {e}")

    await bot.process_commands(message)

# Ejecutar el bot
bot.run("TOKEN_AQUI")
