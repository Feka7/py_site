from .models import ThreadTask
import threading
import time
from django_redis import get_redis_connection

def startThreadTask():
    task = ThreadTask()
    task.save()
    t = threading.Thread(target=controllTask,args=[task.id])
    t.setDaemon(True)
    t.start()
    return

def controllTask(id):
    while(True):
        conn = get_redis_connection("default")
        time.sleep(30)
        conn.lpop('news')
    return
