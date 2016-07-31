import urllib
import urllib.request
import urllib.parse
import bs4
import re
import pandas as pd
import json
import datetime as dt

today = dt.date.today()
prev = today - dt.timedelta(days=90)

def cleanText(text):
	return text.replace('\t', '').replace('\n', '').replace('\r', '').strip()


key = "412fe4ee301602a5cb5685ae2b6db230e531588e"
API_URL = "http://dart.fss.or.kr/api/search.json?auth="
API_URL = API_URL + key
#option = "dsp_tp=I&bsn_tp=I002&page_set=100page_no=1"
def GetList(page):
	options = {
		"dsp_tp": "I",
		"bsn_tp": "I002",
		"page_set": "100",
		"page_no": page,
		"start_dt": prev.strftime("%Y%m%d")
	}
	data = urllib.parse.urlencode(options)
	data = data.encode(encoding='ascii')
	REQ = urllib.request.Request(API_URL, data)
	HTML = urllib.request.urlopen(REQ)
	HTML= HTML.read().decode('utf-8')
	HTML = json.loads(HTML)

	HowManyPages = HTML['total_page']
	Contents = HTML['list']
	Companies = []
	Titles = []
	Dates = []
	Links = []
	for x in Contents:
		Companies.append(x['crp_nm'])
		Titles.append(x['rpt_nm'])
		Dates.append(int(x['rcp_dt']))
		Links.append(x['rcp_no'])
	Links = ["http://dart.fss.or.kr/dsaf001/main.do?rcpNo=" + x for x in Links]
	df = pd.DataFrame({"GenerateDate": Dates, "Companies": Companies, "Titles": Titles, "Links": Links})
	df = df[df.Titles.str.contains("영업")]
	return HowManyPages, df

HowManyPages, df = GetList(1)
#f, df2 = GetList(2)
print(HowManyPages)

if int(HowManyPages) > 1:
	for x in range(2, 2 + int(HowManyPages) - 1):
		print(x)
		t, temp = GetList(x)
		df = df.append(temp, ignore_index = True)

df[['GenerateDate', 'Companies', 'Titles', 'Links']].to_csv("result.csv", index=False)