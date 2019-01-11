from linebot import LineBotApi
from linebot.models import TextSendMessage
import pymysql

line_bot_api = LineBotApi('IvYpqJR+lpcyxylcpIWrIvWKFZn5G5is/OSTiQnIvZvNz2zuQSPFPnkvqVo0MW3dlVK7auccB32d+PFbPdgHnDAKUuHLoSaVpjW28UIQu/ijUmz2UQ5odoqGGTCNGBPuBz8t66e9eH9+oNkXlmyDVgdB04t89/1O/w1cDnyilFU=')

conn = pymysql.connect('192.168.1.185', 'yudi', '123123', 'db_bot')
cur = conn.cursor()

while True:
    sql = "SELECT * FROM outbox WHERE STATUS = 0 LIMIT 10"
    cur.execute(sql)
    datOutbox = cur.fetchall()
    for row in datOutbox:
        if(row[2] is None):
            print("Terkirim PM")
            line_bot_api.push_message(row[1], TextSendMessage(text=row[4]))
            cur.execute("UPDATE outbox SET status = 1 WHERE id = %s" % (
                row[0]))
            conn.commit()
        else:
            print("Terkirim Grup")
            line_bot_api.push_message(row[2], TextSendMessage(text=row[4]))
            cur.execute("UPDATE outbox SET status = 1 WHERE id = %s" % (
                row[0]))
            conn.commit()

    conn.rollback()