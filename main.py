import re #regular expression to get rid of all special character, example 'what?' is made into 'what' for easier checking 
import tkinter as tk #For Graphical user interface (GUI) where we can put our text.
from tkinter.scrolledtext import ScrolledText
from tkinter import *
import pickle
import nltk
from nltk.corpus import words
nltk.download('words') #to use words from nltk we are downloading it here
from corrector import corrector
from googletrans import Translator

class spelling_checker:


    def __init__(self):
        self.root = tk.Tk() #Creates the main window     
        #Defining the style of GUI
        self.root.title("TEXT SPELLING CHECKER")
        self.root.geometry("700x600") #Sets the resolution of the main window
        self.text = ScrolledText(self.root,width=50,height=15,font=("Arial",14)) #This gives space for text input where we can type and scrolled here means we can enter multiple lines and also we have a scroll bar
        self.text.bind("<KeyRelease>", self.check) #When ever the key is released we are calling the function check, key release is the sequence and self.check is the function to be performed when the sequence happens 
        self.text.bind("<Return>",self.check_append) #To Take the Red Words and store it in a list
        self.text.bind("<Control-Return>",self.corrected_text)
        self.text.pack(pady=20) #Adds text to the gui i.e it packs all the things we have defined into the GUI
        self.old_spaces = 0 #Settings a normal variable
        self.button_frame = Frame(self.root)
        self.button_frame.pack()
        self.content = self.text.get('1.0',END)

        clear_button = Button(self.button_frame,text='Clear Text', command=self.clear_text  )
        clear_button.grid(row=0,column=0,padx=20)

        translate_button = Button(self.button_frame,text='Translate',command=self.lang_select)
        translate_button.grid(row=0,column=1,padx=20)

        exit_button = Button(self.button_frame,text="Exit",command=self.root.destroy)
        exit_button.grid(row=0,column=2,padx=20)

        self.my_label = Label(self.root,text='')
        self.my_label.pack(pady=15)
        self.root.mainloop() #gets the GUI Running
    def lang_select(self):
        self.label2 = Label(self.root,text="Enter the language code to translate",font=('Helvetica',15))
        self.label2.pack()
        self.lang = Text(self.root,height=2)
        self.lang.pack()
        self.lang.bind('<Return>',self.trans)
        #dest_lang = self.lang.get('1.0','1.2')
        #print(dest_lang)
        #self.lang.destroy()
        
    def trans(self,event):
        dest_lang = self.lang.get('1.0','1.2')
        try:
            self.label.destroy()
        except:
            pass
        translator = Translator()
        #translated = translator.translate(self.text.get('1.0',END),dest=dest_lang)
        translated = translator.translate(corrector.correctr(),dest=dest_lang)
        self.label = Label(self.root,text=translated.text,font=('Helvetica',15))
        
        self.label.pack(pady=10)

    def corrected_text(self,event):
        self.my_label.config(text=f'Corrected Text: '+f'{corrector.correctr()}',font=('Helvetica',15))#Corrected Text
    def clear_text(self):
        self.text.delete("1.0",END)

    #Functon to store text       
    def check_append(self, event):
        red_words = []
        content = self.text.get("1.0",tk.END)
        
        for word in content.split(" "):
            if re.sub(r"[^\w]", "",word.lower()) not in words.words():
                if re.sub(r"[^\w]","",word.lower()) not in red_words:
                    red_words.append(re.sub(r"[^\w]","",word.lower()))
        print(red_words)
        red_words.append(content)
        with open('red_words.bin','wb') as f: 
            pickle.dump(red_words,f)

    #Function that is performed on keyrelease sequence
    def check(self, event):
        content = self.text.get("1.0",tk.END) #here 1.0 means first character in the GUI similary second char -> 1.1 , third char -> 1.2 and so on.., tk.END means till final char.
        space_count = content.count(" ")

        if space_count != self.old_spaces:
            self.old_spaces = space_count

            for tag in self.text.tag_names():
                self.text.tag_delete(tag)


            for word in content.split(" "):
                if re.sub(r"[^\w]", "",word.lower()) not in words.words():
                    #here [^\w] means everything that is not a normal char, i.e special char, all these are replaced by '' in word.lower()
                    # and checking if the stripped word is present in re word 

                    position = content.find(word) # Getting the position of the word that is not matching in re word to mark it red, marking it red is the next line code
                    self.text.tag_add(word,f"1.{position}", f"1.{position+ len(word)}") 
                    self.text.tag_config(word, foreground="red")
                    


spelling_checker()
