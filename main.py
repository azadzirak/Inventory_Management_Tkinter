from os import system
system("cls")
from tkinter import Tk,Label,Entry,Button,messagebox,simpledialog,Toplevel,Frame
from shop_module import Product,Shop,Sales
shop=Tk()
shop.title("Tehran Shop:")
shop.geometry("800x500")
shop.resizable(True,True)
shop.configure(bg="black")
form_frame=Frame(shop,bg="black")
form_frame.pack(pady=10)
Label(form_frame,text="Name:",bg="black",fg="white",font=("Arial",12,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="e")
name=Entry(form_frame,font=("Arial",12),fg="black",bd=3)
name.grid(row=0,column=1,padx=5,pady=5)
Label(form_frame,text="Price1:",bg="black",fg="white",font=("Arial",12,"bold")).grid(row=1,column=0,padx=5,pady=5,sticky="e")
price1=Entry(form_frame,font=("Arial",12),fg="black",bd=3)
price1.grid(row=1,column=1,padx=5,pady=5)
Label(form_frame,text="Price2:",bg="black",fg="white",font=("Arial",12,"bold")).grid(row=2,column=0,padx=5,pady=5,sticky="e")
price2=Entry(form_frame,font=("Arial",12),fg="black",bd=3)
price2.grid(row=2,column=1,padx=5,pady=5)
Label(form_frame,text="Stock:",bg="black",fg="white",font=("Arial",12,"bold")).grid(row=3,column=0,padx=5,pady=5,sticky="e")
stock=Entry(form_frame,font=("Arial",12),fg="black",bd=3)
stock.grid(row=3,column=1,padx=5,pady=5)
button_frame=Frame(shop,bg="black")
button_frame.pack(pady=15)
def save():
    p=Product(name.get(),price1.get(),price2.get(),stock.get())
    s=Shop()
    if s.save(p):
        messagebox.showinfo("Success","Product saved.")
        name.delete(0,"end")
        price1.delete(0,"end")
        price2.delete(0,"end")
        stock.delete(0,"end")
    else:
        messagebox.showerror("Error","Invalid product.")    
Button(button_frame,text="Add",font=("arial",11,"bold"),bg="blue",fg="white",
        command=save).pack(side="left",padx=5)
def search():
    item_name=simpledialog.askstring("Search","Enter product name:")
    if not item_name:
        return
    s=Shop()
    result=s.search(item_name)
    if result:
        messagebox.showinfo("Found",result)
    else:
        messagebox.showerror("Not Found","Product not found.")
Button(button_frame,text="Search",font=("arial",11,"bold"),bg="blue",fg="white",
        command=search).pack(side="left",padx=5)
def available():
    s=Shop()
    items=s.list_all()
    if items:
        text="\n".join(item.strip().replace("\t","  |  ") for item in items)
        messagebox.showinfo("Available Products",text)
Button(button_frame,text="Available",font=("arial",11,"bold"),bg="blue",fg="white",
        command=available).pack(side="left",padx=5)
def sell():
    sell_win=Toplevel()
    sell_win.title("Sell Product")
    sell_win.geometry("400x300")
    sell_win.configure(bg="black")
    Label(sell_win,text="Product Name:",fg="white",bg="black").pack(pady=5)
    name_entry=Entry(sell_win)
    name_entry.pack(pady=5)
    Label(sell_win,text="Quantity:",fg="white",bg="black").pack(pady=5)
    qty_entry=Entry(sell_win)
    qty_entry.pack(pady=5)
    def submit_sale():
        name=name_entry.get()
        quantity=qty_entry.get()
        if not name or not quantity:
            messagebox.showerror("Error","All fields required.")
            return
        if not quantity.isdigit():
            messagebox.showerror("Error","'Quantity must be a number.")
            return
        confirm=messagebox.askyesno("Confirm Sale",f"Sell {quantity} of '{name}'?")
        if not confirm:
            return
        s=Sales()
        if s.sell(name,quantity):
            messagebox.showinfo("Success","Product sold.")
            sell_win.destroy()
        else:
            messagebox.showerror("Error","Sale failes.")
    Button(sell_win,text="Sell it",bg="blue",fg="white",command=submit_sale).pack(pady=15)
Button(button_frame,text="Sell",font=("arial",11,"bold"),bg="blue",fg="white",
        command=sell).pack(side="left",padx=5)
def report():
    s=Sales()
    s.report()
Button(button_frame,text="Report",font=("arial",11,"bold"),bg="blue",fg="white",
        command=report).pack(side="left",padx=5)
def edit():
    item_name=simpledialog.askstring("Edit","Enter product name to edit:")
    if not item_name:
        return
    s=Shop()
    lines=s.list_all()
    for line in lines:
        parts=line.strip().split("\t")
        if len(parts)!=4:
            continue
        pname,p1,p2,stock=parts
        if pname.lower()==item_name.lower():
            edit_win=Toplevel()
            edit_win.title("Edit Product")
            edit_win.geometry("400x300")
            edit_win.configure(bg="black")
            Label(edit_win,text="New Price1:",fg="white",bg="black").pack(pady=5)
            price1_entry=Entry(edit_win)
            price1_entry.insert(0,p1)
            price1_entry.pack(pady=5)
            Label(edit_win,text="New Price2:",fg="white",bg="black").pack(pady=5)
            price2_entry=Entry(edit_win)
            price2_entry.insert(0,p2)
            price2_entry.pack(pady=5)
            Label(edit_win,text="New Stock:",fg="white",bg="black").pack(pady=5)
            stock_entry=Entry(edit_win)
            stock_entry.insert(0,stock)
            stock_entry.pack(pady=5)
            def apply_edit():
                np1=price1_entry.get()
                np2=price2_entry.get()
                nstock=stock_entry.get()
                if not all([np1,np2,nstock]):
                    messagebox.showerror("Error","All fields required.")
                    return
                if not(np1.replace(".", "").isdigit() and np2.replace(".", "").isdigit() and nstock.isdigit()):
                    messagebox.showerror("Error","Values must be numeric.")
                    return
                if s.edit_product(item_name,np1,np2,nstock):
                    messagebox.showinfo("Success","Product edited.")
                    edit_win.destroy()
                else:
                    messagebox.showerror("Error","Failed to edit.") 
            Button(edit_win,text="Apply",command=apply_edit,bg="blue",fg="white").pack(pady=10)
            return
    messagebox.showerror("Not Found","Product not found.")               
Button(button_frame,text="Edit",font=("arial",11,"bold"),bg="blue",fg="white",
       command=edit).pack(side="left",padx=5)
def delete():
    item_name=simpledialog.askstring("Delete","Enter product name to delete:")
    if not item_name:
        return
    confirm=messagebox.askyesno("Confirm Delete",f"Are you sure you want to delete '{item_name}'?")
    if not confirm:
        return
    s=Shop()
    if s.delete_product(item_name):
        messagebox.showinfo("Success","Product deleted.")
    else:
        messagebox.showerror("Error","Product not found or deletion failed.")
Button(button_frame,text="Delete",font=("arial",11,"bold"),bg="blue",fg="white",
       command=delete).pack(side="left",padx=5)
def clear():
    name.delete(0,"end")
    price1.delete(0,"end")
    price2.delete(0,"end")
    stock.delete(0,"end")
Button(button_frame,text="Clear",font=("arial",11,"bold"),bg="blue",fg="white",
        command=clear).pack(side="left",padx=5)
def exitform():
    if messagebox.askyesno("Exit","Are you sure you want to exit?"):
        shop.destroy()
Button(button_frame,text="Exit",font=("arial",11,"bold"),bg="red",fg="white",
        command=exitform).pack(side="left",padx=5)
shop.mainloop()