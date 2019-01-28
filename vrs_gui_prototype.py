#!/usr/bin/python3

from tkinter import *
import sv.enrollment as enroll
import sv.verification as verify
from tkinter.messagebox import *
import sounddevice as sd
from configuration import get_config
import numpy as np
from PIL import Image, ImageTk

config = get_config()


''' Define fields in main window '''
fields = 'Name',

def fetch(entries):
    ''' Fetch/display entries in terminal'''
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text)) 

        
def makeform(root, fields):
    ''' Create contents of main window (label, entry)'''
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


def popup_showinfo(wdw="Window",text="Hello World!"):
    ''' Gets message text and display it in new window'''
    showinfo(wdw, text)
    
    
def enroll_entry(entries):
    print("enroll_entry")
    rec = prerecord("Enroll",entries)
    
    
def verify_entry(entries):
    print("verify_entry")
    rec = prerecord("Verify",entries)

        
def prerecord(action,entries):
    ''' Displays new window prompt for recording voice '''
    print("prerecord")
    name = entries[0][1].get()
    win = Toplevel()
    win.wm_title(action)
    lab = Label(win, text = "Press OK when ready. \n Will start immediately and record for 5 seconds").pack()
    okButton = Button(win,
                     text = "OK",
                     command = lambda a=action: record(a,name,win)).pack()
    

def record(action,name,win):
    ''' Function for recording voice and closes previous window'''
    print("record")
    recording = sd.rec(int(config.duration * config.sr), samplerate=config.sr, channels=1)
    print("Recording...")
    sd.wait()
    recording = np.reshape(recording,config.duration*config.sr)
    res = work(action,name,recording)
    result(name,action,res)
    close_window(win)
    
    
def result(name,action,res):
    ''' Displays result of enrollment/verification'''
    print("result")
    if res == True:
        if action == "Enroll":
            popup_showinfo(action,"Congrats! Enrolled ka na %s" % name)
        elif action == "Verify":
            popup_showinfo(action,"Congrats! Ikaw nga yan %s!" % name)
    else:
        if action == "Enroll":
            popup_showinfo(action,"Error. Please record again.")
        elif action == "Verify":
            popup_showinfo(action,"Hindi ka si %s! Guard hulihin to." % name)
    
    
def work(action,name,rec):
    ''' Gate to enroll/verify functions'''
    print("work")
    if action == "Enroll":
        res = enroll.main(name,rec)
    elif action == "Verify":
        res = verify.main(name,rec)
    return res
        
    
def close_window(win):
    win.destroy()

    
class Window(Frame):
    
    
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):
        imgpath = 'nm-logo-transparent.ico'
        im = Image.open(imgpath)
        img = ImageTk.PhotoImage(im)
        
        # changing the title of our master widget      
        self.master.title("Speaker Verification")
    
        # changing the icon of our master widget
        self.master.wm_iconbitmap(img)
        
        # adding image in our master widget
        """
        # image wont load
        # image needs to be manually place in upper left corner 
        # beside the intro text

        imgpath = 'nm-logo-transparent.png'
        im = Image.open(imgpath)
        img = ImageTk.PhotoImage(im)
        label = Label(self, image=img)
        label.pack(side = "top", fill = "both", expand = "no")
        label.image=img
        """
        
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating text in window
        introtext = "Welcome to \n NM Speaker Verification"

        ents = makeform(root, fields)
        root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
        b1 = Button(root, text='Enroll',
              command=(lambda e=ents: enroll_entry(e)))  ##(lambda e=ents: fetch(e)))
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(root, text='Verify',
              command=(lambda e=ents: verify_entry(e)))
        b2.pack(side=LEFT, padx=5, pady=5)
        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        label_intro = Label(self, 
                      justify = CENTER,
                      text = introtext).pack(side=TOP)
        
        
if __name__ == '__main__':
    root = Tk()
    app = Window(root)
    root.mainloop()