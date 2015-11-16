import pandas

data = pandas.read_csv("english_data.csv")
print(data)
print(data.Kelly)

data = pandas.read_csv("japanese_data.csv")
print(data)
print(data.慶子)
print(data[u"慶子"])
print(data[u"慶子".encode("utf-8")])


data = pandas.read_csv("romaji_data.csv")
print(data)
print(data.Keiko)

# Haruto as kanji: (陽斗, 陽翔, 大翔)