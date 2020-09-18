import re
import random
# from _collections import defaultdict
from math import fabs

eps = 0.01

r_alphabet = re.compile(u'[а-яА-Я0-9-’.,:;?!]+')


def get_line(ainput):
    for line in ainput:
        yield line.lower()


def get_word(line):
    for word in line:
        yield word


def get_bigramms(words):
    for i in range(len(words) - 1):
        yield words[i], words[i + 1]


def statistic1(statistic, bigramms):
    for bi in bigramms:
        if bi in statistic:
            statistic[bi] += 1
        else:
            statistic[bi] = 1


def statistic2(statistic, super_statistic):
    for s1, s2 in statistic:
        if s1 in super_statistic:
            super_statistic[s1].append([s2, statistic[s1, s2]])
        else:
            super_statistic[s1] = [[s2, statistic[s1, s2]]]
    for key in super_statistic:
        prob = 0
        for i in range(len(super_statistic[key])):
            prob += super_statistic[key][i][1]
        for i in range(len(super_statistic[key])):
            super_statistic[key][i][1] /= prob


def generate_phrase(super_statistic):
    phrase = ""
    phrase += '^ '
    x=random.randint(0, len(super_statistic['^']))
   # print(x)
    phrase += super_statistic['^'][x][0]
    #print(phrase)
    i = 0
    maxnum = 0
    maxind = 0
    while True:
        curr = phrase.split()[-1]
        if curr in super_statistic:
            for j in range(len(super_statistic[curr])):

                if super_statistic[curr][j][1] > maxnum:
                    maxnum = super_statistic[curr][j][1]
                    maxind = j
                if fabs(super_statistic[curr][j][1] - maxnum) < eps:
                    maxind = random.choice([maxind, j])
            phrase += " "
            phrase += super_statistic[curr][maxind][0]
            i += 1
            maxnum = 0
        if phrase.split()[-1] == "^":
            break
    return phrase


f = open('text.txt', 'r')
text = f.read()
data = re.split(r'[.|!|?|…]', text)
str = (get_line(data))
words = []

for i in range(len(data)):
    line = re.findall(r'\w+', next(str))
    word = get_word(line)
    words.append('^')
    for j in range(len(line)):
        words.append(next(word))

bigramms = []
bigramm = get_bigramms(words)
for k in range(len(words) - 1):
    bigramms.append(next(bigramm))

statistic = dict()
statistic1(statistic, bigramms)
super_statistic = dict()
statistic2(statistic, super_statistic)
print("enter number of phrases")
n=int(input())
i=0
for i in range(n):
    print(generate_phrase(super_statistic))
