# ����ʵ��
|ѧУ|רҵ|����|��ϵ��ʽ|
|:-------:|:-------------: | :----------:|:-------------: |
|�ɶ���ѧ|�������(��)15-2|���|18990051970|
## 1. �����̳�-�ֻ�ҳ��ͼƬ��ȡ
### 1.1 Դ�����£�

``` class
import requests
from bs4 import BeautifulSoup
import re
from hashlib import md5
from requests.exceptions import RequestException
from multiprocessing import Pool
import sys
import os

def get_index(offset):
	headers = {
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36'
	}
	url = "https://list.jd.com/list.html?cat=9987,653,655&page="+offset
	html = requests.get(url, headers=headers)
	# ��ȡ����������Ʒ��div
	soup = BeautifulSoup(html.content, 'lxml')
	a = soup.find_all("div",class_="p-img")
	# ��bs4�Ľ����ת��Ϊ�ַ���
	a = str(a)
	# ����������ʽ��ȡ
	pattern = r'<a href="(.*?)" target="_blank">'
	res = re.compile(pattern, re.S)
	results = re.findall(res, a)
	for result in results:
		yield result


def get_page(url):
	# �����ֻ�ҳ����ȡͼƬ
	headers = {
		'User - Agent':'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 63.0.3236.0Safari / 537.36'
	}
	url = 'https:'+url
	html = requests.get(url, headers=headers)
	soup = BeautifulSoup(html.content, 'lxml')
	a = soup.find_all("div", class_="spec-items")
	a = str(a)
	pattern = 'src="(.*?)n5/.*?" data-url="(.*?)"'
	res = re.compile(pattern, re.S)
	result = re.findall(res, a)
	for i in result:
		yield 'http:'+i[0]+'n1/s450x450_'+i[1]

def download_pic(url):
	headers = {
		'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
	'Accept - Encoding': 'gzip, deflate',
	'Accept - Language': 'zh - CN, zh;',
	'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 63.0.3236.0Safari / 537.36'
	}
	try:
		html = requests.get(url, headers=headers)
		content = html.content
		print(url)
		print(html.status_code)
		if html.status_code == 200:
			file_path = "{0}/{1}/{2}.{3}".format(sys.path[0], 'iphone', md5(content).hexdigest(), 'jpg')
			if not os.path.exists(file_path):
				with open(file_path, 'wb') as f:
					f.write(content)
					f.close()
			return 1
	except RequestException:
		print('����ͼƬʧ��', url)
		return None

def main(offset):
	for  url in get_index(offset):
		for image_url in get_page(url):
			download_pic(image_url)

if __name__ == '__main__':
	groups = [str(x) for x in range(1,60)]
	pool = Pool()
	pool.map(main, groups)

```

### 1.2 ץȡ�����ͼ��


![class](jdSpider.PNG)



## 2. mzitu��վ��Ƭ��ȡ

### 2.1 Դ�����£�

```class 
import requests
from bs4 import BeautifulSoup
import sys
import os
from hashlib import md5
from requests.exceptions import RequestException
from multiprocessing import Pool


'''
	��ȡ����ͼ(http://www.mzitu.com/page/)������ͼ
'''

# ��ȡ�ȵ�ͼ��ÿһҳ����ͼ������
def get_url(offset):
	url = "http://www.mzitu.com/page/" + str(offset)
	headers = {
		'Cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c = 1523859284, 1524038568;Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c = 1524038865',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36'
	}
	html = requests.get(url, headers=headers)
	soup = BeautifulSoup(html.content, 'lxml')
	bs = soup.select('ul[id="pins"] a')
	for item in bs:
		yield item.get('href')

# �õ�ÿһ����ͼ�����ҳ��,�����ϳ����ӷ���get_page_index
def get_maxpage(url):
	headers = {
		'Cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c = 1523859284, 1524038568;Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c = 1524038865',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36'
	}
	html = requests.get(url, headers=headers)
	bs = BeautifulSoup(html.content, 'lxml')
	# ��ȡÿһ��ͼ�׵����ҳ��
	max_page = (bs.select('div[class="pagenavi"] a span'))[-2].text
	for i in range(1, int(max_page) + 1):
		url_pic = url+'/'+str(i)
		yield url_pic


# �õ���ͼÿһҳ�����ص�ַ
def get_page_index(url):
	headers = {
		'Cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c = 1523859284, 1524038568;Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c = 1524038865',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36'
	}
	response = requests.get(url, headers=headers)
	bs = BeautifulSoup(response.text, 'lxml')
	a = bs.select('div[class="main-image"] img')
	for li in a:
		yield li.get('src')


def download_pic(url):
	headers = {
		'Cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c = 1523859284, 1524038568;Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c = 1524038865',
		'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 63.0.3236.0Safari / 537.36',
		'Referer':'http://www.mzitu.com/'
	}
	try:
		html = requests.get(url, headers=headers)
		content = html.content
		print(url)
		print(html.status_code)
		if html.status_code == 200:
			file_path = '{0}/{1}/{2}.{3}'.format(sys.path[0], 'new', md5(content).hexdigest(), 'jpg')
			if not os.path.exists(file_path):
				with open(file_path, 'wb') as f:
					f.write(content)
					print("ͼƬ���سɹ�")
		return 1
	except RequestException:
		print('����ͼƬʧ��', url)
		return None


def main(offset):
	for url in get_url(offset):
		for next_url in get_maxpage(url):
			for final_url in get_page_index(next_url):
				download_pic(final_url)

if __name__ == '__main__':
	# groups����http://www.mzitu.com/page/ ҳ����������
	groups = [x for x in range(1, 176)]
	pool = Pool()
	pool.map(main, groups)


``` 

