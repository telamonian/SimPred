from Tkinter import *
import os.path

root = Tk()
root.configure(background='red')

def refresh():
    if os.path.isfile('/home/mklein/remote_called'):
        root.configure(background='green')
        Label(root,text='Executing Job...',font=('Ariel',80),bg='green',height=400,width=400).pack()
        root.after(2000,refresh)
    else:
        root.configure(background='red')
        root.after(100,refresh)
    return

#w = Label(root, text="Hi!")
#b = Button(root, text="Refresh!", command=refresh)
#b.pack()
#w.pack()
Label(root,text='Waiting For Job...',font=('Ariel',80),height=400,width=400,bg='red').pack()
root.after(100,refresh)
root.mainloop()
