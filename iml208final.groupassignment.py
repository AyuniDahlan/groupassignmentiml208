from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import sqlite3  as db



def establishconnect():
    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()
    sql = '''
    create table if not exists sell (
        date string,
        product string,
        price number,
        quantity number,
        total number
        )
    '''
    c.execute(sql)
    connectobject.commit()   

establishconnect()    
mainwindow=Tk()
mainwindow.title("Katarsis Club Merchandise")
tab = ttk.Notebook(mainwindow) 
window1= ttk.Frame(tab)
window2=ttk.Frame(tab)

tab.add(window1, text ='STOCK') 
tab.add(window2, text ='SELL') 
tab.pack(expand = 6, fill ="both") 
  

def connection2():
    connectobject2 = db.connect("shopManagement.db")
    c = connectobject2.cursor()
    sql = '''
    create table if not exists stock (
        date string,
        product string,
        price number,
        quantity number
        )
    '''
    c.execute(sql)
    connectobject2.commit()   

connection2() 

def Stock():
    global dateE2,quantity,name,price

    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()  
    sql = '''
            INSERT INTO stock VALUES 
            (?, ?, ?, ?)
            '''
    c.execute(sql,(dateE2.get(),name.get(),price.get(),quantity.get()))
    connectobject.commit() 

def viewingStock():
    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()  

    sql = 'Select * from stock'
    c.execute(sql)

    rows=c.fetchall()
    viewingarea2.insert(END,f"Date \t Product\t  Price\t  Quantity\t \n")
    
    for i in rows:
        allrows=""
        for j in i:
            allrows+=str(j)+'\t'
        allrows+='\n'
        viewingarea2.insert(END,allrows)

def deleteSellItem():
    selected_item = viewingarea.tag_ranges("sel")
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to delete.")
        return

    start, end = selected_item
    start_line, _ = map(int, viewingarea.index(start).split('.'))
    end_line, _ = map(int, viewingarea.index(end).split('.'))

    # Delete the selected lines
    viewingarea.delete(f"{start_line}.0", f"{end_line + 1}.0")

    # Assuming you have an ID column in your sell table
    selected_id = start_line
    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()
    sql = 'DELETE FROM sell WHERE rowid=?'
    c.execute(sql, (selected_id,))

    connectobject.commit()
    messagebox.showinfo("Success", "Sell item deleted successfully.")

delete_button_sell = Button(window2, command=deleteSellItem, text="Delete",
                             font=('Consolas', 18, 'bold'), bg="red", width=20)
delete_button_sell.grid(row=7, column=0, padx=7, pady=7)


def deleteStockItem():
    selected_item = viewingarea.tag_ranges("sel")
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to delete.")
        return

    start, end = selected_item
    start_line, _ = map(int, viewingarea.index(start).split('.'))
    end_line, _ = map(int, viewingarea.index(end).split('.'))

    # Delete the selected lines
    viewingarea.delete(f"{start_line}.0", f"{end_line + 1}.0")

    # Assuming you have an ID column in your stock table
    selected_id = start_line
    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()
    sql = 'DELETE FROM stock WHERE rowid=?'
    c.execute(sql, (selected_id,))

    connectobject.commit()
    messagebox.showinfo("Success", "Stock item deleted successfully.")

delete_button_stock = Button(window1, command=deleteStockItem, text="Delete",
                             font=('Consolas', 18, 'bold'), bg="red", width=20)
delete_button_stock.grid(row=7, column=0, padx=7, pady=7)


dateL=Label(window1,text="Date",width=12,font=('Consolas',18,'bold'))
dateL.grid(row=0,column=0,padx=7,pady=7)

dateE2=DateEntry(window1,width=12,font=('Consolas',15,'bold'))
dateE2.grid(row=0,column=1,padx=7,pady=7)

l1=Label(window1, text="Product",font=('Consolas',18,'bold'),width=12)
l1.grid(row=1,column=0,padx=7,pady=7)

l1=Label(window1, text="Price",font=('Consolas',18,'bold'),width=12)
l1.grid(row=2,column=0,padx=7,pady=7)

l1=Label(window1, text="Quantity",font=('Consolas',18,'bold'),width=12)
l1.grid(row=3,column=0,padx=7,pady=7)

