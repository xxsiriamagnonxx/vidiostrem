import re 
import os
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from pyyoutube import ytdl

API_ID = os.environ.get("API_ID",12345)
API_HASH = os.environ.get("API_HASH","")
SESSION_NAME = os.environ.get("SESSION_NAME","")
CHAT = os.environ.get("CHAT","")
ADMIN = int(os.environ.get("ADMIN", 1950281200))

app = Client(SESSION_NAME, API_ID, API_HASH)

group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["start"]))
async def start(client, m: Message):
	await m.reply("مرحبًا ابدأ تشغيل الفيديو باستخدام الأمر /play(مع الرد) او /stop لي اقافه")


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["play"]))
async def play(client, m: Message):
	if (m.reply_to_message):
			link = m.reply_to_message.text
			youtube_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
			youtube_regex_match = re.match(youtube_regex, link)
			if youtube_regex_match:
				             try:
				             	video_url = ytdl(link).besturl()
				             except Exception as e:
				             	await m.reply(f"**حدث خطأ** -- `{e}`")
				             	return
				             try:
				             	group_call = group_call_factory.get_group_call()
				             	await group_call.join(CHAT)
				             	await group_call.start_video(video_url,enable_experimental_lip_sync=True)
				             	VIDEO_CALL[CHAT] = group_call
				             	await m.reply("**بدء التشغيل!**")
				             except Exception as e:
				             	await m.reply(f"**حدث خطأ** -- `{e}`")
				             	
					
			else:
			         	try:
			         		group_call = group_call_factory.get_group_call()
			         		await group_call.join(CHAT)
			         		await group_call.start_video(link,enable_experimental_lip_sync=True)
			         		VIDEO_CALL[CHAT] = group_call
			         		await m.reply("**بدء التشغيل!**")
			         	except Exception as e:
			         	    	await m.reply(f"**حدث خطأ** -- `{e}`")
				             	

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["stop"]))
async def stop (client, m: Message):
	try:
	       await VIDEO_CALL[CHAT].stop()
	       await m.reply("**توقف البث!**")
	except Exception as e:
		await m.reply(f"**حدث خطأ** - `{e}`")
