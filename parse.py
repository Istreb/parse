#!/usr/bin/python3
import urllib.request
from urllib.parse import urlparse
import re
import sys, getopt
from datetime import datetime
import configparser
import os
import textwrap

def parse_content(text, type): #убираем лишнее
   res = ''
   if type == 'header':
      res = text.replace('&nbsp;',' ') #удаление неразрывных пробелов
      res += '\n'
   elif type == 'content':
      res = re.sub(r'</p>|</div>', '', text) #удаление лишних закрывающих тегов
      res = re.sub(r'<a href=\"?\'?([^"\'>]*)\".*?>(.*?)</a>', r'[\1] \2', res) #обработка ссылок
      res = re.sub(r'<aside.*?</aside>', r'', res) #рекомендованные материалы
      res = re.sub(r'<i>(.*?)</i>', r'\1', res) #примечания
      res = re.sub(r'<p>|<br.*?>', '\n\n', res) #перенос по абзацам
      string_size = Config.get('default', 'string_size')
      res = textwrap.fill(res, int(string_size), replace_whitespace=False)
   return res

def find_lemm(text, domain, s_path): #поиск нужных лемм
   header_tag = Config.get(domain, 'header_tag') #читаем теги и их классы из конфига
   header_tag_class= Config.get(domain, 'header_tag_class')
   content_tag= Config.get(domain, 'content_tag')
   content_tag_class= Config.get(domain, 'content_tag_class')
   found =0
   f = open(s_path+"/res.txt", "w", encoding='utf-8')
   for line in text.splitlines():
      if found ==2: # если нашли и текст и заголовок - выйти
         print(str(datetime.now().time()) + ':\tparsed url content written to '+ s_path+'/res.txt')
         break
      header_pattern = re.compile(header_tag+'.*class=\".*'+header_tag_class+'.*?\".*?>(.*)?</'+header_tag) #паттерн для поиска заголовка
      if re.search(header_pattern, line):
         result = header_pattern.findall(line)
         res = parse_content(result[0],'header') 
         f.write(res)
         found+=1
      content_pattern = re.compile(content_tag+'.*class=\".*'+content_tag_class+'.*?\".*?>(.*)?</'+content_tag) #паттерн для поиска текста
      if re.search(content_pattern, line):
         result = content_pattern.findall(line)
         res = parse_content(result[0],'content')
         f.write(res)
         found+=1
   f.close()

def open_url(url): #открываем url
   print (str(datetime.now().time()) + ':\turl is ', url)
   page = urllib.request.urlopen(url)
   s_path=Config.get('default', 'def_folder')
   i_domain = 0
   domain = ''
   for val in url.split('/'):
      if val == '' or val =='http:' or val=='https:':
         continue
      else:
         if i_domain == 0:
            i_domain = 1
            domain = val #запоминаем название домена
         s_path +='/'+val
         if not os.path.exists(s_path):
            os.makedirs(s_path) #создаем структуру папок, если ее нет
   f = open(s_path+"/orig.txt", "w", encoding='utf-8') #сохраняем оригинальный файл на всякий случай
   content = page.read()
   encoding = Config.get(domain, 'encoding')
   text = str(content.decode(encoding))
   f.write(text)
   f.close()
   print(str(datetime.now().time()) + ':\toriginal url content written to '+ s_path+'/orig.txt')
   find_lemm(text, domain, s_path) #поиск нужных лемм

def get_conf():
   global Config 
   Config = configparser.ConfigParser()
   Config.read("conf.ini")
    
def main(argv):
   url = ''
   usage_str = Config.get('default', 'usage_str')
   try:
      opts, args = getopt.getopt(argv,"hu:",["url="]) #возможные ключи -h,-u или --url
   except getopt.GetoptError:
      print (usage_str)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (usage_str)
         sys.exit()
      elif opt in ("-u", "--url"):
         url = arg
         open_url(url)
if __name__ == "__main__":
   get_conf()
   main(sys.argv[1:])