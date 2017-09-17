from pypinyin import pinyin
from unidecode import unidecode
import pypinyin
import re
import json
import collections
import itertools
"""Script to generate list of all valid pinyins"""

chars = [] # store all Chinese characters

with open("characters.txt", "r") as file:
	for line in file:
		try:
			chars.append(line.strip())
		except:
			pass

# map each character to its pinyin
l = list(map(lambda x: pinyin(x, heteronym=True,strict=True,style=pypinyin.NORMAL), chars))
# flatten list
l = list(itertools.chain(*list(itertools.chain(*l))))
# decode unicode into ascii
l = list(map(unidecode, l))
# remove duplicates
syllables = list(set(l))
# filter invalid pinyin
r = re.compile("[a-z]+")
syllables = list(filter(r.match, sorted(syllables)))

d = {}
# write all pinyin to a file
f = open("./lazy_pinyin.txt","w")
for i in syllables:
	start = i[0]
	if d.get(start) == None:
		d[start] = [i]
	else:
		d[start].append(i)
	f.write(i)
	f.write("\n")
	# print(i)
f.close()

od = collections.OrderedDict(sorted(d.items()))

# print(od)

# write JSON representation
f = open("./mapping.json","w")
# print(json.dumps(od, indent=4))
f.write(json.dumps(od, indent=4))
f.close()

print(len(syllables))