import tkinter as tk
from tkinter import filedialog
import pygame
import os

class ReproductorMusica:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Música Estilo Spotify")
        
        # Inicializa pygame
        pygame.mixer.init()
        
        # Variables para el estado de la música
        self.musica_reproduciendo = False
        self.cancion_actual = ""
        self.volumen = 0.5  # Valor inicial del volumen (rango de 0.0 a 1.0)
        self.lista_reproduccion = []
        self.indice_actual = 0
        
        # Frame para los controles
        self.frame_controles = tk.Frame(root)
        self.frame_controles.pack(pady=20)
        
        # Botones de control
        self.boton_abrir = tk.Button(self.frame_controles, text="Abrir", command=self.abrir_archivo)
        self.boton_abrir.grid(row=0, column=0, padx=10)
        
        self.boton_reproducir = tk.Button(self.frame_controles, text="Reproducir", command=self.reproducir_musica, state=tk.DISABLED)
        self.boton_reproducir.grid(row=0, column=1, padx=10)
        
        self.boton_pausar = tk.Button(self.frame_controles, text="Pausar", command=self.pausar_musica, state=tk.DISABLED)
        self.boton_pausar.grid(row=0, column=2, padx=10)
        
        self.boton_detener = tk.Button(self.frame_controles, text="Detener", command=self.detener_musica, state=tk.DISABLED)
        self.boton_detener.grid(row=0, column=3, padx=10)
        
        self.boton_siguiente = tk.Button(self.frame_controles, text="Siguiente", command=self.siguiente_pista, state=tk.DISABLED)
        self.boton_siguiente.grid(row=1, column=0, padx=10)
        
        # Botones de control de volumen
        self.boton_volumen_up = tk.Button(self.frame_controles, text="Volumen +", command=self.subir_volumen)
        self.boton_volumen_up.grid(row=1, column=1, padx=10)
        
        self.boton_volumen_down = tk.Button(self.frame_controles, text="Volumen -", command=self.bajar_volumen)
        self.boton_volumen_down.grid(row=1, column=2, padx=10)
        
        # Lista de reproducción
        self.lista_reproduccion_frame = tk.Frame(root)
        self.lista_reproduccion_frame.pack(pady=10)
        
        self.lista_reproduccion_label = tk.Label(self.lista_reproduccion_frame, text="Lista de Reproducción")
        self.lista_reproduccion_label.pack()
        
        self.lista_reproduccion_box = tk.Listbox(self.lista_reproduccion_frame, width=50, height=10)
        self.lista_reproduccion_box.pack()

    def abrir_archivo(self):
        archivos = filedialog.askopenfilenames(filetypes=[("Archivos de música", "*.mp3 *.wav")])
        if archivos:
            self.lista_reproduccion = archivos
            self.indice_actual = 0
            self.cancion_actual = self.lista_reproduccion[self.indice_actual]
            self.lista_reproduccion_box.delete(0, tk.END)
            for archivo in self.lista_reproduccion:
                self.lista_reproduccion_box.insert(tk.END, os.path.basename(archivo))
            self.boton_reproducir.config(state=tk.NORMAL)
            self.boton_siguiente.config(state=tk.NORMAL)
    
    def reproducir_musica(self):
        if not self.musica_reproduciendo:
            if self.cancion_actual:
                pygame.mixer.music.load(self.cancion_actual)
                pygame.mixer.music.set_volume(self.volumen)  # Establece el volumen
                pygame.mixer.music.play()
                self.musica_reproduciendo = True
                self.boton_pausar.config(state=tk.NORMAL)
                self.boton_detener.config(state=tk.NORMAL)
    
    def pausar_musica(self):
        if self.musica_reproduciendo:
            pygame.mixer.music.pause()
            self.musica_reproduciendo = False
            self.boton_reproducir.config(state=tk.NORMAL)
    
    def detener_musica(self):
        if self.musica_reproduciendo:
            pygame.mixer.music.stop()
            self.musica_reproduciendo = False
            self.boton_reproducir.config(state=tk.NORMAL)
            self.boton_pausar.config(state=tk.DISABLED)
            self.boton_detener.config(state=tk.DISABLED)
    
    def siguiente_pista(self):
        if self.lista_reproduccion:
            self.indice_actual = (self.indice_actual + 1) % len(self.lista_reproduccion)
            self.cancion_actual = self.lista_reproduccion[self.indice_actual]
            if self.musica_reproduciendo:
                pygame.mixer.music.stop()
            self.reproducir_musica()
    
    def subir_volumen(self):
        if self.volumen < 1.0:
            self.volumen = min(self.volumen + 0.1, 1.0)
            pygame.mixer.music.set_volume(self.volumen)
            print(f"Volumen: {self.volumen:.1f}")  # Muestra el volumen actual en la consola
    
    def bajar_volumen(self):
        if self.volumen > 0.0:
            self.volumen = max(self.volumen - 0.1, 0.0)
            pygame.mixer.music.set_volume(self.volumen)
            print(f"Volumen: {self.volumen:.1f}")  # Muestra el volumen actual en la consola

if __name__ == "__main__":
    root = tk.Tk()
    reproductor = ReproductorMusica(root)
    root.mainloop()
