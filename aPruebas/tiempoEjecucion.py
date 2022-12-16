import time
import datetime

start = time.time()

time.sleep(100)

end = time.time()

sec = round(end - start)
tiempo = str(datetime.timedelta(seconds=sec))
print(tiempo)


