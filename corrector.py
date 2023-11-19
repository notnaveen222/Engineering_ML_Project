from textblob import TextBlob
f = open('red_words.txt','r')
text = f.read().split(',')
text.remove('')
print(text)
c_words = []
for words in text:
     word = TextBlob(words)
     correct = word.correct()
     c_words.append(correct)
print(c_words)