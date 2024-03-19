import customtkinter
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MyPlotFrame(customtkinter.CTkScrollableFrame):
    def __init__(self,master,title):
        super().__init__(master)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        self.title = title
        self.figure, self.ax = plt.subplots()
        

        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()
        #Puedo hacer la creación del objeto con el matplot en blanco y a traves de metodos hago los cambios de valores
        
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0,column=0,padx=10,pady=(10,0), sticky="ew")

        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=(10,0), sticky="ew")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Adventure Works Data Visualization App")
        self.geometry("1080x990")
        self.grid_rowconfigure((0,1),weight=1)
        self.grid_columnconfigure((0,1),weight=1)

        self.MyPlotFrame1 = MyPlotFrame(self, title="Ventas por territorio 2014")
        self.MyPlotFrame1.grid(row=0,column=0,padx=10,pady=(10,0), sticky="nsew")


        

        self.MyPlotFrame2 = MyPlotFrame(self, title="Categorias más vendidas en el territorio X") #Siendo x el territorio con mayor ganacias en 2014
        self.MyPlotFrame2.grid(row=0,column=1,padx=10,pady=(10,0), sticky="nsew")

        
        self.MyPlotFrame3 = MyPlotFrame(self, title="Categorias más vendidas en el territorio Y") #Siendo y el territorio con menos ventas en 2014
        self.MyPlotFrame3.grid(row=1,column=0,padx=10,pady=(10,0), sticky="nsew")

        
        self.MyPlotFrame4 = MyPlotFrame(self, title="Categorias con menos ventas en 2014")
        self.MyPlotFrame4.grid(row=1,column=1,padx=10,pady=(10,0), sticky="nsew")
app = App()
app.mainloop()