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

#
# import asyncio
# from aiogram.types import Message
# from aiogram.dispatcher.middlewares.base import BaseMiddleware
# from typing import Callable, Any, Awaitable, Union
#
#
# class AlbumMiddleware(BaseMiddleware):
# 	album_data: dict = {}
#
# 	def __init__(self, latency: Union[int, float] = 0.01):
# 		self.latency = latency
#
# 	async def __call__(
# 					self,
# 					handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
# 					message: Message,
# 					data: dict[str, Any]
# 	) -> Any:
# 		if not message.media_group_id:
# 			await handler(message, data)
# 			return
# 		try:
# 			self.album_data[message.media_group_id].append(message)
# 		except KeyError:
# 			self.album_data[message.media_group_id] = [message]
# 			await asyncio.sleep(self.latency)
#
# 			data['_is_last'] = True
# 			data["album"] = self.album_data[message.media_group_id]
# 			await handler(message, data)
#
# 		if message.media_group_id and data.get("_is_last"):
#
# 			del self.album_data[message.media_group_id]
# 			del data['_is_last']
