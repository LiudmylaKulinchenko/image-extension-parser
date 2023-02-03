import pandas as pd

SHEET_ID = "1QX2IhFyYmGDFMvovw2WFz3wAT4piAZ_8hi5Lzp7LjV0"
SHEET_NAME = "feed"
NEW_SHEET_FILE = "Parser_ImageSize.xlsx"
COLUMN_NAME = "SIZE"


def get_sheet_data() -> pd.DataFrame:
    """Upload data from sheet"""
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    )
    dataframe = pd.read_csv(url)

    return dataframe


def get_image_urls() -> tuple[pd.DataFrame, int]:
    """Return tuple with DataFrame of image_urls and DataFrame size"""
    dataframe = get_sheet_data()
    image_urls_dataframe = dataframe["image_url"][1:]
    dataframe_size = image_urls_dataframe.size

    return image_urls_dataframe, dataframe_size


def split_urls_into_package(dataframe: pd.DataFrame, size: int) -> dict:
    """
    The generator divides the urls into dictionaries (packs) <= 10_000 each
    """
    pack_size = 10_000
    packs_amount = size // pack_size + 1

    for i in range(packs_amount):
        yield dataframe[pack_size * i:pack_size * (i + 1)].to_dict()

    return dataframe[pack_size * packs_amount:].to_dict()


def update_sheet_size_column(sizes: dict):
    """Update size column with new data"""
    data = get_sheet_data()
    sizes_list = list(sizes.values())
    new_data = pd.DataFrame({COLUMN_NAME: sizes_list})
    data.update(new_data)

    with pd.ExcelWriter(NEW_SHEET_FILE, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name=SHEET_NAME, index=False)
