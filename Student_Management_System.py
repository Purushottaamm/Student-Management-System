import bs4
import socket
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

root = Tk()
root.title("S. M. S")
root.geometry("500x500+350+100")


# add student
def f1():
    addStu.deiconify()
    root.withdraw()


# deiconify add student
def f2():
    root.deiconify()
    addStu.withdraw()


# del student
def f6():
    delStu.deiconify()
    root.withdraw()


# deiconify del student
def f7():
    root.deiconify()
    delStu.withdraw()


# update student
def f8():
    updStu.deiconify()
    root.withdraw()


# deiconify update student
def f9():
    root.deiconify()
    updStu.withdraw()


# Temperature

def f13():
    try:
        cities = lblctn.get()
        socket.create_connection(("www.google.com", 80))
        a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
        a2 = "&q=" + cities
        a3 = "&appid=c6e315d09197cec231495138183954bd"
        api_address = a1 + a2 + a3
        res1 = requests.get(api_address)
        j1 = res1.json()
        d1 = j1['main']
        temp = d1['temp']
        showTemp.insert(INSERT, str(temp))
    except OSError:
        print("check network")


# del and focus temp
def f15():
    lblctn.delete(0, END)
    showTemp.delete(0, END)
    lblctn.focus()


# GRAPH

Graph = Toplevel(root)
Graph.title("Graph")
Graph.geometry("600x400+200+200")
Graph.withdraw()


def f14():
    import cx_Oracle
    con = None
    cursor = None

    try:
        con = cx_Oracle.connect("system/abc123")
        cursor = con.cursor()
        cursor.execute("select count(*) from studf")
        for row in cursor:
            totalstudents = row[0]
        t = np.arange(totalstudents)
        cursor.execute("select sid,smarks from studf")

        sid = []
        smarks = []

        for row in cursor:
            sid.append(row[0])
            smarks.append(row[1])

        bar_width = 0.5
        plt.bar(t, smarks, bar_width)
        plt.xticks(t, sid)
        plt.xlabel("Sid")
        plt.ylabel("Smarks")
        plt.title("Student Info")
        plt.legend()
        plt.grid()

        xs = [x for x in range(0, totalstudents)]
        for x, y in zip(xs, smarks):
            plt.annotate(smarks[x], (x - bar_width / 2, y))

        plt.show()

    except cx_Oracle.DatabaseError as e:
        con.rollback()
        messagebox.showerror("Failure ", e)


# view student
viewStu = Toplevel(root)
viewStu.title("View Student")
viewStu.geometry("500x400+200+200")
viewStu.withdraw()


def f4():
    st.delete(1.0, END)
    root.deiconify()
    viewStu.withdraw()


st = scrolledtext.ScrolledText(viewStu, width=30, height=5)
btnViewBack = Button(viewStu, text="Back", command=f4)
st.pack(pady=10)
btnViewBack.pack(pady=10)


def f3():
    viewStu.deiconify()
    root.withdraw()

    import cx_Oracle
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        print("u r connected ")
        cursor = con.cursor()
        sql = "select * from studf"
        cursor.execute(sql)
        data = cursor.fetchall()
        mdata = ""
        for d in data:
            mdata = mdata + str(d[0]) + " " + d[1] + " " + str(d[2]) + "\n"
        st.insert(INSERT, mdata)
    except cx_Oracle.DatabaseError as e:
        print("issue ", e)
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
            print("U r disconnected ")


btnAdd = Button(root, text="Add", width=20, command=f1)
btnView = Button(root, text="View", width=20, command=f3)
btnUpdate = Button(root, text="Update", width=20, command=f8)
btnDelete = Button(root, text="Delete", width=20, command=f6)
btnGraph = Button(root, text="Graphical Statistics", width=20, command=f14)

# quote of the day

res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
print(res)

soup = bs4.BeautifulSoup(res.text, 'lxml')

quote = soup.find('img', {"class": "p-qotd"})
print(quote)

text = quote['alt']
lbl1 = Label(root, text="Quote of the day : ")
lblQuote = scrolledtext.ScrolledText(root, width=60, height=3)
lblQuote.insert(INSERT, text)

