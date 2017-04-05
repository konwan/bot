# !/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import logging
import os
# for atom
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from bs4 import BeautifulSoup
from bot import WebBot, BotLog, BOTLOGDIR
from src.lib.util.utils import random_id
from src.lib.util.message import no_data


THR_STATION={"左營站":"f2519629-5973-4d08-913b-479cce78a356",
            "台南站":"9c5ac6ca-ec89-48f8-aab0-41b738cb1814",
            "嘉義站":"60831846-f0e4-47f6-9b5b-46323ebdcef7",
            "雲林站":"5f4c7bb0-c676-4e39-8d3c-f12fc188ee5f",
            "彰化站":"38b8c40b-aef0-4d66-b257-da96ec51620e",
            "台中站":"3301e395-46b8-47aa-aa37-139e15708779",
            "苗栗站":"e8fc2123-2aaf-46ff-ad79-51d4002a1ef3",
            "新竹站":"a7a04c89-900b-4798-95a3-c01c455622f4",
            "桃園站":"fbd828d8-b1da-4b06-a3bd-680cdca4d2cd",
            "板橋站":"e6e26e66-7dc1-458f-b2f3-71ce65fdc95f",
            "台北站":"977abb69-413a-4ccf-a109-0272c24fd490",
            "南港站":"2f940836-cedc-41ef-8e28-c2336ac8fe68",
}


class THR(WebBot):
    log_level = logging.DEBUG
    bot_type = "thr-time"
    browser = "chrome"
    event = random_id()

    def __init__(self, *args, **kwargs):
        super(THR, self).__init__(*args, **kwargs)
        self.src_url = "https://www.thsrc.com.tw/tw/TimeTable/SearchResult"
        self.start_station = "台北站"
        self.end_station = "台中站"
        self.start_time = "17:00"
        self.end_time = ""

    def crawl_data(self):
        try :
            self.botlogger.log("[{}]-{} start crawl data".format(self.__class__.__name__, self.event))
            self.driver.get(self.src_url)
            self.driver.find_element_by_css_selector("#StartStation > option[value='{}']".format(THR_STATION[self.start_station])).click()
            self.driver.find_element_by_css_selector("#EndStation > option[value='{}']".format(THR_STATION[self.end_station])).click()
            self.driver.find_element_by_css_selector("#SearchTime > option[value='{}']".format(self.start_time)).click()
            self.driver.find_element_by_css_selector("#formQuickTimeTableSearch > input").click()
            res = BeautifulSoup(self.driver.page_source, "lxml")
            nexttrip = res.select("#printcontent > section > section.time_check_result.time_check_result_tw > ul > section > table > tbody tr > td > table ")
            self.driver.find_element_by_css_selector("#printcontent > section > section.time_check_result.time_check_result_tw > ul > nav > a.res_prev_btn.res_prev_btn_tw").click()

            res1 = BeautifulSoup(self.driver.page_source, "lxml")
            lasttrip = res1.select("#printcontent > section > section.time_check_result.time_check_result_tw > ul > section > table > tbody tr > td > table ")

            trips = lasttrip[7:] + nexttrip[0:4]
            self.data = ([i.text.strip().split("\n") for i in trips])

        except Exception as e:
            self.driver.save_screenshot("{}/{}_{}.png".format(BOTLOGDIR, self.bot_type, self.event))
            self.botlogger.log("[{}]-{} get data fail".format(self.event, self.__class__.__name__))
        finally:
            self.end_crawler()
            self.result()

    def result(self):
        # ['0133', '13:31', '14:18', '00:47']
        if len(self.data) == 0:
            self.answer = no_data()
        else:
            self.answer = "車次如下：\n出發時間 [*直達車 車次號碼](行駛時間)\n"
            for i in self.data :
                mark = ("*" if ((i[0][0] if(len(i[0]) == 3) else i[0][1])) == "1" else " ")
                self.answer += "{} [{} {}] ({}) \n".format(i[1], mark, i[0], i[3])


class TWR(WebBot):
    log_level = logging.DEBUG
    bot_type = "twr-time"
    browser = "chrome"
    event = random_id()

    def __init__(self, *args, **kwargs):
        super(TWR, self).__init__(*args, **kwargs)
        self.src_url = "http://twtraffic.tra.gov.tw/twrail/"
        self.start_station = "新烏日"
        self.end_station = "斗六"
        self.start_time = "1600"
        self.end_time = "2000"


    def crawl_data(self):
        try :
            self.botlogger.log("[{}]-{} start crawl data".format(self.__class__.__name__, self.event))
            # self.driver.set_window_size(1920,1080)
            self.driver.get(self.src_url)
            if self.driver.find_element_by_css_selector("#dialog"):
                self.driver.find_element_by_css_selector("#dialog > table > tbody > tr > td:nth-of-type(3) > img").click()

            self.driver.switch_to_frame(self.driver.find_element_by_css_selector("#contentframe"))
            self.driver.find_element_by_css_selector("#FromStationInput").send_keys(self.start_station)
            self.driver.find_element_by_css_selector("#ToStationInput").send_keys(self.end_station)
            self.driver.find_element_by_css_selector("#FromTimeSelect > option[value='{}']".format(self.start_time)).click()
            self.driver.find_element_by_css_selector("#ToTimeSelect > option[value='{}']".format(self.end_time)).click()
            self.driver.find_element_by_css_selector("#SearchButton").click()

            res = BeautifulSoup(self.driver.page_source, "lxml")
            raw = res.select("#ResultGridView > tbody > tr")

            for j in raw:
                self.data.append([i.text.strip() for i in j.select("td")])

        except Exception as e:
            self.driver.save_screenshot("{}/{}_{}.png".format(BOTLOGDIR, self.bot_type, self.event))
            self.botlogger.log("[{}]-{}  get data fail".format(self.__class__.__name__, self.event))

        finally:
            self.end_crawler()
            self.result()

    def result(self):
        if len(self.data) == 0:
            self.answer = no_data()
        else:
            self.answer = "車次如下：\n出發時間 [車種] 車次號碼(行駛時間)\n"
            for i in self.data :
                self.answer += "{} [{}] {} ({}) \n".format(i[4], i[0][0], i[1], i[6])


if __name__ == "__main__":
    # print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
    a = THR()
    a.crawl_data()
    print(a.answer)
