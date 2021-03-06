import json
import os
import requests
import re
from datetime import datetime

class CrawlerError(Exception):
    pass


class ReError(CrawlerError):
    pass


def crawler(url):
    page = requests.get(url).content.decode('utf8')
    return page

def get_lectures_XMU(url="https://chem.xmu.edu.cn/xwdt/xshd.htm"):
    """
    Extract lectures from given url using re, return a set of lectures
    """
    context = crawler(url)
    p_lec_title = re.compile("<a title=\"(.*?)\"")
    p_lec_url_id = re.compile("href=\"../info/(.*?).htm\"")
    p_lecturer = re.compile("报告人：(.*?)<")   
    p_lec_time = re.compile("时间：(.*?)<")
    p_lec_loc =  re.compile("地点：(.*?)<")

    lec_titles = p_lec_title.findall(context)
    lec_url_ids = p_lec_url_id.findall(context)
    lecturers = p_lecturer.findall(context)
    lec_times = p_lec_time.findall(context)
    lec_locs = p_lec_loc.findall(context)

    if not (len(lec_titles) == len(lec_url_ids) == len(lecturers) == len(lec_times) == len(lec_locs)):
        print("title\turl\tlecture\ttime\tloc\n{}\t{}\t{}\t{}\t{}".format(len(lec_titles), 
                                                                          len(lec_url_ids), 
                                                                          len(lecturers), 
                                                                          len(lec_times), 
                                                                          len(lec_locs)))
        raise ReError('Captured lectures does not match in dimension')
    
    lectures = set()
    for i, title in enumerate(lec_titles):
        lecture = {}
        lecture['title'] = title
        lecture['lecturer'] = lecturers[i]
        lecture['time'] = lec_times[i]
        lecture['loc'] = lec_locs[i]
        # lecture['url'] = 'http://chem.xmu.edu.cn/showevent.asp?id='+str(lec_url_ids[i])
        lecture['url'] = 'http://chem.xmu.edu.cn/info/'+str(lec_url_ids[i])+'.htm'
        lectures.add(json.dumps(lecture, sort_keys=True, ensure_ascii=False))
    
    return lectures

def save_lectures(lectures, path):
    """
    input: set of lectures, file&directory
    output: json file
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    lectures_output = []
    for lecture in list(lectures):
        lectures_output.append(json.loads(lecture))
    # lectures_output_sorted = sorted(lectures_output, reverse=True, 
    #                                 key=lambda x: datetime.strptime(x['time'], '%Y-%m-%d %H:%M'))
    with open(path, 'w') as fp:
        json.dump(lectures_output, fp, sort_keys=True, ensure_ascii=False, indent=2)

def load_lectures(path):
    """
    load lectures from local josn file
    """
    with open(path, 'r') as fp:
        lectures_input = json.load(fp)
    lectures_local = set()
    for lecture in lectures_input:
        lectures_local.add(json.dumps(lecture, sort_keys=True, ensure_ascii=False))
    return lectures_local
    


if __name__ == '__main__':
    try:
        lectures_local = load_lectures('./data/lectures.json')
    except FileNotFoundError:
        lectures_local = set()
    lectures = get_lectures_XMU()
    # print(lectures)
    #TODO Feed new lecture
    save_lectures(lectures, './data/lectures.json')
    lectures_new = lectures.difference(lectures_local)
    if lectures_new:
        print(lectures_new)
    else:
        print("Lectures up to date.")
