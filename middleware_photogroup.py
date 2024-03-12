from typing import Any, Dict, Union
import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: Union[int, float] = 0.1):
        self.latency = latency
        self.album_data = {}

    async def __call__(self, handler, event: Message, data: Dict[str, Any]) -> Any:
        if not event.media_group_id:
            data["album"] = [
                event]  # ---- > это моя попытка добавить одну фотку в альбом при проверке. но что-то пошло не так)
            return await handler(event, data)
        total_before = self.collect_album_message(event)

        await asyncio.sleep(self.latency)
        total_after = len(self.album_data[event.media_group_id]["messages"])
        if total_before != total_after:
            return

        album_messages = self.album_data[event.media_group_id]["messages"]
        album_messages.sort(key=lambda x: x.message_id)
        data["album"] = album_messages

        await handler(event, data)
        del self.album_data[event.media_group_id]

    def collect_album_message(self, event: Message):
        if event.media_group_id not in self.album_data:
            self.album_data[event.media_group_id] = {"messages": []}
        self.album_data[event.media_group_id]["messages"].append(event)
        return len(self.album_data[event.media_group_id]["messages"])