lblTemp = Label(root, text="Check Temperature ")
lblctne = Label(root, text="Enter City Name : ")
lblctn = Entry(root, bd=5)
lblTemp1 = Label(root, text="Today's Temperature ")
showTemp = Entry(root, bd=5)
btnCheck = Button(root, text="Check Temp", command=f13)
btnCheckagain = Button(root, text="Check Again", command=f15)

btnAdd.pack(pady=5)
btnView.pack(pady=5)
btnUpdate.pack(pady=5)
btnDelete.pack(pady=5)
btnGraph.pack(pady=10)
lbl1.pack()
lblQuote.pack(pady=10)
lblTemp.pack(pady=10)
lblctne.pack()
lblctn.pack()
lblTemp1.pack()
showTemp.pack()
btnCheck.pack(pady=5)
btnCheckagain.pack()

# ADD

addStu = Toplevel(root)
addStu.title("Add Student")
addStu.geometry("500x400+200+200")
addStu.withdraw()

lbladdSid = Label(addStu, text="Enter Roll no.")
entaddSid = Entry(addStu, bd=5)
lbladdSname = Label(addStu, text="Enter Name")
entaddSname = Entry(addStu, bd=5)
lbladdSmarks = Label(addStu, text="Enter Marks")
entaddSmarks = Entry(addStu, bd=5)


def f5():
    import cx_Oracle
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        print("u r connected ")
        cursor = con.cursor()
        sql = "insert into studf values(%d,'%s',%d)"

        sid = entaddSid.get()
        if sid.isdigit() and int(sid) > 0:
            sid = int(sid)
        else:
            messagebox.showerror("Error", "Enter a valid id")
            entaddSid.delete(0, END)
            entaddSid.focus()
            return

        sname = entaddSname.get()
        if sname.isalpha() and len(sname) > 1:
            sname = sname
        else:
            messagebox.showerror("Error", "Enter valid name(min 2 letters)")
            entaddSname.delete(0, END)
            entaddSname.focus()
            return

        smarks = entaddSmarks.get()
        if smarks.isdigit() and int(smarks) > 0 and int(smarks) < 101:
            smarks = int(smarks)
        else:
            messagebox.showerror("Error", "Enter +ve marks(0-100)")
            entaddSmarks.delete(0, END)
            entaddSmarks.focus()
            return

        args = (sid, sname, smarks)
        cursor.execute(sql % args)

        msg = str(cursor.rowcount) + " records inserted "
        messagebox.showinfo("Success", msg)
        entaddSid.delete(0, END)
        entaddSid.focus()
        entaddSname.delete(0, END)
        entaddSname.focus()
        entaddSmarks.delete(0, END)
        entaddSmarks.focus()
        con.commit()

    except ValueError:
        messagebox.showerror('gadbad hai ')
        entaddSid.delete(0, END)
        entaddSid.focus()
        entaddSname.delete(0, END)
        entaddSname.focus()
        entaddSmarks.delete(0, END)
        entaddSmarks.focus()

    except cx_Oracle.DatabaseError as e:
        con.rollback()
        messagebox.showerror("Failure ", e)
        entaddSid.delete(0, END)
        entaddSid.focus()
        entaddSname.delete(0, END)
        entaddSname.focus()
        entaddSmarks.delete(0, END)
        entaddSmarks.focus()
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
            print("U r disconnected ")


btnAddSave = Button(addStu, text="Save", command=f5)

btnAddBack = Button(addStu, text="Back", command=f2)

lbladdSid.pack(pady=10)
entaddSid.pack(pady=10)
lbladdSname.pack(pady=10)
entaddSname.pack(pady=10)
lbladdSmarks.pack(pady=10)
entaddSmarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

# UPDATE

updStu = Toplevel(root)
updStu.title("Update Student")
updStu.geometry("500x400+200+200")
updStu.withdraw()

lblUpdSid = Label(updStu, text="Enter Rno.")
entUpdSid = Entry(updStu, bd=5)
lblUpdSname = Label(updStu, text="Enter Name")
entUpdSname = Entry(updStu, bd=5)
lblUpdSmarks = Label(updStu, text="Enter Marks")
entUpdSmarks = Entry(updStu, bd=5)


