from textblob import TextBlob
from textblob import Word
import pickle
class corrector():
    def correctr():
        f = open('red_words.bin','rb')
        text = pickle.load(f)
        text[-1] = (text[-1].strip())
        #print(text)
        c_words = {}
        for i in text: 
            if i == '':
                break
            else:
                word = TextBlob(i)
                c_words [i] =  str(word.correct())
                #print(str(word.correct()))
        content = text[-1]

        correct_content = ''
        for i in content.split(' '):
            if i in c_words:
                correct_content+= (i.replace(i,c_words[i])+ ' ') 
            else:
                correct_content+=(i+' ')
        return correct_content
            

