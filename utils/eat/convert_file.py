from os import remove

import pandas as pd

TEMP_PATH = 'attachments/eats/temp/'


def edit_exel_file(file: pd.DataFrame) -> pd.DataFrame:
    to_exel = {}
    new_columns = ['brand_id','place_id','brand_name', 'item_id','item_name',
                   'description','weight','calories','proteins','fats','carbohydrates']
    for col in new_columns:
        to_exel[col] = []
    for i in file.values:
        if pd.isna(i[1]): continue
        val_dict = {
            'place_id': int(i[1]),
            'item_id': int(i[2]),
            'item_name': i[3],
            'calories': str(i[4]).split('.')[0] if not pd.isna(i[4]) else '',
            'proteins': str(i[5]).split('.')[0] if not pd.isna(i[5]) else '',
            'fats': str(i[6]).split('.')[0] if not pd.isna(i[6]) else '',
            'carbohydrates': str(i[7]).split('.')[0] if not pd.isna(i[7]) else ''
        }
        for key in to_exel.keys():
            if key in val_dict:
                to_exel[key].append(val_dict[key])
            else:
                to_exel[key].append('')
    return pd.DataFrame(to_exel)


async def convert_file_to_csv(file_path: str, file_name: str) -> bool:
    try:
        data = pd.read_excel(file_path, engine="openpyxl")
        data = edit_exel_file(data)
        data.to_csv(path_or_buf=f'{TEMP_PATH}{file_name}.csv',
                    sep=';',
                    encoding='utf-8-sig',
                    index=False)
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
