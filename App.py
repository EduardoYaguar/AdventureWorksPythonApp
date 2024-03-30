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
        #Puedo hacer la creación del objeto con el matplot en blanco y a traves de metodos hago los cambios de valores
        
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

        x = []
        y = []
        self.title("Adventure Works Data Visualization App")
        self.geometry("1080x990")
        self.grid_rowconfigure((0,1),weight=1)
        self.grid_columnconfigure((0,1),weight=1)

        db = DataBase("mssql+pyodbc://LAPTOP-MGLHUKHT/DWAdventureWorks?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
        db.connect()
        result1 = db.executeQuery(text('SELECT ter.Nombreterritorio FROM DimTerritorio as ter ORDER BY ter.Nombreterritorio'))
        for rows in result1:
            x.extend(rows)
        result2 = db.executeQuery(text('SELECT CAST(SUM(ord.TotalOrden) AS INTEGER) as Total_Ventas FROM DimTerritorio as ter INNER JOIN Hechos_Ordenes AS ord ON ter.IDTerritorio = ord.IDTerritorio GROUP BY ter.Nombreterritorio'))
        for rows in result2:
            value = int(rows[0])
            y.append(value)
        

        self.MyPlotFrame1 = MyPlotFrame(self, title="Ventas por territorio 2014", xData=result1, yData=result2 ,desc="Lorem ipsvolutpat. Integer s tempus finibu massa purus, rhoncus et diam.")
        self.MyPlotFrame1.grid(row=0,column=0,padx=10,pady=(10,0), sticky="nsew")

        result1 = db.executeQuery(text('SELECT TOP 10 pro.NombreProducto FROM DimProductos as pro INNER JOIN DimDetalles_Orden as deo ON pro.IDProducto = deo.IDProducto INNER JOIN Hechos_Ordenes as ord ON deo.IDOrden = ord.IDOrden GROUP BY pro.NombreProducto ORDER BY SUM(ord.TotalOrden) DESC;'))
        x = []
        for rows in result1:
            x.extend(rows)
        y = []
        result2 = db.executeQuery(text('SELECT TOP 10 CAST(SUM(ord.TotalOrden) AS INTEGER) as totalVentas FROM DimProductos as pro INNER JOIN DimDetalles_Orden as deo ON pro.IDProducto = deo.IDProducto INNER JOIN Hechos_Ordenes as ord ON deo.IDOrden = ord.IDOrden GROUP BY pro.NombreProducto ORDER BY totalVentas DESC;'))
        for rows in result2:
            value = int(rows[0])
            y.append(value)

        self.MyPlotFrame2 = MyPlotFrame(self, title="Top 10 Productos Más Vendidos", xData=result1, yData=result2 ,desc="Lorem t amet iaculis con")
        self.MyPlotFrame2.grid(row=0,column=1,padx=10,pady=(10,0), sticky="nsew")
        
        result1 = db.executeQuery(text('SELECT tie.TRIMESTRE FROM DimTiempo as tie INNER JOIN Hechos_Ordenes as ord ON tie.IDOrden = ord.IDOrden GROUP BY tie.TRIMESTRE ORDER BY SUM(ord.TotalOrden) DESC;'))
        x = []
        for rows in result1:
            x.extend(rows)
        
        y = []
        result2 = db.executeQuery(text('SELECT CAST(SUM(ord.TotalOrden) AS INTEGER) as Total_Ventas FROM DimTiempo as tie INNER JOIN Hechos_Ordenes as ord ON tie.IDOrden = ord.IDOrden GROUP BY tie.TRIMESTRE ORDER BY Total_Ventas DESC;'))
        for rows in result2:
            value = int(rows[0])
            y.append(value)

        self.MyPlotFrame3 = MyPlotFrame(self, title="Ventas Por Trimestre", xData=result1, yData=result2 , desc="Lorem iit. Pnullibero elemeetisellus massa purus, rhoncus et diam.") #Siendo y el territorio con menos ventas en 2014
        self.MyPlotFrame3.grid(row=1,column=0,padx=10,pady=(10,0), sticky="nsew")

        result1 = db.executeQuery(text("SELECT TOP 10 CONCAT(cli.Primer_Nombre, ' ', cli.Apellido) AS Nombre_Completo FROM DimClientes AS cli INNER JOIN Hechos_Ordenes as ord ON cli.IDCliente = ord.IDCliente GROUP BY cli.Primer_Nombre, cli.Apellido ORDER BY SUM(ord.TotalOrden) DESC;"))
        x = []
        for rows in result1:
            x.extend(rows)
        y = []
        result2 = db.executeQuery(text('SELECT TOP 10 CAST(SUM(ord.TotalOrden) AS INTEGER) as total_Ventas FROM DimClientes AS cli INNER JOIN Hechos_Ordenes as ord ON cli.IDCliente = ord.IDCliente GROUP BY cli.Primer_Nombre, cli.Apellido ORDER BY SUM(ord.TotalOrden) DESC;'))
        for rows in result2:
            value = int(rows[0])
            y.append(value)

        self.MyPlotFrame4 = MyPlotFrame(self, title="Ventas por Cliente", xData=result1, yData=result2 , desc="Lor libero, nec coeo. Phasellus massa purus, rhoncus et diam.")
        self.MyPlotFrame4.grid(row=1,column=1,padx=10,pady=(10,0), sticky="nsew")

        db.disconnect()

app = App()
app.mainloop()