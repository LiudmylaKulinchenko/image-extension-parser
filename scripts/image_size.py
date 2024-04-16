import asyncio
from io import BytesIO

import aiohttp
import pandas as pd
from PIL import Image

from logger_setup import logger


async def process_image(content: bytes) -> str:
    """Process image content to get its size."""
    try:
        with Image.open(BytesIO(content)) as image:
            return f"{image.size[0]}x{image.size[1]}"
    except Image.UnidentifiedImageError:
        logger.warning("InvalidImage error while processing image")
        return "InvalidImage"


async def get_size(
    sem: asyncio.Semaphore, row: int, url: str, session: aiohttp.ClientSession
):
    """The coroutine gets the image size from the url"""
    if pd.isna(url):
        return {row: "UrlNotProvided"}

    async with sem:
        async with session.get(url) as response:
            if response.status != 200:
                return {row: "ImageNotFound"}

            content = await response.content.read()

        image_size = await process_image(content)

    return {row: image_size}


async def get_images_sizes(image_urls_: dict):
    """Create an async client and event loop"""
    sem = asyncio.Semaphore(20)

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[
                get_size(sem, image_row, image_url, session)
                for image_row, image_url in image_urls_.items()
            ]
        )
