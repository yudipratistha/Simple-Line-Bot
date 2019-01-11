import pymysql
import time

# while True:
#     try:
conn = pymysql.connect('192.168.1.185', 'yudi', '123123', 'db_bot')
cur = conn.cursor()

while True:
    sql = "SELECT * FROM inbox WHERE STATUS = 0 LIMIT 10"
    cur.execute(sql)
    datInbox = cur.fetchall()

    for inbox in datInbox:
        cur.execute("SELECT * FROM kamus WHERE id = '%s'" % (inbox[4]))
        datKamus = cur.fetchone()

        if (datKamus is not None):
            print("data cocok")
            if(inbox[2] is None):
                dataKamus = "Ketik perintah seperi dibawah ini\n" + datKamus[2]
                cur.execute("INSERT INTO outbox VALUES(NULL, '%s', NULL, '%s', '%s', NOW(), NOW(), 0)" % (
                    inbox[1], inbox[3], dataKamus))
                cur.execute("UPDATE inbox SET status = 1 WHERE id = %s" % (
                    inbox[0]))
                conn.commit()

            else:
                cur.execute("INSERT INTO outbox VALUES(NULL, '%s', '%s', '%s', '%s', NOW(), NOW(), 0)" % (
                    inbox[1], inbox[2], inbox[3], datKamus[2]))
                cur.execute("UPDATE inbox SET status = 1 WHERE id = %s" % (
                    inbox[0]))
                conn.commit()
        elif(datKamus is None):
            msg = inbox[4].split(" #") #keyword found

            cur.execute("SELECT * FROM kamus WHERE keyword = '%s'" % msg[0])
            datPencari = cur.fetchone()
            if(datPencari is not None):
                datSplit = datPencari[4]
                i = 0
                for key in msg:
                    if(i != 0):
                        datSplit = datSplit.replace("?", key, 1)
                    i= i+1
                cur.execute(datSplit)
                dataMsg = cur.fetchall()
                if(len(dataMsg) > 0):
                    key = ""
                    for datMsg in dataMsg:
                        i=0
                        for data2 in datMsg:
                            # if(i== 0):
                            #     key = key + str(data2) + ". "
                            # else:
                            #     key = key + str(data2) + " "
                            # i=i+1
                            key = key + str(data2) + "\n"
                        if (dataMsg is not None):
                            key = key + "\n"

                    if (inbox[2] is None):
                        cur.execute("INSERT INTO outbox VALUES(NULL, '%s', NULL, '%s', '%s', NOW(), NOW(), 0)" % (
                            inbox[1], inbox[3], key))
                        cur.execute("UPDATE inbox SET status = 1 WHERE id = %s" % (
                            inbox[0]))
                        conn.commit()
                    else:
                        cur.execute("INSERT INTO outbox VALUES(NULL, '%s', '%s', '%s', '%s', NOW(), NOW(), 0)" % (
                            inbox[1], inbox[2], inbox[3], key))
                        cur.execute("UPDATE inbox SET status = 1 WHERE id = %s" % (
                            inbox[0]))
                        conn.commit()
                else:
                    if (datPencari[5] == "insert"):
                        datatipe = "Data berhasil input"
                    elif (datPencari[5] == "update"):
                        datatipe = "Data berhasil diperbarui"
                    else:
                        datatipe = "Data tidak tersedia"
                    if(inbox[2] is None):
                        cur.execute("INSERT INTO outbox VALUES(NULL, '%s', NULL, '%s', '%s', NOW(), NOW(), 0)" % (
                            inbox[1], inbox[3], datatipe))
                        cur.execute("UPDATE inbox SET status = 1 WHERE id = %s" % (
                            inbox[0]))
                        conn.commit()
                    else:
                        cur.execute("INSERT INTO outbox VALUES(NULL, '%s', '%s', '%s', '%s', NOW(), NOW(), 0)" % (
                            inbox[1], inbox[2], inbox[3], datatipe))
                        cur.execute("UPDATE inbox SET status = 1 WHERE id = %s" % (
                            inbox[0]))
                        conn.commit()
            else:
                print("Tidak ada yg cocok")
                cur.execute("SELECT * FROM kamus")
                datKeyword = cur.fetchall()
                key = "Command yang tersedia\n\n"
                for data in datKeyword:
                    key = key + str(data[0])+"." + " "+ data[1] + "\n"
                if(inbox[2] is None):
                    cur.execute("INSERT INTO outbox VALUES(NULL, '%s', NULL, '%s', '%s', NOW(), NOW(), 0)" % (
                        inbox[1], inbox[3], key))
                else:
                    cur.execute("INSERT INTO outbox VALUES(NULL, '%s', '%s', '%s', '%s', NOW(), NOW(), 0)" % (
                        inbox[1], inbox[2], inbox[3], key))
                cur.execute("UPDATE inbox SET status = 1 WHERE id = %s" % (
                    inbox[0]))
                conn.commit()
    conn.rollback()
    # except Exception as e:
    #     print("Koneksi database ERROR " + str(e))