def f6():
    import cx_Oracle
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        print("u r connected ")
        cursor = con.cursor()
        sql = "update studf set sid='%d',sname='%s',smarks='%d' where sid='%d'"
        sid = entUpdSid.get()
        if sid.isdigit() and int(sid) > 0:
            sid = int(sid)
        else:
            messagebox.showerror("Error", "Enter a valid id")
            entUpdSid.delete(0, End)
            entUpdSid.focus()
            return

        sname = entUpdSname.get()
        if sname.isalpha() and len(sname) > 1:
            sname = sname
        else:
            messagebox.showerror("Error", "Enter valid name (min 2 letters)")
            entUpdSname.delete(0, End)
            entUpdSname.focus()
            return

        smarks = entUpdSmarks.get()
        if smarks.isdigit() and int(smarks) > 0 and int(smarks) < 101:
            smarks = int(smarks)
        else:
            messagebox.showerror("Error", "Enter a positive marks(0-100)")
            entUpdSmarks.delete(0, End)
            entUpdSmarks.focus()
            return

        args = (sid, sname, smarks, sid)
        cursor.execute(sql % args)
        con.commit()
        msg = str(cursor.rowcount) + " records updated "
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "not present")
            entUpdSid.delete(0, END)
            entUpdSid.focus()
        else:
            messagebox.showinfo("Success", msg)
        entUpdSid.delete(0, END)
        entUpdSid.focus()
        entUpdSname.delete(0, END)
        entUpdSname.focus()
        entUpdSmarks.delete(0, END)
        entUpdSmarks.focus()
    except cx_Oracle.DatabaseError as e:
        con.rollback()
        #		messagebox.showerror("Failure ",e)
        #		entUpdSid.delete(0,END)
        #		entUpdSid.focus()
        entUpdSname.delete(0, END)
        entUpdSname.focus()
        entUpdSmarks.delete(0, END)
        entUpdSmarks.focus()
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
            print("U r disconnected ")


btnUpdSave = Button(updStu, text="Save", command=f6)

btnUpdBack = Button(updStu, text="Back", command=f9)

lblUpdSid.pack(pady=10)
entUpdSid.pack(pady=10)
lblUpdSname.pack(pady=10)
entUpdSname.pack(pady=10)
lblUpdSmarks.pack(pady=10)
entUpdSmarks.pack(pady=10)
btnUpdSave.pack(pady=10)
btnUpdBack.pack(pady=10)

# DELETE

delStu = Toplevel(root)
delStu.title("Delete Student")
delStu.geometry("500x400+200+200")
delStu.withdraw()

lbldelSid = Label(delStu, text="Enter Rno.")
entdelSid = Entry(delStu, bd=5)


def f12():
    import cx_Oracle
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        print("u r connected ")
        cursor = con.cursor()
        sql = "delete from studf where sid=%s"
        sid = entdelSid.get()
        if sid.isdigit() and int(sid) > 0:
            sid = int(sid)
        else:
            messagebox.showerror("Error", "Enter a valid id")
            entdelSid.delete(0, END)
            entdelSid.focus()

        args = (sid)
        cursor.execute(sql % args)
        con.commit()
        msg = str(cursor.rowcount) + " records updated "
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "not present")
            entdelSid.delete(0, END)
            entdelSid.focus()
        else:
            messagebox.showinfo("Success", msg)

        entdelSid.delete(0, END)
        entdelSid.focus()


    except cx_Oracle.DatabaseError as e:
        con.rollback()
    #		messagebox.showerror("Failure ",e)
    #		entdelSid.delete(0,END)
    #		entdelSid.focus()
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
            print("U r disconnected ")


btnDelSave = Button(delStu, text="Save", command=f12)

btnDelBack = Button(delStu, text="Back", command=f7)

lbldelSid.pack(pady=10)
entdelSid.pack(pady=10)
btnDelSave.pack(pady=10)
btnDelBack.pack(pady=10)

root.mainloop()