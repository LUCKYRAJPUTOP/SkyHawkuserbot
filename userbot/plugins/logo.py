import glob,os,random,time

from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterPhotos

from userbot import *
from SkyhawkBot.utils import admin_cmd
from userbot.cmdhelp import CmdHelp

@bot.on(admin_cmd(pattern="logo ?(.*)"))
async def _(event):
    name = event.pattern_match.group(1)
    if not name:
        await eod(xx, "`Give a Name!`")
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in SkyhawkBot.iter_messages(
            "@bg_for_logos", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
        fpath_ = "SkyHawkuserbot/resources/fonts/"
        f = random.choice(os.listdir(fpath_))
        font_ = fpath_ + f    
    if not bg_:
        pics = []
        async for i in SkyhawkBot.iter_messages(
            "@bg_for_logos", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = random.choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob.glob("SKyHawkuserbot/resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        fnt_size = 150
        strke = 10
    elif len(name) >= 9:
        fnt_size = 50
        strke = 5
    else:
        fnt_size = 130
        strke = 20
    img = Image.open(bg_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text(
        (x, y), name, font=font, fill="white", stroke_width=strke, stroke_fill="black"
    )
    flnme = f"ultd.png"
    img.save(flnme, "png")
    await xx.edit("`Done!`")
    if os.path.exists(flnme):
        tt = time.time()
        up = await uploader(flnme, flnme, tt, xx, "Uploading...")
        await ultroid.send_file(
            event.chat_id,
            file=up,
            caption=f"Logo by [{OWNER_NAME}](tg://user?id={OWNER_ID})",
            foce_document=True,
        )
        os.remove(flnme)
        await xx.delete()
    if os.path.exists(bg_):
        os.remove(bg_)
    if os.path.exists(font_):
        if not font_.startswith("resources/fonts"):
            os.remove(font_)

CmdHelp("logo").add_command(
 'logo', None, 'Make Logo For You'
).add()
