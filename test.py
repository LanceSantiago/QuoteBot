import random
import re

f=open('testFile.txt')
lines=f.readlines()
quote = random.randint(0, len(lines)-1)
print (lines[quote])
nospeakerWithQuoteNum = lines[quote].split("\" - ")[0]
noSpeaker = (re.split(r'\#[0-9]*:', nospeakerWithQuoteNum)[1])
speakerWithNum = lines[quote].split("\" -")[1] 
speaker = speakerWithNum.split("[")[0] 
print(noSpeaker + "\"")
print(speaker)
print(noSpeaker + "\" - " + speaker)
# #386132: "How do I quote myself?
# Emily W [1566343650]

# want to get rid:
# #386132:
# [1566343650]


