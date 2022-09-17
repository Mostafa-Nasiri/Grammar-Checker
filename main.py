from tkinter import *
from tkinter import messagebox
from textblob import TextBlob

import sqlite3
import tkinter.ttk as ttk


root = Tk()
root.title("Grammer Paraphraser By Mostafa Nasiri")
width = 500
height = 550
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)


#=====================================VARIABLES============================================
quote1 = StringVar()
quote2 = StringVar()
ww=[]
wn=[]
wnnp=[]

#=====================================METHODS==============================================

def row_count(input):
    with open(input) as f:
     return len(f.readlines())

def loadinp():
    global ww
    global wn
    ww=[]
    wn=[]
    x=T1.get("1.0","end-1c")
    print(x)
    b = TextBlob(x)
    bb=(b.parse()).replace('\n',' ')
    ss=[]
    ss=bb.split(' ')
    #print(ss)
    for x in ss:
         #print(x.split('/'))
         tmp=x.split('/')
         ww.append(tmp[0])
         wn.append(tmp[1])
    #print(ww)
    #print(wn)
    detect()



def detect():
    print(("-"*5)+'start'+("-"*5))
    print(wn+ww)
    #loadinp()print(ww+wn)print(ww+wn)
    global wnnp
    wnnp=[]
    import pandas
    df = pandas.read_csv('dat\grammer_rules.csv')
    #print(type(df['type'][0])) <class 'str'>

    for i in range(len(df)):
         #==print(wn)
        det=df["minimal"][i].split('+')
        #print(str(wn.index('oi'))+det[3])

        tx=wn[0]
        for x in range(len(wn)):
            if x !=0: tx = tx+'+'+wn[x]
        #==print(tx)
        if  (tx.find(df["minimal"][i],0,len(tx)) != -1) and (df["behind"][i] == 'y'):
         #print('ma0')
         if (df["fulldetection"][i].find("...",0,len(df["fulldetection"][i])) != -1)  and (int(df["max"][i]) > 0):

          for x in range(int(df["max"][i])):
            #print('max')
            #print(str(x)+' -> '+str(len(tx.split('+'))))
            tmp=(df["fulldetection"][i].split('+'))[(df["fulldetection"][i].split('+')).index("...")-1]
            #print(tmp+'****'+df["fulldetection"][i].replace("...",((tmp+"+")*x)[0:len((tmp+"+")*x)-1]))
            tx=tx.replace(df["fulldetection"][i].replace("...",((tmp+"+")*x)[0:len((tmp+"+")*x)-1]),"@"+str(i)+"@"+str(len(df["fulldetection"][i].replace("...",((tmp+"+")*x)[0:len((tmp+"+")*x)-1]).split('+'))))
            #print('---->> '+tx)
            #print(str(x)+' -> '+str(len(tx.split('+'))))#
         else:
            #print('tx')
            tx=tx.replace(df["minimal"][i],"@"+str(i)+"@"+str(len(df["minimal"][i].split('+'))))
            #print('ma0')


         wnn=tx.split('+')


         #print(wnn)
         t =0


         for j in range(len(wnn)):
            if wnn[j].find("@"+str(i)+"@") != -1 :
                txx=''
                tmp=''
                tmp=(wnn[j].split('@'))
                tmp.insert(2,str(t))
                for x in range(len(tmp)):
                    if x !=0: txx = txx+'@'+tmp[x]

                #print(txx)
                wnnp.append(txx)
                t=t+int(wnn[j].split('@')[2])-1

                #if t ==j :

                #else:wnnp.append(wnn[j])
            t+=1

        print(wnnp)

    simple()

