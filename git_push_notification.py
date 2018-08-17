import telegram
import git
import time
import datetime
import json
from multiprocessing import Process

def send_msg(token="", chat_id="", path=""):
    bot = telegram.Bot(token=token)
    git_project = git.Git(path)

    while True:
        with open("./out.txt", "a", encoding='utf-8') as log:
            try:
                pull = git_project.pull('origin', 'master')
            except Exception as err:
                log.write("\n[{0}] - {1}".format(str(datetime.datetime.today()), err))
                print("\n[{0}] - {1}".format(str(datetime.datetime.today()), err))
            else:
                if "Updating" in pull:
                    log.write("\n[{0}] - {1}".format(str(datetime.datetime.today()), pull))
                    bot.send_message(chat_id=chat_id, text=git_project.log("-1"))
                    print("\n[{0}] - {1}".format(str(datetime.datetime.today()), pull))
                else:
                    log.write("\n[{0}] - {1}".format(str(datetime.datetime.today()), pull))
        time.sleep(60)

if __name__ == '__main__':
    with open('./settings.json', 'r') as file:
        json_data = json.load(file)

    p = Process(target=send_msg, kwargs=json_data)
    p.start()
    a = p.is_alive()
    p.join()
