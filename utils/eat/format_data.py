

async def create_data_for_display(data: list[dict[str, str]]) -> str:
    format_str = ''
    for i in range(len(data)):
        format_str += f'{i + 1}) {data[i]["or_file_name"]} -> ' \
                      f'{data[i]["final_file_name"]} ' \
                      f'[{str(data[i]["created_on"]).split(".")[0]}]\n\n'
    return format_str