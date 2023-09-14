from os import remove

import pandas as pd

TEMP_PATH = 'attachments/eats/temp/'

async def convert_file_to_csv(file_path: str, file_name: str) -> bool:
    try:
        data = pd.read_excel(file_path, engine="openpyxl")
        data.to_csv(path_or_buf=f'{TEMP_PATH}{file_name}.csv',
                    sep=';',
                    encoding='utf-8-sig')
        return True
    except Exception as err:
        print(err)
        return False


def delete_temp_file(path_file: str) -> bool:
    try:
        remove(path_file)
        return True
    except Exception as err:
        print(err)
        return False