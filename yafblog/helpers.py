import os,math,calendar
from flask import json,jsonify
from datetime import datetime,timedelta,date
from time import mktime

class CacheFile():
    def __init__(self, fname, ftype, finit=[]):
        self.fname = fname
        self.ftype = ftype
        self.finit = finit
        base_dir = os.path.dirname(__file__)
        self.fpath = base_dir+'/caches/'+fname+'.'+ftype

    def read(self):
        if self.ftype == 'json':
            return self.read_json()

    def read_json(self):
        if not os.path.exists(self.fpath):
            self.write_json(self.finit)
        f = open(self.fpath, 'r');
        f.close()
        with open(self.fpath, 'r') as f:
            return json.load(f)

    def write(self, text):
        if self.ftype == 'json':
            return self.write_json(text)

    def write_json(self, text):
        with open(self.fpath, 'w') as f:
            json.dump(text, f)

    def is_exists(self):
        return os.path.exists(self.fpath)

def find_dict_in_list(res, key, val):
    for r in res:
        if r[key] == val or str(r[key]) == str(val):
            return r
    return {}

def list_to_dict(value, key = 'id'):
    d = {}
    if value is not None:
        for v in value:
            d[str(v[key])] = v
    return d

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return datetime.fromtimestamp(value).strftime(format)

def num_to_date(val):
    return val[0:4]+'年'+val[4:]+'月'

def search_list(res, key, val):
    tmp = []
    for r in res:
        if r[key].upper().find(val.upper()) >= 0:
            tmp.append(r)
    return tmp

def month_range():
    today = date.today();
    week, month_days = calendar.monthrange(today.year, today.month)
    month_start = int(mktime(datetime(today.year, today.month, 1).timetuple()))
    month_end = month_start + month_days * 86400 - 1
    return (month_start, month_end)

def week_range():
    today = date.today();
    day_of_week = today.weekday()
    today_stamp = int(mktime(today.timetuple()))
    week_start = today_stamp - day_of_week * 86400
    week_end = today_stamp + (7 - day_of_week) * 86400 - 1
    return (week_start, week_end)

def pages(page, all_num, per_page, url):
    count = math.ceil(all_num / per_page)
    show_page = 4
    page_html = '<ul class="pagination mt-3">'
    if page > 1:
        if page > 2:
            preUrl = url+'?page='+str(page-1)
        else:
            preUrl = url
        page_html += '<li class="page-item"><a class="page-link" href="'+preUrl+'">Previous</a></li>';
    else:
        page_html += '<li class="page-item disabled"><a class="page-link" href="javascript">Previous</a></li>';

    if count <= show_page:
        start = 1
        end = count
    else:
        start = page - int(show_page / 2)
        end = page + int(show_page / 2)
        if start <= 0:
            end = end - start + 1
            start = 1
        if end > count:
            start =  start - end + count
            end = count

    for p in range(start, end + 1):
        if p != 1:
            listUrl = url+'?page='+str(p)
        else:
            listUrl = url
        if p == page:
            page_html += '<li class="page-item active"><a class="page-link" href="javascript:;">'+str(p)+'</a><span class="sr-only">(current)</span></li>'
        else:
            page_html += '<li class="page-item"><a class="page-link" href="'+listUrl+'">'+str(p)+'</a></li>'

    if page < count:
        nextUrl = url+'?page='+str(page+1)
        page_html += '<li class="page-item"><a class="page-link" href="'+nextUrl+'">Next</a></li>'
    else:
        page_html += '<li class="page-item disabled"><a class="page-link" href="javascript:;">Next</a></li>'
    page_html += '</ul>'
    return page_html

