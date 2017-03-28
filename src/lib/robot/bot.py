# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
# logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s")
import os
import sys
import random
from datetime import datetime
from selenium import webdriver

# for atom use
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# from hibot.src.lib.util.utils import random_id
from src.lib.util.utils import random_id

####################################################################
# 1. time (thr/train)
# 2. invest (gold/ex/stock)
# 3. map (according to geo data(in 5 km) git top 5 bus/ food/ tour)
# 4. big (top 5 tech, society, novel, movie)
# 5. chat (sweet heart)
####################################################################


# '/Users/data/Desktop/cindy/hibot'
BOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
BOTLOGDIR =  "{}/log".format(BOTDIR)
BOTDRIVERDIR =  "{}/src/etc/driver".format(BOTDIR)
BOTDATADIR =  "{}/data".format(BOTDIR)

LOGGER = "botlog"
CHROME_DRIVER = "{}/chrome/mac64/chromedriver".format(BOTDRIVERDIR)
PHANTOMJS_DRIVER = "{}/phantomjs/mac64/phantomjs-2.1.1/bin/phantomjs".format(BOTDRIVERDIR)
WEBAGENT = "Mozilla/{x}.0 (Macintosh; Intel Mac OS X 10.9; rv:{x}.0) Firefox/{x}.0".format(x=random.randint(0,30))

class EMBot(object):
    # 1. time (thr/train)
    # 2. invest (gold/ex/stock)
    # 3. map (according to geo data(in 5 km) git top 5 bus/ food/ tour)
    # 4. big (top 5 tech, society, novel, movie)
    # 5. chat (sweet heart)

    log_level = logging.DEBUG
    bot_type = "time" # ['time', 'chat', 'big', 'invest', 'map']
    event = random_id()

    def __init__(self):
        self.botlogger = BotLog(self.log_level, self.bot_type)
        self.start()

    def start(self):
        self.botlogger.log("{} start bot".format(self.event))

    def job(self):
        self.botlogger.log("job {}".format(BOTDATADIR))

    def end(self):
        self.botlogger.log("end bot")

    def trace(self):
        pass

class Bot(object):
    log_level = logging.DEBUG
    bot_type = "time" # ['time', 'chat', 'big', 'invest', 'map']
    browser = "phantomjs" #['phantomjs', 'chrome']
    event = random_id()

    def __init__(self):
        self.src_url = ""
        self.botlogger = BotLog(self.log_level, self.bot_type)

        if self.browser == "phantomjs":
            self.driver = webdriver.PhantomJS(PHANTOMJS_DRIVER)
        else:
            self.driver = webdriver.Chrome(CHROME_DRIVER)
        self.start()

    def start(self):
        self.botlogger.log("start bot")

    def job(self):
        self.botlogger.log("job {}".format(BOTDATADIR))

    def end(self):
        self.botlogger.log("end bot")

    def trace(self):
        pass


class BotLog(object):
    LOG_TYPE = [logging.INFO,logging.WARNING,logging.ERROR,logging.CRITICAL,logging.DEBUG]
    LOG = logging.getLogger(LOGGER)
    FOMATTER = logging.Formatter('%(asctime)s  [%(name)s] [%(levelname)s] - %(message)s')

    def __init__(self, level, bot_type):
        self.level = level
        self.path = "{}/{}_{}.log".format(BOTLOGDIR, LOGGER, bot_type)
        self.HANDLER = logging.FileHandler(self.path)
        self.start()

    def start(self):
        self.HANDLER.setFormatter(self.FOMATTER)
        self.LOG.addHandler(self.HANDLER)
        self.LOG.setLevel(self.level)

    def log(self, msg):
        self.LOG.log(self.level, msg)
        # self.LOG.log(40, datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f ")[:-3] + msg)


if __name__ == "__main__":
    # a = BotLog(logging.INFO, 'time')
    # a.log(" oh yap  ")
    b = Bot()
    print(b.event)
    # b.start()
    # b.crawl_data()
    # b.end()
