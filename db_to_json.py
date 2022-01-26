from os import getenv
import json
import pymssql
from dotenv import load_dotenv
load_dotenv()


sql_string = f"SELECT stuDataTable.stuId, stuDataTable.stuName, stuData2Table.grantNo,  roomIdTable.roomId, \
    roomIdTable.roomName, roomIdTable.maxRow, roomIdTable.maxColumn \
    FROM stuDataTable \
    INNER JOIN stuData2Table ON stuDataTable.idNo = stuData2Table.idNo \
    INNER JOIN roomIdTable ON roomIdTable.grantNo = stuData2Table.grantNo     \
    ORDER BY  CAST(roomIdTable.roomId AS int), grantNo"


def connect_db():
    """DB連線

    Returns:
        connect: 連線物件
    """
    try:
        server = getenv("PYMSSQL_TEST_SERVER")
        user = getenv("PYMSSQL_TEST_USERNAME")
        password = getenv("PYMSSQL_TEST_PASSWORD")
        db = getenv("PYMSSQL_TEST_DB")
        conn = pymssql.connect(server, user, password, db,)
        return conn
    except pymssql.OperationalError as e:
        raise


def grouping_by_room_id():
    """考生以考場號碼分組

    Returns:
        dict: 分組後dict物件
    """
    grouping ={}
    stud_list = []
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql_string)
    row = cursor.fetchone()
    group_room_id = row[3].strip()
    cursor.execute(sql_string)
    rows = cursor.fetchall()
    for row in rows:
        room_id = row[3].strip()
        if group_room_id != room_id:
            grouping[group_room_id] = stud_list
            group_room_id = room_id
            stud_list = []
        new_row = [str(i).strip() for i in row]
        stud_list.append(new_row)
    with open("data.json", "w", encoding='utf8') as a_file:
        json.dump(grouping, a_file, ensure_ascii=False)
        a_file.close()
    return grouping

if __name__ == '__main__':
    grouping_by_room_id()
    