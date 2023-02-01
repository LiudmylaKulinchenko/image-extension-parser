import asyncio
from io import BytesIO

import aiohttp
from PIL import Image


async def get_size(row: int, url: str, session: aiohttp.ClientSession):
    """The coroutine gets the image size from the url"""
    if type(url) != str:
        return {row: None}

    async with session.get(url) as response:
        if response.status != 200:
            return {row: "ImageNotFound"}

        content = await response.content.read()
        with Image.open(BytesIO(content)) as image:
            image_size = image.size

    image_size = f"{image_size[0]}x{image_size[1]}"

    return {row: image_size}


async def get_images_sizes(image_urls_: dict):
    """Create an async client and event loop"""
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[
                get_size(image_row, image_url, session)
                for image_row, image_url in image_urls_.items()
            ]
        )


def merge_dicts(list_of_dicts: list) -> dict:
    merged_dict = {}

    for dictionary in list_of_dicts:
        merged_dict.update(dictionary)

    return merged_dict
