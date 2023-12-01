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
        self.root = tk.Tk() #Creates Tkinter Instance to use its features and create a window  
        #Below code is for Defining the style of GUI
        self.root.title("TEXT SPELLING CHECKER")#Setting the title of the Opened Window 
        self.root.geometry("700x600") #Sets the size of the main window
        self.text = ScrolledText(self.root,width=50,height=15,font=("Arial",14)) #This gives space for text input where we can type and scrolled here means we can enter multiple lines and also we have a scroll bar
        self.text.bind("<KeyRelease>", self.check) #When ever the key is released (Pressing a key and releasing it) we are calling the function check, key release is the trigger. so when this action is performed it calls the self.check function which detects the misspelled words
        self.text.bind("<Return>",self.check_append) #To Take the Red Words and store it in a list, This function is performed when we press enter after typing the complete text.
        self.text.bind("<Control-Return>",self.corrected_text)#To print the Corrected sentence, here we have to press control + Enter
        self.text.pack(pady=20) #Adds text to the gui i.e it packs all the things we have defined into the GUI, pady means leaving 20px space on top to look good
        self.old_spaces = 0 #Settings a normal variable to store the number of spaces present in the full text
        self.button_frame = Frame(self.root) #an instance to create button.
        self.button_frame.pack()# adding the buttons to the gui
        self.content = self.text.get('1.0',END) #Getting the text from the text space, here 1.0 means first character of first line in the GUI similary second char -> 1.1 , third char -> 1.2 and so on.., tk.END means till final char.

        clear_button = Button(self.button_frame,text='Clear Text', command=self.clear_text  )# Creating a button that when pressed clears the text in the textspace and new text can be inputed
        clear_button.grid(row=0,column=0,padx=20)#For aligment of button, it is placed in row 0 and column 0 and with 20pixel space on each sides

        translate_button = Button(self.button_frame,text='Translate',command=self.lang_select)#Creating a button that when pressed opens the translating window
        translate_button.grid(row=0,column=1,padx=20)#For alignment of the button

        exit_button = Button(self.button_frame,text="Exit",command=self.root.destroy)#Creating a button that when pressed it closes the Tkinter gui 
        exit_button.grid(row=0,column=2,padx=20)#for allignment 

        abbr_slan_button = Button(self.button_frame,text="Add Abbrevation",command=self.abr_adder)#Creating a button that when pressed it opens up the adding abbreviation window
        abbr_slan_button.grid(row=0,column=3,padx=20)#Allignment


        self.my_label = Label(self.root,text='')#Creates a label-text in the window for now of no text
        self.my_label.pack(pady=15)#adding the label to the window
        self.root.mainloop() #gets the GUI Running
    def abr_adder(self):#Function that is performed when the add abbreviation is clicked
        self.abr = tk.Tk() #Creating a new tkinter instance 
        self.abr.title('Add Abbreviation')#adding the title
        self.abr.geometry("300x300")#Setting the geometry of the window
        self.abr_text= Text(self.abr,height=5,width=20)#Giving text space for the user to input the abbreviation
        self.abr_text.pack(padx=10,pady=20)#adding the text to Gui 


        self.button_frame_abr = Frame(self.abr)#Creating a button instance
        self.button_frame_abr.pack()#adding the buttons to GUI
        f = open('abbrevation.bin',"ab+")#Opening the abbreviation file to load the previous exisiting abbreviation

        def write_into():#adding new abbreviations into the text
            f = open('abbrevation.bin',"ab+")#opening the abbreviation file to load and write
            abr_text = self.abr_text.get('1.0',END)#getting the content present in the abbreviation GUI window
            f.seek(0)#going to the 0th position of the file since ab+ mode opens with file pointer at end
            previous_content = (pickle.load(f))#loading all the text from the file 
            previous_content.append(abr_text.rstrip())#Adding the new abbreviation to the list of previous abbreviation
            f.close()#Closing the file so that it gets saved
            f = open('abbrevation.bin','wb')#Opening the file in wb mode to write the new abbreviation
            pickle.dump(previous_content,f)#Writing the list of abbreviation in the text
            f.flush()#closing the file so that it gets saved


        add_button = Button(self.button_frame_abr,text="Add Abbreviation",command=write_into)#Add abbreviation button present in the window
        add_button.grid(row=0,column=0,pady=20)#positioning the button
        
        self.abr.mainloop()#running the Tkinter Gui


    def lang_select(self):#A Function that is performed when clicked on translate 
        self.label2 = Label(self.root,text="Enter the language code to translate",font=('Helvetica',15))#Displaying text for used to choose the language
        self.label2.pack()#adding the label to the gui
        self.lang = Text(self.root,height=2)#Giving a text space for the user to type the destination language
        self.lang.pack()#adding the text space
        self.lang.bind('<Return>',self.trans)#When pressed enter it calls the Trans function
        
    def trans(self,event):#Translator Function that uses Google Translate API to translate text into other languages
        dest_lang = self.lang.get('1.0','1.2')#Getting the content that has to be translated
        try:
            self.label.destroy()#This is to remove the previous translated text when a second a different language is passed again
        except:
            pass
        translator = Translator()#Creating the instance of the translator to use its function
        translated = translator.translate(corrector.correctr(),dest=dest_lang)#The corrected text that has no spelling errors is passed and also the destination language is passd
        self.label = Label(self.root,text=translated.text,font=('Helvetica',15))#Displaying the translated text
        self.label.pack(pady=10)#adding it to the gui

    def corrected_text(self,event):
        self.my_label.config(text=f'Corrected Text: '+f'{corrector.correctr()}',font=('Helvetica',15))#Corrected Text
    def clear_text(self):
        self.text.delete("1.0",END)

    #Functon to store text       
    def check_append(self, event):
        red_words = []# Stores the list of wrong words
        content = self.text.get("1.0",tk.END) #Gets the text typed in text box
        f = open('abbrevation.bin','rb') #Opening the abbreviation binary file to check and add abbreviation
        abbrevation_text = pickle.load(f)#Loading the text from the file and saving it 
        for word in content.split(" "):#For loop to check for all the wrong words
            if re.sub(r"[^\w]", "",word.lower()) not in words.words() and re.sub(r"[^\w]", "",word.lower()) not in abbrevation_text  :#Checking for the wrong word
                if re.sub(r"[^\w]","",word.lower()) not in red_words:#Checking if this word is already marked as wrong
                    red_words.append(re.sub(r"[^\w]","",word.lower()))#If this word is not marked wrong we store it 
        #print(red_words) Ignore this line
        red_words.append(content)#Also storing the full sentence in the list
        with open('red_words.bin','wb') as f: 
            pickle.dump(red_words,f)#writing it into the file 

    #Function that is performed on keyrelease sequence
    #Main Function
    def check(self, event):
        content = self.text.get("1.0",tk.END) #here 1.0 means first character in the GUI similary second char -> 1.1 , third char -> 1.2 and so on.., tk.END means till final char.
        space_count = content.count(" ")#counting the number of spaces in the inputted text
        f = open('abbrevation.bin','rb') #Opening the abbreviation binary file to check and add abbreviation
        abbrevation_text = pickle.load(f)#Loading the text from the file and saving it 
        if space_count != self.old_spaces:
            self.old_spaces = space_count 

            for tag in self.text.tag_names():
                self.text.tag_delete(tag)


            for word in content.split(" "):
                if re.sub(r"[^\w]", "",word.lower()) not in words.words() and re.sub(r"[^\w]", "",word.lower()) not in abbrevation_text :
                    #here [^\w] means everything that is not a normal char, i.e special char, all these are replaced by '' in word.lower()
                    # and checking if the stripped word is present in re word 
                    # and also checking if this is not present in the abbrevation text file
                    position = content.find(word) # Getting the position of the word that is not matching in re word to mark it red, marking it red is the next line code
                    self.text.tag_add(word,f"1.{position}", f"1.{position+ len(word)}") #creating a tag on the word that is spelled wrongly
                    self.text.tag_config(word, foreground="red")#making the text into red in color
spelling_checker()