#### 2.2 �����ȡ��1W+ͼƬ�����ڲ�������ԭ��ͼƬ�Ͳ�չʾ�ˣ���

![class](mztSpider.PNG)



### 3 �Ա���Ʒץȡ--�洢��mongodb

#### 3.1 Դ�����£�

``` class

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
MAX_PAGE = 100
KEYWORD = '��ʽ���޷�'
MONGO_URL ='localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def index_page(page):
	"""
	ץȡ����ҳ
	:param page:ҳ��
	:return:
	"""
	print('������ȡ��', page, 'ҳ')
	try:
		url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
		browser.get(url)
		if page > 1:
			input = wait.until(
				EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
			submit = wait.until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
			input.clear()
			input.send_keys(page)
			submit.click()
		# �ȴ���ת���ҳ��������
		wait.until(
			EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
		# .m-itemlist .items .item���ѡ������Ӧ����ÿ����Ʒ����Ϣ��
		wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
		# ������سɹ�����ִ�к����� get_products()����
		get_products()
	except TimeoutException:
		index_page(page)

def get_products():
	"""
	��ȡ��Ʒ����
	:return:
	"""
	html = browser.page_source
	doc = pq(html)
	items = doc('#mainsrp-itemlist .items .item').items()
	for item in items:
		product = {
			'image': item.find('.pic .img').attr('data-src'),
			'price': item.find('.price').text(),
			'deal': item.find('.deal-cnt').text(),
			'title': item.find('.title').text(),
			'shop': item.find('.shop').text(),
			'location': item.find('.location').text()
		}
		print(product)
		save_to_mongo(product)

def save_to_mongo(result):
	"""
	������MongoDB
	:param result:���
	:return:
	"""
	try:
		if db[MONGO_COLLECTION].insert(result):
			print('�洢��MongoDB�ɹ�')
	except Exception:
		print('�洢��MongoDBʧ��')

def main():
	"""
	����ÿһҳ
	:return:
	"""
	for i in range(1, MAX_PAGE + 1):
		index_page(i)

main()

``` 

#### 3.2 ץȡ�����ͼ��

![class](seleniumSpider.PNG)


### 4 ��������Ϣץȡ--����CSV�ļ����洢��������Ŀ

#### 4.1 Դ�����£�
``` class
import re
import requests
import csv
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import RequestException


def get_one_page(city, keyword, region, page):
	# ��ȡ��ҳ���ݲ�����
	paras = {
		'jl': city,  # ��������
		'kw': keyword,  # �����ؼ���
		'isadv': 0,  # �Ƿ�򿪸���ϸ����
		'isfilter': 1,  # �Ƿ�Խ������
		'p': page,  # ҳ��
		're': region,  # region����д������
	}

	headers = {
		'Host': 'sou.zhaopin.com',
		'Referer': 'http: // sou.zhaopin.com / jobs / searchresult.ashx?jl = % E5 % 8C % 97 % E4 % BA % AC & kw = python % E5 % B7 % A5 % E7 % A8 % 8B % E5 % B8 % 88 & p = 1 & isadv = 0',
		'Upgrade - Insecure - Requests': '1',
		'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 63.0.3236.0Safari / 537.36',
	}

	url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?' + urlencode(paras)
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException as e:
		return None


def parse_one_page(html):
	# ����HTML���룬��ȡ������Ϣ������
	# ������ʽ���н���
	pattern = re.compile('<a style=.*? target="_blank">(.*?)</a>.*?'  					# ƥ��ְλ��Ϣ
						 '<td class="gsmc"><a href="(.*?)" target="_blank">(.*?)</a>.*?'  	# ƥ�乫˾��ַ�͹�˾����
						 '<td class="zwyx">(.*?)</td>', re.S)  								# ƥ����н

	items = re.findall(pattern, html)

	for item in items:
		job_name = item[0]
		job_name = job_name.replace('<b>', '')
		job_name = job_name.replace('</b>', '')
		yield {
			'job': job_name,
			'website': item[1],
			'company': item[2],
			'salary': item[3],
		}

def write_csv_file(path, headers, rows):
	# ����ͷ����ϵд��csv�ļ�
	with open(path, 'a', encoding='utf8', newline='') as f:
		f_csv = csv.DictWriter(f, headers)
		f_csv.writeheader()
		f_csv.writerows(rows)

def write_csv_headers(path, headers):
	# д���ͷ
	with open(path, 'a', encoding='utf8', newline='') as f:
		f_csv = csv.DictWriter(f, headers)
		f_csv.writeheader()

def write_csv_rows(path, headers, rows):

	# д����
	with open(path, 'a', encoding='utf8', newline='') as f:
		f_csv = csv.DictWriter(f, headers)
		f_csv.writerows(rows)

def main(city, keyword, region, pages):
	'''
	:param city: ��Ҫ��ѯ�ĳ���
	:param keyword: ��Ҫ��ѯ��ְλ
	:param region: ����ĳ��д���
	:param pages: ��ѯҳ��
	:return: ��ĿĿ¼������һ��csv�ļ���������ְҵ���ơ���˾���ơ���˾��ַ��н��
	'''
	filename = 'zl_' + city + '_' + keyword + '.csv'
	headers = ['job', 'website', 'company', 'salary']
	write_csv_headers(filename, headers)
	for page in tqdm(range(1, pages+1)):
		jobs = []
		html = get_one_page(city, keyword, region, page)
		items = parse_one_page(html)
		for item in items:
			jobs.append(item)
		write_csv_rows(filename, headers, jobs)


if __name__ == '__main__':
	# 2381�Ǹ�����
	main('�ɶ�', 'python', 2381, 10)

```

#### 4.2 ץȡ�����ͼ��

![class](zhilianSpider.PNG)

![class](zhilianCSV.PNG)