def simple():
    import pandas as pd
    #detect()
     #return [tree.get_element(1) for x in tree.selection()]

    df = pd.read_csv('dat\db.csv')
    dt = pd.read_csv('dat\grammer_rules.csv')
     #print(type(df['November'][0]))
     #messagebox.showinfo('', df["name"][0] + df["model"][0] )
    #print(wnnp)
     #print('', df["sign"].str.findall('fancy') )

    for j in range(len(wnnp)): #len(wnnp)----------------------
        #print(wnnp[j])
        tt=(wnnp[j][1:len(wnnp[j])]).split("@")
        #print(tt)
        print(("-"*5)+str(tt)+("-"*5))

        print(ww[int(tt[1]):int(tt[2])+int(tt[1])])
        print(wn[int(tt[1]):int(tt[2])+int(tt[1])])
        #-----order of adjectives---------
        model=(dt["model"][0]).split("+")
        q=dt["sens"][int(tt[0])].split("+")
        if len(q)==1 :
            f_pro={}
            for i in range(len(wn[int(tt[1]):int(tt[2])+int(tt[1])])):
             if dt["sens"][int(tt[0])]==(wn[int(tt[1]):int(tt[2])+int(tt[1])])[i]:
                #print(ww[int(tt[1]):int(tt[2])+int(tt[1])][i])
                t='0@'+str(i)
                #t=''

                for x in range(len(df)):
                 if  (df["word"][x].lower()==ww[int(tt[1]):int(tt[2])+int(tt[1])][i]) :
                     #print('', df["type"][x] +str(i))
                     if t=='': t=df["type"][x]
                     else:
                        t=t+"+"+str(model.index(df["type"][x]))+df["type"][x]
                        #print(str(t))
                f_pro[ww[int(tt[1]):int(tt[2])+int(tt[1])][i]] =t
            #----print(f_pro)
            dic={}
            dic = {'pos': [], 'typ': []}
            #fp=[]
            for x in f_pro:
              #  fp.append(x)
                tmp=f_pro[x].split("+")

                tmp.sort()
                #----print(tmp)

                dic['pos'].append(tmp[0])
                dic['typ'].append(tmp[1])
            #print(tmp)

            fd=pd.DataFrame(data=dic).sort_values('typ')

     ##            print(model)
     ##            print("-"*30)
     ##            print(ww[int(tt[1]):int(tt[2])+int(tt[1])])
            now=[]
            now=ww[int(tt[1]):int(tt[2])+int(tt[1])]

            #print(fp)
            #print(f_pro)
            #print(ww)
            #print(tmp)
            tmp=[]

            crct='t'


            ggg=fd.loc[fd.index,'typ'].iat[1]
            for y in range(len(fd)):
                st=fd.loc[fd.index,'pos'].iat[y].split('@')[1]
                tmp.append(ww[int(tt[1]):int(tt[2])+int(tt[1])][int(st)])
                now[y+1]=(ww[int(tt[1]):int(tt[2])+int(tt[1])][int(st)])
              #  print(ww[int(tt[1]):int(tt[2])+int(tt[1])][int(st)])
              #  print(st)
              #  print(str(y))

                #print(fd.loc[fd.index,'typ'].iat[y]+' '+fd.loc[fd.index,'pos'].iat[y])
        #------------------------------------------------------------------------
        #print(tmp)
        print(now)

        if crct=='t':
             #print(ww)
             ww[int(tt[1]):int(tt[2])+int(tt[1])]=now
        print(ww)

        if len(q)>1 : print("sign is more than 1")

    output()

def word():
    t=''
    for i in range(len(df)):
     if (df["sens"][i]=='JJ') and (df["word"][i].lower()=='skinny') :
      print('', df["type"][i] +str(i))
      if t=='': t=df["type"][i]
      else: t=t+"+"+df["type"][i]

def output():
 global ww
 out=''
 for i in range(len(ww)):
    if i==0 :
     out=ww[i]
    else:
       out=out +' '+ww[i]
 T2.delete("1.0","end-1c")
 T2.insert(END, out)


#=====================================FRAME================================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
TopFrame = Frame(root, width=500)
TopFrame.pack(side=TOP)
TopForm= Frame(TopFrame, width=300)
TopForm.pack(side=LEFT, pady=10)
TopMargin = Frame(TopFrame, width=260)
TopMargin.pack(side=LEFT)

#=====================================LABEL WIDGET=========================================
lbl_title = Label(Top, width=500, font=('arial', 18), text="Grammar Checker")
lbl_title.pack(side=TOP, fill=X)

#===================================,height=100==ENTRY WIDGET=========================================

T2 = Text(root, height=14, width=10)
T2.pack(side=LEFT, fill=Y)
#T2.config(yscrollcommand=S2.set)
T2.pack(side=BOTTOM, fill=X)
#T2.config(yscrollcommand=S2.set)

quote2 = "OUTPUT"
T2.insert(END, quote2)

T1 = Text(root, height=14, width=10)
T1.pack(side=LEFT, fill=Y)
T1.pack(side=TOP, fill=X)

quote1 = "I really liked that blue big beautiful ball my uncle gave me on my birthday."
T1.insert(END, quote1)

#=====================================BUTTON WIDGET========================================
btn_log = Button(TopForm, text="        Check       ", command=loadinp)
btn_log.pack(side=LEFT)

#=====================================INITIALIZATION=======================================
if __name__ == '__main__':
    #Database()
    #Load()
    root.mainloop()

