import configparser
import pymysql
import json
import pandas as pd
import datetime


def main():

    console_format("Read setting")
    config = configparser.ConfigParser()
    config.read("config.ini")
    console_format("Connect to server")
    db = pymysql.connect(host=config['DEFAULT']['DB_HOST'],
                         user=config['DEFAULT']['DB_USERNAME'],
                         password=config['DEFAULT']['DB_PW'],
                         db=config['DEFAULT']['DB_NAME'],
                         cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()
    console_format("Fetch data")
    cursor.execute("SELECT * FROM `tbl_monitor_data`")

    result = cursor.fetchall()
    db.close()
    console_format("Processing...")

    table = list()
    for row in result:
        temp_datas = json.loads(row['Datas'])
        for key in temp_datas:
            row[key] = temp_datas[key]
        row.pop('Datas')
        table.append(row)

    df = pd.DataFrame(table)
    df.to_excel("output.xlsx", index=False)
    console_format("OK!")


def console_format(message):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))


if __name__ == "__main__":
    main()
