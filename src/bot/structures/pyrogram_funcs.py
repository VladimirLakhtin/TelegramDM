import asyncio

from pyrogram import Client
from pyrogram.types import User
from pyrogram.raw.functions.contacts import GetLocated
from pyrogram.raw.types import InputGeoPoint

from config import API_ID, API_HASH, SESSION_NAME


async def send_message(session_name) -> None:
    async with Client(session_name, API_ID, API_HASH) as app:
        await app.send_message("yummy.lvl", "Hey")


async def get_user_info(session_name, username) -> User:
    async with Client(session_name, API_ID, API_HASH) as app:
        return await app.get_users(username)


async def get_nearby_chats(session_name, latitude, longitude):
    async with Client(session_name, API_ID, API_HASH) as app:
        return await app.get_nearby_chats(latitude, longitude)


async def get_chat_members(session_name, chat_id):
    async with Client(session_name, API_ID, API_HASH) as app:
        return [member async for member in app.get_chat_members(chat_id, limit=10)]


async def get_users_nearly(session_name):
    async with Client(session_name, API_ID, API_HASH) as app:
        geo = InputGeoPoint(lat=45.051192, long=39.029169, accuracy_radius=1)
        located = GetLocated(geo_point=geo, self_expires=42)
        return await app.invoke(located)


if __name__ == '__main__':
    LATITUDE = 45.051173
    LONGITUDE = 39.029378
    print(API_ID, API_HASH)
    asyncio.run(get_nearby_chats(SESSION_NAME, latitude=LATITUDE, longitude=LONGITUDE))