name=StringVar()
price=IntVar()
quantity=IntVar()

Name=Entry(window1,textvariable=name,font=('Consolas',18,'bold'),width=12)
Name.grid(row=1,column=1,padx=7,pady=7)

Price=Entry(window1,textvariable=price,font=('Consolas',18,'bold'),width=12)
Price.grid(row=2,column=1,padx=7,pady=7)

Quantity=Entry(window1,textvariable=quantity,font=('Consolas',18,'bold'),width=12)
Quantity.grid(row=3,column=1,padx=7,pady=7)

addbutton=Button(window1,command=Stock,text="Add",
font=('Consolas',18,'bold'),bg="orange",width=20)

addbutton.grid(row=4,column=1,padx=7,pady=7)

viewingarea2=Text(window1)
viewingarea2.grid(row=5,column=0,columnspan=2)

viewbutton2=Button(window1,command=viewingStock,text="View Stock",
font=('Consolas',18,'bold'),bg="orange",width=20 )

viewbutton2.grid(row=4,column=0,padx=7,pady=7)

def Bill():
    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()  

    global areaforbill
    if p1quant.get()==0 and p2quant.get()==0 and p3quant.get()==0 and p4quant.get()==0:
        messagebox.showerror("Error","No product purchased")
    else:
        areaforbill.delete('1.0',END)
        areaforbill.insert(END,"\t|| Katarsis Club Merchandise ||")
        areaforbill.insert(END,"\n_________________________________________\n")
        areaforbill.insert(END,"\nDate\t Products\tPrice\t   QTY\t Total")
        areaforbill.insert(END,"\n==========================================")

        price= IntVar()
        price2=IntVar()
        price3=IntVar()
        price4=IntVar()

        print(datee.get())
        price=price2=price3=price4=0

        if p1quant.get()!=0:
            price=p1quant.get()*pricep1.get()
            print(price)
            areaforbill.insert(END,f"\n{datee.get()}\t Keychain \t{pricep1.get()}\t {p1quant.get()}\t {price}")

            sql = '''
            INSERT INTO Sell VALUES 
            (?, ?, ?, ?,?)
            '''
            c.execute(sql,(datee.get(),'Keychain',pricep1.get(),p1quant.get(),price))
            connectobject.commit() 

        if p2quant.get()!=0:
            price2=(p2quant.get()*pricep2.get())
            print(price2)
            areaforbill.insert(END,f"\n{datee.get()}\t Lanyard \t{pricep2.get()}\t {p2quant.get()}\t {price2}")

            sql = '''
            INSERT INTO Sell VALUES 
            (?, ?, ?, ?,?)
            '''
            print(datee.get(),'Lanyard',pricep2.get(),p2quant.get(),price2)
            c.execute(sql,(datee.get(),'Lanyard',pricep2.get(),p2quant.get(),price2))
            connectobject.commit() 

        if p3quant.get()!=0:
            price3=p3quant.get()*pricep1.get()
            print(price3)
            areaforbill.insert(END,f"\n{datee.get()}\t Notebook \t{pricep3.get()}\t {p3quant.get()}\t {price3}")

            sql = '''
            INSERT INTO Sell VALUES 
            (?, ?, ?, ?,?)
            '''
            c.execute(sql,(datee.get(),'Notebook',pricep3.get(),p3quant.get(),price3))
            connectobject.commit() 

        if p4quant.get()!=0:
            price4=p4quant.get()*pricep1.get()
            areaforbill.insert(END,f"\n{datee.get()}\t T-shirt \t{pricep4.get()}\t {p4quant.get()}\t {price4}")

            sql = '''
            INSERT INTO Sell VALUES 
            (?, ?, ?, ?,?)
            '''
            c.execute(sql,(datee.get(),'T-shirt',pricep4.get(),p4quant.get(),price4))
            connectobject.commit() 

        Total=IntVar()
        Total=price+price2+price3+price4

        quantity=IntVar()
        quantity=p1quant.get()+p2quant.get()+p3quant.get()+p4quant.get()
        areaforbill.insert(END,f"\nTotal \t \t  \t{quantity}\t {Total}")


