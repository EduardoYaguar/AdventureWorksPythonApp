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
    def __init__(self,master,title, desc):
        super().__init__(master)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        self.title = title
        self.desc = desc
        self.figure, self.ax = plt.subplots()
        
        

        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()   
        #Puedo hacer la creación del objeto con el matplot en blanco y a traves de metodos hago los cambios de valores
        
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0,column=0,padx=10,pady=(10,0), sticky="ew")

        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=(10,0), sticky="ew")

        textBox = customtkinter.CTkTextbox(self, fg_color="gray30", corner_radius=6, cursor="arrow")
        textBox.insert(index="0.0",text=self.desc)
        textBox.configure(state="disable")
        textBox.grid(row=3, column=0, padx=10, pady=(10,0), sticky="nsew",)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Adventure Works Data Visualization App")
        self.geometry("1080x990")
        self.grid_rowconfigure((0,1),weight=1)
        self.grid_columnconfigure((0,1),weight=1)

        db = DataBase("mssql+pyodbc://LAPTOP-MGLHUKHT/DWAdventureWorks?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
        db.connect()
        results = db.executeQuery(text('SELECT * FROM DIMTiendas'))
        print(results)



        self.MyPlotFrame1 = MyPlotFrame(self, title="Ventas por territorio 2014", desc="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque varius, dui sit amet iaculis convallis, nulla lectus varius turpis, vitae fringilla dui mi iaculis mi. Donec et mattis urna, vel vestibulum diam. Suspendisse nec pellentesque felis. Nunc in volutpat libero, nec condimentum velit. Nullam quis quam eget felis convallis porta. Mauris porttitor, nunc ut aliquet posuere, leo lectus aliquam est, eu luctus magna dolor non nibh. Aliquam erat volutpat. Integer ultricies suscipit lacus. Sed eu massa non enim lobortis elementum. Cras tempus finibus nunc, sit amet pretium nisl mattis quis. Cras id tristique leo. Phasellus massa purus, rhoncus et diam.")
        self.MyPlotFrame1.grid(row=0,column=0,padx=10,pady=(10,0), sticky="nsew")


        self.MyPlotFrame2 = MyPlotFrame(self, title="Categorias más vendidas en el territorio X", desc="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque varius, dui sit amet iaculis convallis, nulla lectus varius turpis, vitae fringilla dui mi iaculis mi. Donec et mattis urna, vel vestibulum diam. Suspendisse nec pellentesque felis. Nunc in volutpat libero, nec condimentum velit. Nullam quis quam eget felis convallis porta. Mauris porttitor, nunc ut aliquet posuere, leo lectus aliquam est, eu luctus magna dolor non nibh. Aliquam erat volutpat. Integer ultricies suscipit lacus. Sed eu massa non enim lobortis elementum. Cras tempus finibus nunc, sit amet pretium nisl mattis quis. Cras id tristique leo. Phasellus massa purus, rhoncus et diam.") #Siendo x el territorio con mayor ganacias en 2014
        self.MyPlotFrame2.grid(row=0,column=1,padx=10,pady=(10,0), sticky="nsew")

        
        self.MyPlotFrame3 = MyPlotFrame(self, title="Categorias más vendidas en el territorio Y", desc="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque varius, dui sit amet iaculis convallis, nulla lectus varius turpis, vitae fringilla dui mi iaculis mi. Donec et mattis urna, vel vestibulum diam. Suspendisse nec pellentesque felis. Nunc in volutpat libero, nec condimentum velit. Nullam quis quam eget felis convallis porta. Mauris porttitor, nunc ut aliquet posuere, leo lectus aliquam est, eu luctus magna dolor non nibh. Aliquam erat volutpat. Integer ultricies suscipit lacus. Sed eu massa non enim lobortis elementum. Cras tempus finibus nunc, sit amet pretium nisl mattis quis. Cras id tristique leo. Phasellus massa purus, rhoncus et diam.") #Siendo y el territorio con menos ventas en 2014
        self.MyPlotFrame3.grid(row=1,column=0,padx=10,pady=(10,0), sticky="nsew")

        
        self.MyPlotFrame4 = MyPlotFrame(self, title="Categorias con menos ventas en 2014", desc="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque varius, dui sit amet iaculis convallis, nulla lectus varius turpis, vitae fringilla dui mi iaculis mi. Donec et mattis urna, vel vestibulum diam. Suspendisse nec pellentesque felis. Nunc in volutpat libero, nec condimentum velit. Nullam quis quam eget felis convallis porta. Mauris porttitor, nunc ut aliquet posuere, leo lectus aliquam est, eu luctus magna dolor non nibh. Aliquam erat volutpat. Integer ultricies suscipit lacus. Sed eu massa non enim lobortis elementum. Cras tempus finibus nunc, sit amet pretium nisl mattis quis. Cras id tristique leo. Phasellus massa purus, rhoncus et diam.")
        self.MyPlotFrame4.grid(row=1,column=1,padx=10,pady=(10,0), sticky="nsew")

        db.disconnect()

app = App()
app.mainloop()