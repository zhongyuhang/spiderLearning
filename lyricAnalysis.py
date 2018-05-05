import requests
import os
import jieba
import jieba.analyse
import re
import json
from lxml import etree
import glob
import heapq
from pyecharts import Bar
from snownlp import SnowNLP
import collections

class music:
	def getAlbum(self):
		"""
		获取专辑信息
		:return: yield返回专辑id
		"""
		url = "http://music.163.com/artist/album?id=6452&limit=100&offset=0"
		headers = {
			'Host': 'music.163.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
		}
		html = requests.get(url, headers=headers)
		content = etree.HTML(html.text)
		content_data = content.xpath('//div[@class="u-cover u-cover-alb3"]')[0]
		# 正则表达式获取专辑的名字
		pattern_name = re.compile(r'<div class="u-cover u-cover-alb3" title="(.*?)">', re.S)
		names = re.findall(pattern_name, html.text)
		cal = 0
		if(os.path.exists("专辑信息.txt")):
			os.remove("专辑信息.txt")
		for i in names:
			cal += 1
			p = i.replace('""', '')
			pattern_id = re.compile(r'<a href="/album\?id=(.*?)" class="tit s-fc0">%s</a>' % (p))
			album_id = re.findall(pattern_id, html.text)
			with open("专辑信息.txt", 'a') as f:
				f.write("album-name:%s,album-id:%s \n" % (i, album_id))
			yield str(album_id).replace("[", "").replace("]", "").replace("'", "")

	def getSong(self, album_id):
		"""
		接收专辑id，根据专辑id获取歌曲id并存入文件 专辑歌曲信息.txt
		:param album_id:
		:return:
		"""
		url = 'http://music.163.com/album?id=' + str(album_id)
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
			'Host': 'music.163.com',
		}
		html = requests.get(url, headers=headers)
		content = etree.HTML(html.text)
		html_data = content.xpath('//ul[@class="f-hide"]//a')
		for i in html_data:
			html_data_one = i.xpath('string(.)')
			html_data_two = str(html_data_one)
			# 获取歌曲id
			pattern = re.compile(r'<li><a href="/song\?id=(\d+?)">%s</a></li>' % (html_data_two))
			song_id = re.findall(pattern, html.text)
			with open("专辑歌曲信息.txt", 'a') as f:
				if len(song_id) > 0:
					f.write("song-name:%s,song-id:%s \n" % (html_data_two, song_id))
				print("获取歌曲 %s 以及歌曲的ID %s 写入文件成功" % (html_data_two, song_id))

	def getLyric(self):
		"""
		根据专辑歌曲信息.txt文件，抓取所有歌曲歌词
		并按照 歌曲名-（歌曲名）.txt的方式生成文件，里面存有相应歌曲的歌词
		:return:
		"""
		for i in glob.glob("*热评*"):
			os.remove(i)
		for i in glob.glob("*歌曲名*"):
			os.remove(i)
		# 直接读取所有的信息
		file_object = open("专辑歌曲信息.txt")
		list_of_line = file_object.readlines()
		aaa = 1
		namelist = ""
		for i in list_of_line:
			# 歌曲的名字是： ID是：
			pattern_name = re.compile(r'song-name:(.*?),song-id')
			pattern_id = re.compile(r'song-id:\[\'(.*?)\'\]')
			item_name = str(re.findall(pattern_name, i)).replace("[", "").replace("]", "").replace("'", "")
			item_id = str(re.findall(pattern_id, i)).replace("[", "").replace("]", "").replace("'", "")
			# print(item_name, item_id)
			# 现在根据歌曲id获取歌词
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
				'Host': 'music.163.com',
			}
			url = "http://music.163.com/api/song/lyric?id="+item_id+"&lv=1&kv=1&tv=1"
			html = requests.get(url, headers=headers)
			json_obj = html.text
			info = json.loads(json_obj)
			try:
				lrc = info['lrc']['lyric']
				pat = re.compile(r'\[.*\]')
				lrc = re.sub(pat, "", lrc)
				lrc = lrc.strip()
				with open("歌曲名-"+item_name+".txt", 'w', encoding="utf-8") as f:
					f.write(lrc)
				aaa += 1
				namelist = namelist + item_name + ".text" + ","
			except:
				print("歌曲%s有错误" % item_name)

	def getCommon(self):
		file_object = open("专辑歌曲信息.txt")
		list_of_line = file_object.readlines()
		for i in list_of_line:
			pattern_name = re.compile(r'song-name:(.*?),song-id')
			pattern_id = re.compile(r'song-id:\[\'(.*?)\'\]')
			item_name = str(re.findall(pattern_name, i)).replace("[", "").replace("]", "").replace("'", "")
			item_id = str(re.findall(pattern_id, i)).replace("[", "").replace("]", "").replace("'", "")
			url = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + str(item_id)
			headers = {
				'Accept - Encoding': 'gzip, deflateAccept - Language: zh - CN, zh;q = 0.9',
				'Cache - Control': 'max - age = 0',
				'Connection': 'keep - alive',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
				'Host': 'music.163.com',
				'Upgrade - Insecure - Requests': '1',
			}
			html = requests.get(url, headers=headers)
			json_obj = html.text
			info = json.loads(json_obj)
			hot_comment = info['hotComments']
			for u in hot_comment:
				username = u['user']['nickname']
				likedCount = str(u['likedCount'])
				comments = u['content']
				with open(item_name + "的热评hotComment" + ".txt", 'a+', encoding='utf8') as f:
					f.write("用户名是:" + username + "\n")
					f.write("评论内容是：" + comments + "\n")
					f.write("点赞数是:" + likedCount + "\n")
					f.write("-------------------------我是分割线-------------------------" + "\n")
			print(item_name + "的热评下载成功" + "\n")

	def mergedFile(self):
		target = 0
		for i in glob.glob("*歌曲名*"):
			file_obj = open(i, 'r', encoding='utf8')
			list_of_line = file_obj.readlines()
			for p in list_of_line:
				if "作词" in p or "作曲" in p or "混音助理" in p or "混音师" in p or "录音师" in p or"执行制作" in p or "编曲" in p:
					target += 1
					print(p)
				else:
					with open("allLyric" + ".txt", "a", encoding='utf-8') as f:
						f.write(p)
			print(target)

		# 要去掉空行的文件
		file_one = open('allLyric.txt', 'r', encoding='utf-8')
		# 生成没有空行的文件
		file_two = open('allLyric_no_space.txt', 'w', encoding='utf-8')
		try:
			for line in file_one.readlines():
				if line == '\n':
					line = line.strip("\n")
				file_two.write(line)
		finally:
			file_one.close()
			file_two.close()
		print("合并歌词文件完成")

	def splitSentence(self, inputFile, outputFile):
		"""
		结巴分词处理歌词
		:param inputFile:
		:param outputFile:
		:return:
		"""
		inf = open(inputFile, 'r', encoding='utf-8')
		outf = open(outputFile, 'w', encoding='utf-8')
		for line in inf:
			line = line.strip()
			line = jieba.analyse.extract_tags(line)
			outstr = " ".join(line)
			outf.write(outstr + '\n')
		inf.close()
		outf.close()
		# 分析前十的数据出现的次数
		f = open("分词过滤后.txt", 'r', encoding='utf-8')
		txt = f.read().split()
		fin = sorted([(x, txt.count(x)) for x in set(txt)], key=lambda x: x[1], reverse=True)
		print(fin)

	def lyricAnalysis(self):
		file = "allLyric_no_space.txt"
		allLyric = str([line.strip() for line in open(file, 'r', encoding='utf-8').readlines()])
		# 获取全部歌词
		allLyrics = allLyric.replace("'", "").replace(" ", "").replace("?", "").replace(",", "").replace('"', '').replace(".", "").replace("!", "").replace(":", "")
		self.splitSentence('allLyric_no_space.txt', '分词过滤后.txt')

		# 词频统计
		f = open("分词过滤后.txt", 'r', encoding='utf-8')
		txt = f.read()
		txt = txt.replace('\n', '')
		txt = txt.replace(' ', '')
		txt = txt.replace(',', '')
		txt = txt.replace('.', '')
		txt = txt.replace('。', '')
		mylist = list(txt)
		mycount = collections.Counter(mylist)
		# 有序返回前十个
		for key, val in mycount.most_common(10):
			print(key, val)

	def emotionAnalysis(self):
		"""
		对情绪进行分析
		SnowNLP是情绪分析模块
		:return:
		"""
		x_axis = []
		y_axis = []
		for i in glob.glob("*歌曲名*"):
			count = 0
			allsen = 0
			with open(i, 'r', encoding='utf-8') as handle:
				list_of_file = handle.readlines()
				for p in list_of_file:
					# 判断文件读取航是否为空行
					p = p.strip()
					if not(len(p)):
						continue # 为空则continue，跳过不管
					# 不为空则进行情绪统计
					else:
						if "作词" in p or "作曲" in p or "混音助理" in p or "混音师" in p or "录音师" in p or "执行制作" in p or "编曲" in p:
							pass
						else:
							s = SnowNLP(p)
							s1 = SnowNLP(s.sentences[0])
							count += 1
							allsen += s1.sentiments
			i = str(i)
			# 处理文件名获得歌曲的名字
			x_axis_test = i.split("-", 1)[1].split(".", 1)[0]
			x_axis.append(x_axis_test)
			avg = int(allsen)/count
			y_axis.append(avg)

		bar = Bar("柱状图数据堆叠示例")
		bar.add("周杰伦歌曲情绪可视化", x_axis, y_axis, is_stack=True, xaxis_interval=0)
		bar.render(r"D:\PyCharm\spiderLearning\musicSpider\chart\周杰伦歌曲情绪分析.html")

		# 显示最好的五首歌
		y_axis_first = heapq.nlargest(10, y_axis)
		temp = map(y_axis.index, heapq.nlargest(10, y_axis))
		temp = list(temp)
		x_axis_first = []
		for i in temp:
			x_axis_first.append(x_axis[i])

		# 情绪积极TOP
		bar = Bar("周杰伦情绪较好的前十首歌")
		bar.add("周杰伦歌曲情绪可视化", x_axis_first, y_axis_first, is_stack=True)
		bar.render(r"D:\PyCharm\spiderLearning\musicSpider\chart\周杰伦积极歌曲TOP10.html")

		# 情绪最差TOP10
		y_axis_first = heapq.nsmallest(10, y_axis)
		temp = map(y_axis.index, heapq.nsmallest(10, y_axis))
		temp = list(temp)
		x_axis_first = []
		for i in temp:
			x_axis_first.append(x_axis[i])

		# 情绪差TOP10图
		bar = Bar("周杰伦情绪较差的前十首歌")
		bar.add("周杰伦歌曲情绪可视化", x_axis_first, y_axis_first, xaxis_interval=0,)
		bar.render(r"D:\PyCharm\spiderLearning\musicSpider\chart\周杰伦最消极歌曲TOP10.html")

"""
ex = music()

通过遍历获取的专辑id获得全部的歌曲id
for album_id in ex.getAlbum():
	ex.getSong(album_id)
	
获取评论
ex.getCommon()

将与歌词无关的文件行全部去掉，将所有歌词合并生成新的歌词文件allLyric_no_space.txt
ex.mergedFile()

将所有词过滤并记录出现频率
ex.lyricAnalysis()

使用snownlp模块对歌词进行情绪分析，并生成图表
ex.emotionAnalysis()

"""