def view():
    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()  

    sql = 'Select * from Sell'
    c.execute(sql)

    rows=c.fetchall()
    viewingarea.insert(END,f"Date\t Product\t  Price of 1\t  Quantity\t  Price\n")
    
    
    for i in rows:
        allrows=""
        for j in i:
            allrows+=str(j)+'\t'
        allrows+='\n'
        viewingarea.insert(END,allrows)

def save_sell_data():
    connectobject = db.connect("shopManagement.db")
    c = connectobject.cursor()

    sql = 'Select * from sell'
    c.execute(sql)

    rows = c.fetchall()

    data_to_save = "Date\tProduct\tPrice\tQuantity\tTotal\n"

    for row in rows:
        data_to_save += "\t".join(map(str, row)) + "\n"

    save_data_to_file(data_to_save, "sell_data.txt")

def save_data_to_file(data, filename):
    try:
        with open(filename, 'w') as file:
            file.write(data)
        messagebox.showinfo("Save Successful", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error during save operation: {e}")

save_button = Button(window2, command=save_sell_data, text="Save Sell Data",
                     font=('Consolas', 18, 'bold'), bg="orange", width=20)
save_button.grid(row=7, column=1, pady=10)


datel=Label(window1,text="Date",width=12,font=('Consolas',15,'bold'))
datel.grid(row=0,column=0,padx=7,pady=7)

datee=DateEntry(window1,width=12,font=('Consolas',15,'bold'))
datee.grid(row=0,column=1,padx=7,pady=7)

l1=Label(window1, text="Product Name",font=('Consolas',18,'bold'),width=12)
l1.grid(row=1,column=0,padx=7,pady=7)


namep1=StringVar()
namep1.set('Keychain')

pricep1=IntVar()
pricep1.set(8)

p1quant=IntVar()
p1quant.set(0)

l1=Label(window2, text=namep1.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=2,column=0,padx=7,pady=7)

l1=Label(window2, text=pricep1.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=2,column=1,padx=7,pady=7)

t1=Entry(window2,textvariable=p1quant,font=('Consolas',18,'bold'),width=12)
t1.grid(row=2,column=2,padx=7,pady=7)


namep2=StringVar()
namep2.set('Lanyard')

pricep2=IntVar()
pricep2.set(15)

p2quant=IntVar()
p2quant.set(0)

l1=Label(window2, text=namep2.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=3,column=0,padx=7,pady=7)

l1=Label(window2, text=pricep2.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=3,column=1,padx=7,pady=7)

t1=Entry(window2,textvariable=p2quant,font=('Consolas',18,'bold'),width=12)
t1.grid(row=3,column=2,padx=7,pady=7)

namep3=StringVar()
namep3.set('Notebook')

pricep3=IntVar()
pricep3.set(25)

p3quant=IntVar()
p3quant.set(0)

l1=Label(window2, text=namep3.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=4,column=0,padx=7,pady=7)

l1=Label(window2, text=pricep3.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=4,column=1,padx=7,pady=7)

t1=Entry(window2,textvariable=p3quant,font=('Consolas',18,'bold'),width=12)
t1.grid(row=4,column=2,padx=7,pady=7)


namep4=StringVar()
namep4.set('T-shirt')

pricep4=IntVar()
pricep4.set(50)

p4quant=IntVar()
p4quant.set(0)

l1=Label(window2, text=namep4.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=5,column=0,padx=7,pady=7)

l1=Label(window2, text=pricep4.get(),font=('Consolas',18,'bold'),width=12)
l1.grid(row=5,column=1,padx=7,pady=7)

t1=Entry(window2,textvariable=p4quant,font=('Consolas',18,'bold'),width=12)
t1.grid(row=5,column=2,padx=7,pady=7)


areaforbill=Text(window2)

submitbutton=Button(window2,command=Bill,text="Bill",
font=('Consolas',18,'bold'),bg="orange",width=20 )

submitbutton.grid(row=6,column=2,padx=7,pady=7)

viewbutton=Button(window2,command=view,text="View All Sellings",
font=('Consolas',18,'bold'),bg="orange",width=20 )

viewbutton.grid(row=6,column=0,padx=7,pady=7)

areaforbill.grid(row=9,column=2)
viewingarea=Text(window2)
viewingarea.grid(row=9,column=0)

mainloop()