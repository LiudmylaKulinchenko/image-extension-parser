import asyncio
from io import BytesIO

import aiohttp
from PIL import Image


async def fetch_image_data(url: str, session: aiohttp.ClientSession):
    """Fetch image data from the URL using the provided session"""
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.content.read()


async def process_image(content) -> str:
    """Process image content to get its size."""
    try:
        with Image.open(BytesIO(content)) as image:
            return f"{image.size[0]}x{image.size[1]}"
    except Image.UnidentifiedImageError:
        return "InvalidImage"


async def get_size(sem: asyncio.Semaphore, row: int, url: str, session: aiohttp.ClientSession):
    """The coroutine gets the image size from the url"""
    if type(url) != str:
        return {row: None}

    retries = 3

    for attempt in range(retries):
        try:
            async with sem:
                content = await fetch_image_data(url, session)
                image_size = await process_image(content)

            return {row: image_size}

        except aiohttp.ClientError as e:
            if e != aiohttp.HTTPNotFound and attempt < retries - 1:
                print(f"Retries {attempt} time for {url} from {row} row")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Failed to fetch {url} from {row} row after {retries} attempts: {e}")
                return {row: "ImageNotFound"}


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
