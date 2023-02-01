import asyncio

from image_size import get_images_sizes, merge_dicts
from sheet_data import get_image_urls, split_urls_into_package, update_sheet_size_column


def main():
    df, df_size = get_image_urls()
    get_urls_packs = split_urls_into_package(df, df_size)

    all_sizes_list = []
    for pack in get_urls_packs:
        image_sizes = asyncio.run(get_images_sizes(pack))
        all_sizes_list += image_sizes

    all_sizes = merge_dicts(all_sizes_list)

    update_sheet_size_column(all_sizes)

    return all_sizes


if __name__ == "__main__":
    main()
