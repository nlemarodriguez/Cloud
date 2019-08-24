from datetime import datetime
import time

while True:
    f = open("./logs/log", "a+")
    now = datetime.now()
    f.write("Hora: %a \r\n" % now.strftime("%d/%m/%Y %H:%M:%S"))
    f.close()
    time.sleep(5)
