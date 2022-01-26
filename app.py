import json
import jinja2
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import numpy as np
import pandas as pd
from collections import deque


def sorting_seat(data):
    """梅花座排位

    Args:
        data (dict): 考生分組後dict,格式為 db_to_json.grouping_by_room_id()

    Returns:
        String: 梅花座Table(Html)
    """
    temp_data = data
    room_id = temp_data[0][3]
    room_name = temp_data[0][4]
    row_count = int(temp_data[0][5])
    col_count = int(temp_data[0][6])
    #
    row_index = [i+1 for i in range(row_count)]
    col_index = [f'第{i+1}排' for i in range(col_count)]
    seat_table_df = pd.DataFrame(np.arange(0, col_count*row_count).reshape(
        (col_count, row_count)), columns=[row_index], index=col_index).T
    #
    stud_list = deque()
    for i in temp_data:
        stud_list.appendleft(f'{i[2]}-*-{i[1]}')
    #
    for i in range(row_count*col_count):
        if stud_list:
            if i % 2 == 0:
                seat_table_df.replace(
                    i,
                    stud_list.pop(), inplace=True)
            else:
                seat_table_df.replace(
                    i,
                    '', inplace=True)
        else:
            seat_table_df.replace(
                i,
                '', inplace=True)
    if row_count % 2 == 0:
        for i in range(2, col_count+1, 2):
            seat_table_df[f'第{i}排'] = seat_table_df[f'第{i}排'].shift(1)
    seat_info = f'<div class="d-flex justify-content-between"><div>註：面向講台左邊為第一排</div><div class="seat_info">第{room_id}試場 {room_name} 場地{row_count}x{col_count}</div></div>'
    return seat_info + seat_table_df.to_html(border=0).replace('-*-', '<br>').replace('NaN', '')


app = Flask(__name__)


@app.route('/')
def checkerboard_seating():
    """Flask 根節點

    Returns:
        List: 每一間試場的梅花座Table(Html)
    """
    tables = []
    with open('data.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for i in data:
            tables.append(sorting_seat(data[i]))
    return render_template('index.html', tables=tables)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    

