import mysql.connector
import tkinter as tk
from tkinter import messagebox

class Vista:
    def __init__(self, root):
        self.root = root
        self.root.title("Conexión a Base de Datos")
        
        self.btn_connect = tk.Button(self.root, text="Conexion", command=self.conectar_bd)
        self.btn_connect.pack(pady=10)
        
        self.btn_disconnect = tk.Button(self.root, text="Desconexion", command=self.desconectar_bd, state=tk.DISABLED)
        self.btn_disconnect.pack(pady=10)
        
        self.conexion = None

    def conectar_bd(self):
        try:
            self.conexion = mysql.connector.connect(user='root', password='root', 
                                                     database='prueba', port=3306)
            messagebox.showinfo("Conexión exitosa")
            self.btn_connect.config(state=tk.DISABLED)
            self.btn_disconnect.config(state=tk.NORMAL)
        except mysql.connector.Error as error:
            messagebox.showerror("Error de conexión", f"Ocurrió un error al conectar a la base de datos: {error}")

    def desconectar_bd(self):
        if self.conexion:
            self.conexion.close()
            messagebox.showinfo("Desconexión exitosa")
            self.btn_connect.config(state=tk.NORMAL)
            self.btn_disconnect.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Advertencia", "No hay una conexión activa.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Vista(root)
    root.mainloop()
