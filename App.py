import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
class DataBase:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine) 

    def connect(self):
        self.session = self.Session()

    def disconnect(self):
        self.session.close()

    def executeQuery(self, query):

        if self.session is None:
            raise Exception ("No se establecio una coneccion. Llama al metodo connect")
        
        result = self.session.execute(query)
        return result.fetchall()

class MyPlotFrame(customtkinter.CTkScrollableFrame):
    def __init__(self,master,title, xData, yData, desc ):
        super().__init__(master)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        self.title = title
        self.desc = desc
        self.figure, self.ax = plt.subplots()
        
        xData = [item[0] for item in xData]
        yData = [item[0] for item in yData]

        self.ax.bar(xData, yData)
        

        self.ax.set_xticks(range(len(xData)))
        self.ax.set_xticklabels(xData, rotation=15, ha='right', fontsize="small")
        self.ax.grid()
        self.ax.yaxis.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.8)  
        self.ax.xaxis.grid(color="none")

        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()   
        
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0,column=0,padx=10,pady=(10,0), sticky="ew")

        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=(10,0), sticky="ew")

        textBox = customtkinter.CTkTextbox(self, fg_color="gray30", corner_radius=6, cursor="arrow")
        textBox.insert(index="0.0",text=self.desc)
        textBox.configure(state="disable")
        textBox.grid(row=3, column=0, padx=10, pady=(15,0), sticky="nsew",)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        self.title("Adventure Works Data Visualization App")
        self.geometry("1080x990")
        self.grid_rowconfigure((0,1),weight=1)
        self.grid_columnconfigure((0,1),weight=1)

        db = DataBase("mssql+pyodbc://LAPTOP-MGLHUKHT/DWAdventureWorks?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
        db.connect()

        result1 = db.executeQuery(text('SELECT ter.Nombreterritorio FROM DimTerritorio as ter ORDER BY ter.Nombreterritorio'))
        result2 = db.executeQuery(text('SELECT CAST(SUM(ord.TotalOrden) AS INTEGER) as Total_Ventas FROM DimTerritorio as ter INNER JOIN Hechos_Ordenes AS ord ON ter.IDTerritorio = ord.IDTerritorio GROUP BY ter.Nombreterritorio'))

        self.MyPlotFrame1 = MyPlotFrame(self, title="Ventas Por Territorio", xData=result1, yData=result2 ,desc="En este gráfico se muestran las ventas en los territorios. Southwest es el territorio con mayor cantidad de ventas con $20,832,037, mientras que Australia es el territorio con menor cantidad de ventas con tan solo $1,801,970. Es una diferencia \nde $19,030,067.")
        self.MyPlotFrame1.grid(row=0,column=0,padx=10,pady=(10,0), sticky="nsew")

        result1 = db.executeQuery(text('SELECT TOP 10 pro.NombreProducto FROM DimProductos as pro INNER JOIN DimDetalles_Orden as deo ON pro.IDProducto = deo.IDProducto INNER JOIN Hechos_Ordenes as ord ON deo.IDOrden = ord.IDOrden GROUP BY pro.NombreProducto ORDER BY SUM(ord.TotalOrden) DESC;'))
        result2 = db.executeQuery(text('SELECT TOP 10 CAST(SUM(ord.TotalOrden) AS INTEGER) as totalVentas FROM DimProductos as pro INNER JOIN DimDetalles_Orden as deo ON pro.IDProducto = deo.IDProducto INNER JOIN Hechos_Ordenes as ord ON deo.IDOrden = ord.IDOrden GROUP BY pro.NombreProducto ORDER BY totalVentas DESC;'))


        self.MyPlotFrame2 = MyPlotFrame(self, title="Top 10 Productos Más Vendidos", xData=result1, yData=result2 ,desc="En este gráfico se muestran los 10 productos con mayor cantidad de ventas. El producto con mayor cantidad de ventas AWC Logo Cap con $47,868,813. Dentro del top 10 se aprecia que hay 3 productos de similares características, Sport-100 Helmet donde su única diferencia es el color del casco, es decir que los cascos deportivos en específico el Sport-100 Helmet es sin duda el producto estrella de la empresa.")
        self.MyPlotFrame2.grid(row=0,column=1,padx=10,pady=(10,0), sticky="nsew")
        
        result1 = db.executeQuery(text("SELECT TOP 10 CONCAT(emp.Primer_Nombre,' ' ,emp.Apellido) AS Nombre_Completo FROM DimEmpleados as emp INNER JOIN Hechos_Ordenes as ord ON emp.IDEmpleado = ord.IDEmpleado GROUP BY emp.Primer_Nombre, emp.Apellido ORDER BY SUM(ord.TotalOrden) DESC;"))
        result2 = db.executeQuery(text('SELECT TOP 10 SUM(ord.TotalOrden) as total_Ventas FROM DimEmpleados as emp INNER JOIN Hechos_Ordenes as ord ON emp.IDEmpleado = ord.IDEmpleado GROUP BY emp.Primer_Nombre, emp.Apellido ORDER BY total_Ventas DESC;'))


        self.MyPlotFrame3 = MyPlotFrame(self, title="Top 10 Empleados Con Mayores Ventas", xData=result1, yData=result2 , desc="El gráfico muestra los 10 empleados con mayor cantidad de ventas, Linda Mitchell lidera en el total de ventas con un valor de $11,695,019. Se puede analizar que la diferencia con su perseguidor Jillian Mitchell es de $352,634.") 
        self.MyPlotFrame3.grid(row=1,column=0,padx=10,pady=(10,0), sticky="nsew")

        result1 = db.executeQuery(text("SELECT TOP 10 CONCAT(cli.Primer_Nombre, ' ', cli.Apellido) AS Nombre_Completo FROM DimClientes AS cli INNER JOIN Hechos_Ordenes as ord ON cli.IDCliente = ord.IDCliente GROUP BY cli.Primer_Nombre, cli.Apellido ORDER BY SUM(ord.TotalOrden) DESC;"))
        result2 = db.executeQuery(text('SELECT TOP 10 CAST(SUM(ord.TotalOrden) AS INTEGER) as total_Ventas FROM DimClientes AS cli INNER JOIN Hechos_Ordenes as ord ON cli.IDCliente = ord.IDCliente GROUP BY cli.Primer_Nombre, cli.Apellido ORDER BY SUM(ord.TotalOrden) DESC;'))


        self.MyPlotFrame4 = MyPlotFrame(self, title="Top 10 Clientes Con Mayores Compras", xData=result1, yData=result2 , desc=" En el siguiente gráfico se puede ver los 10 clientes que han gastado más en los productos. Roger Harui es el cliente top 1 con un valor total de $989,184. Las ganancias que se han generado de las compras de los top 10 clientes son de $9,342,196.")
        self.MyPlotFrame4.grid(row=1,column=1,padx=10,pady=(10,0), sticky="nsew")

        db.disconnect()

app = App()
app.mainloop()