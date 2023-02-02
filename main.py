import asyncio
from datetime import datetime

from image_size import get_images_sizes
from sheet_data import (
    get_image_urls,
    split_urls_into_package,
    update_sheet_size_column
)


def merge_dicts(list_of_dicts: list) -> dict:
    merged_dict = {}

    for dictionary in list_of_dicts:
        merged_dict.update(dictionary)

    return merged_dict


def main():
    dataframe, dataframe_size = get_image_urls()
    get_urls_packs = split_urls_into_package(dataframe, dataframe_size)

    all_sizes_list = []
    for pack in get_urls_packs:
        image_sizes = asyncio.run(get_images_sizes(pack))
        all_sizes_list += image_sizes

    all_sizes = merge_dicts(all_sizes_list)

    update_sheet_size_column(all_sizes)

    return all_sizes


if __name__ == "__main__":
    start = datetime.now()
    main()
    finish = datetime.now()

    print(
        f"Start time: {start.strftime('%H:%M:%S')}\n"
        f"Finish time: {finish.strftime('%H:%M:%S')}\n"
        f"Execution: {(finish - start).total_seconds() * 10 ** 3} ms"
    )
