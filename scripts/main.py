import asyncio
import logging
from datetime import datetime

from image_size import get_images_sizes
from sheet_data import (
    get_image_urls,
    split_urls_into_package,
    create_excel_file_with_image_sizes,
)


logging.basicConfig(
    filename="../logs/main.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(name)s - %(levelname)s - %(message)s",
)


def merge_dicts(list_of_dicts: list) -> dict:
    merged_dict = {}

    for dictionary in list_of_dicts:
        merged_dict.update(dictionary)

    return merged_dict


def main():
    images_df, df_size = get_image_urls()
    get_urls_packs = split_urls_into_package(images_df, df_size)

    all_sizes_list = []
    pack_number = 1
    for pack in get_urls_packs:
        logging.info(f"Start asynchronous collection of image sizes for pack {pack}")
        image_sizes = asyncio.run(get_images_sizes(pack))
        logging.info(f"Successfull finish getting image sizes for pack {pack}")
        all_sizes_list += image_sizes
        pack_number += 1

    all_sizes = merge_dicts(all_sizes_list)

    create_excel_file_with_image_sizes(all_sizes)


if __name__ == "__main__":
    start = datetime.now()
    main()
    finish = datetime.now()

    logging.info(
        f"Start time: {start.strftime('%H:%M:%S')}\n"
        f"Finish time: {finish.strftime('%H:%M:%S')}\n"
        f"Execution: {(finish - start).total_seconds() * 10 ** 3} ms"
    )
