from pypinyin import lazy_pinyin
import pypinyin
import re
import json
import collections

chars = [] # store all Chinese(Simplified) characters

with open("characters.txt", "r") as file:
	for line in file:
		try:
			line = line.strip()
			chars.append(line)
			# print(line)
		except:
			pass

# l = list(map(lambda x: lazy_pinyin(x, style=pypinyin.TONE2), chars))

# map each character to its pinyin
l = list(map(lambda x: lazy_pinyin(x), chars)) 
# remove duplicates
syllables = list(set([item for sublist in l for item in sublist]))
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

print(len(syllables))

od = collections.OrderedDict(sorted(d.items()))

print(od)

# write JSON representation
f = open("./mapping.json","w")
print(json.dumps(od, indent=4))
f.write(json.dumps(od, indent=4))
f.close()
