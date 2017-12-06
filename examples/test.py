import requests
import sys
import markdown
import codecs
import json

mdFile = sys.argv[1]
title, category, tags, createDay = mdFile.split('+')

input_file = codecs.open(mdFile, mode="r", encoding="utf-8")
text = input_file.read()
content = markdown.markdown(text)

headers = {'Content-Type': 'application/json'}
payload = {'title': title, 'category': category,  'content': content, 'tags': tags.split('-'), 'createDay': createDay.split('.')[0]}
r = requests.post("http://127.0.0.1:5000/blog/new", data=json.dumps(payload), headers=headers)
print r
