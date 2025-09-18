from os import system
system("cls")
import matplotlib.pyplot as plt
class Product:
    def __init__(self,name,price1,price2,stock):
        self.name=name
        self.price1=float(price1)
        self.price2=float(price2)
        self.stock=int(stock)
    def is_valid(self):
        return self.price2>=self.price1 and self.stock>=0
    def to_line(self):
        return f"{self.name}\t{self.price1}\t{self.price2}\t{self.stock}\n"
class Shop():
    def __init__(self,filename="TehranShop.txt"):
        self.filename=filename
    def save(self,product:Product):
        if not product.is_valid():
            return False
        with open(self.filename,"a") as file:
            file.write(product.to_line())
        return True
    def search(self,name):
        try:
            with open(self.filename,"r") as file:
                for line in file:
                    if name.lower() in line.lower():
                        return line.strip()
        except FileNotFoundError:
            return None
        return None
    def list_all(self):
        try:
            with open(self.filename,"r") as file:
                return file.readlines()
        except FileNotFoundError:
            return []
    def edit_product(self,name,new_price1,new_price2,new_stock):
        try:
            updated_lines=[]
            edited=False
            with open(self.filename,"r") as file:
                lines=file.readlines()
            for line in lines:
                parts=line.strip().split("\t")
                if len(parts)!=4:
                    updated_lines.append(line)
                    continue
                pname=parts[0]
                if pname.lower()==name.lower():
                    new_line=f"{pname}\t{new_price1}\t{new_price2}\t{new_stock}\n"
                    updated_lines.append(new_line)
                    edited=True
                else:
                    updated_lines.append(line)
            if edited:
                with open(self.filename,"w") as file:
                    file.writelines(updated_lines)
                return True
            return False
        except FileNotFoundError:
            return False
    def delete_product(self,name):
        try:
            updated_lines=[]
            deleted=False
            with open(self.filename,"r") as file:
                lines=file.readlines()
            for line in lines:
                if name.lower() not in line.lower():
                    updated_lines.append(line)
                else:
                    deleted=True
            if deleted:
                with open(self.filename,"w") as file:
                    file.writelines(updated_lines)
                return True
            return False
        except FileNotFoundError:
            return False
class Sales(Shop):
    def __init__(self,filename="TehranShop.txt",sales_file="sales.txt"):
        super().__init__(filename)
        self.sales_file=sales_file
    def sell(self,name,quantity):
        try:
            quantity=int(quantity)
            with open(self.filename,"r") as file:
                lines=file.readlines()
            updated_lines=[]
            sold=False
            for line in lines:
                parts=line.strip().split("\t")
                if len(parts)!=4:
                    updated_lines.append(line)
                    continue
                pname,p1,p2,stock=parts
                if pname.lower()==name.lower():
                    if int(stock)<quantity:
                        return False
                    new_stock=int(stock)-quantity
                    updated_lines.append(f"{pname}\t{p1}\t{p2}\t{new_stock}\n")
                    with open(self.sales_file,"a") as sf:
                        sf.write(f"{pname}\t{quantity}\t{p2}\t{p2*quantity}\n")
                    sold=True
                else:
                    updated_lines.append(line)  
            if sold:
                with open(self.filename,"w") as file:
                    file.writelines(updated_lines)
                return True
            return False  
        except FileNotFoundError:
            return False
    def report(self):
        try:
            with open(self.sales_file,"r") as file:
                lines=file.readlines()
            product_quantities={}
            product_revenues={}
            for line in lines:
                parts=line.strip().split("\t")
                if len(parts)<4:
                    continue
                name=parts[0]
                quantity=int(parts[1])
                price=float(parts[2])
                total=quantity*price
                product_quantities[name]=product_quantities.get(name,0)+quantity
                product_revenues[name]=product_revenues.get(name,0)+total
        except FileNotFoundError:
            return
        x=list(product_quantities.keys())
        y=list(product_quantities.values())
        revenues=list(product_revenues.values())
        plt.figure(figsize=(10,6))
        bars=plt.bar(x,y,color="purple",edgecolor="black",linewidth=1.5)
        plt.title("Sales Report",fontsize=14,fontweight="bold",color="navy")
        plt.xlabel("Products",fontsize=12)
        plt.ylabel("Quantity Sold",fontsize=12)
        plt.grid(True,linestyle="--",alpha=0.4)
        for bar,revenue in zip(bars,revenues):
            plt.text(bar.get_x()+bar.get_width()/2,
                     bar.get_height(),
                     f"{revenue:.0f} T",
                     ha="center",va="bottom",
                     fontsize=10,fontweight="bold",
                     color="black")
        plt.xticks(rotation=30) 
        plt.tight_layout()
        plt.show()