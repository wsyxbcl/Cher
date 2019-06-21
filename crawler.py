import json
import requests
import re


class CrawlerError(Exception):
    pass

class ReError(CrawlerError):
    pass


def crawler(url):
    page = requests.get(url).content.decode('utf8')
    return page

def get_lectures_XMU(url="http://chem.xmu.edu.cn/eventlist.asp"):
    """
    Extract lectures from given url using re, return a set of lectures
    """
    context = crawler(url)
    p_lec_title = re.compile("<a   title=\'(.*?)\'")
    p_lecturer = re.compile("报告人：(.*?)<")
    p_lec_time = re.compile("时间：(.*?)<")
    p_lec_loc =  re.compile("地点：(.*?)<")

    lec_titles = p_lec_title.findall(context)
    lecturers = p_lecturer.findall(context)
    lec_times = p_lec_time.findall(context)
    lec_locs = p_lec_loc.findall(context)

    if not (len(lec_titles) == len(lecturers) == len(lec_times) == len(lec_locs)):
        raise ReError('Captured lectures does not match in dimension')
    
    lectures = set()
    for i, title in enumerate(lec_titles):
        lecture = {}
        lecture['title'] = title
        lecture['lecturer'] = lecturers[i]
        lecture['time'] = lec_times[i]
        lecture['loc'] = lec_locs[i]

        lectures.add(json.dumps(lecture, sort_keys=True, ensure_ascii=False))
    
    return lectures

if __name__ == '__main__':
    lectures = get_lectures_XMU()
    print(lectures)
    #TODO Saving & Updating & Feed new lecture




