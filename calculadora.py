import tkinter as tk
from tkinter import messagebox
import turtle

class MotorArboles:
    """
    Clase principal para la creación, transformación y renderizado de árboles dirigidos
    y su representación binaria utilizando la librería turtle.
    """
    
    COORD_DIR = {
        'I': (-350, 350), 'F': (-500, 200), 'V': (-200, 200), 'C': (-600, 100),
        'D': (-550, 100), 'R': (-450, 100), 'S': (-400, 100), 'H': (-300, 100),
        'T': (-250, 100), 'Y': (-150, 100), 'L': (-100, 100), 'U': (-650, 50),
        'G': (-625, 50), 'P': (-575, 50), 'K': (-550, 50), 'M': (-450, 50),
        'N': (-425, 50), 'A': (-375, 50), 'B': (-360, 50), 'Z': (-340, 50),
        'Br': (-250, 50), 'Ga': (-150, 50), 'Le': (-50, 50)
    }

    COORD_BIN = {
        'I': (350, 350), 'F': (300, 300), 'C': (200, 200), 'U': (100, 100),
        'V': (400, 220), 'H': (365, 185), 'T': (399, 160), 'Y': (432, 135),
        'L': (465, 110), 'Ga': (435, 75), 'Le': (480, 40), 'Z': (330, 150),
        'Br': (370, 120), 'D': (233, 173), 'R': (266, 146), 'S': (300, 120),
        'M': (260, 80), 'N': (293, 53), 'A': (327, 26), 'B': (360, 0),
        'G': (133, 73), 'P': (166, 46), 'K': (200, 20)
    }

    SECUENCIA_ARISTAS = {
        2: [('I','F'), ('I','V'), ('F','C'), ('F','S'), ('V','H'), ('V','L'), ('C','U'), ('C','K'), ('S','M'), ('S','B'), ('H','Z'), ('H','Br'), ('L','Ga'), ('L','Le')],
        3: [('I','F'), ('I','V'), ('F','C'), ('F','D'), ('F','S'), ('V','H'), ('V','T'), ('V','L'), ('C','U'), ('C','G'), ('C','K'), ('S','M'), ('S','B'), ('S','N')],
        4: [('I','F'), ('I','V'), ('F','C'), ('F','D'), ('F','R'), ('F','S'), ('V','H'), ('V','T'), ('V','Y'), ('V','L'), ('C','U'), ('C','G'), ('C','P'), ('C','K')]
    }

    # Constantes para el renderizado con Turtle
    SCREEN_WIDTH = 1440
    SCREEN_HEIGHT = 900
    NODE_FONT_SIZE = 14
    TITLE_FONT_SIZE = 16
    TABLE_HEADER_FONT_SIZE = 12
    TABLE_CONTENT_FONT_SIZE = 13
    EQUATION_FONT_SIZE = 18

    NODE_LABEL_OFFSET_Y = -10
    GRAPH_TITLE_OFFSET_Y = 70

    TABLE_TITLE_POS_X = -700
    TABLE_TITLE_POS_Y = 10
    TABLE_START_X = -570
    TABLE_START_Y = -20
    TABLE_ROW_HEIGHT = 25
    TABLE_COL_WIDTH = 100
    TABLE_CELL_X_OFFSET = 15

    GRID_START_Y = 5
    GRID_MIN_X = -600
    GRID_MAX_X = -200

    EQUATION_TITLE_POS_X = 0
    EQUATION_TITLE_POS_Y = -50
    EQUATION_CONTENT_POS_X = -100
    EQUATION_CONTENT_POS_Y = -200
    EQUATION_LINE_BREAK_THRESHOLD = 85
    EQUATION_LINE_BREAK_X_OFFSET = 45
    EQUATION_LINE_BREAK_Y_OFFSET = -30


    def __init__(self, elementos: int, grado: int):
        """
        Inicializa el MotorArboles con el número de elementos y el grado del árbol.

        Args:
            elementos (int): Número de elementos a considerar para el árbol dirigido.
            grado (int): Grado del árbol (n-ario). Debe ser 2, 3 o 4.
        """
        self.elementos = elementos
        self.grado = grado
        # Selecciona un subconjunto de aristas basado en el grado y elementos.
        self.dir_edges = self.SECUENCIA_ARISTAS[self.grado][:self.elementos - 1]
        # Extrae y ordena los nodos únicos de las aristas dirigidas.
        self.nodos = sorted(list(set([u for u, v in self.dir_edges] + [v for u, v in self.dir_edges])))
        # Transforma el árbol dirigido a un árbol binario y obtiene sus componentes.
        self.bin_edges, self.left_map, self.right_map = self.transformar_knuth(self.dir_edges)

    def transformar_knuth(self, dir_edges: list) -> tuple:
        """
        Transforma un árbol dirigido (n-ario) en su representación de árbol binario
        posicional (transformación de Knuth o "left-child, right-sibling").

        Args:
            dir_edges (list): Lista de tuplas representando las aristas del árbol dirigido [(u, v)].

        Returns:
            tuple: Una tupla que contiene:
                - bin_edges (list): Lista de tuplas representando las aristas del árbol binario.
                - left_map (dict): Mapeo de nodos a su primer hijo (en el árbol binario).
                - right_map (dict): Mapeo de nodos a su siguiente hermano (en el árbol binario).
        """
        adj = {}
        for u, v in dir_edges:
            adj.setdefault(u, []).append(v)

        # Ordena los hijos para una representación consistente.
        for u in adj:
            adj[u].sort(key=lambda n: self.COORD_DIR[n][0])

        bin_edges = []
        left_map, right_map = {}, {}

        for u, hijos in adj.items():
            if hijos:
                primer_hijo = hijos[0]
                bin_edges.append((u, primer_hijo))
                left_map[u] = primer_hijo
                
                actual = primer_hijo
                for hermano in hijos[1:]:
                    bin_edges.append((actual, hermano))
                    right_map[actual] = hermano
                    actual = hermano

        return bin_edges, left_map, right_map

    def construir_matriz(self) -> list:
        """
        Construye una representación tabular (matriz) del árbol binario.

        Returns:
            list: Una lista de tuplas, donde cada tupla representa una fila
                  con (INDICE, LEFT_CHILD_INDEX, DATA, RIGHT_CHILD_INDEX).
        """
        node_to_idx = {nodo: i + 2 for i, nodo in enumerate(self.nodos)}
        
        # Fila para la raíz o un elemento especial (según la lógica original).
        root_idx = node_to_idx.get('I', 0)
        filas = [("1", str(root_idx), "", "")] # Esta fila parece ser un placeholder o una convención específica.
        
        for i, nodo in enumerate(self.nodos):
            idx = i + 2
            l_val = str(node_to_idx[self.left_map[nodo]]) if nodo in self.left_map else "0"
            r_val = str(node_to_idx[self.right_map[nodo]]) if nodo in self.right_map else "0"
            filas.append((str(idx), l_val, nodo, r_val))
            
        return filas

    def renderizar(self):
        """
        Renderiza los dos grafos (dirigido y binario posicional) y la tabla
        de representación matricial utilizando la librería turtle.
        """
        ventana = turtle.Screen()
        ventana.setup(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 0, 0)
        ventana.clear()
        ventana.bgcolor("black")
        ventana.tracer(0)   

        lapiz = turtle.Turtle(visible=False)
        lapiz.pencolor("Yellow")
        texto = turtle.Turtle(visible=False)
        texto.pencolor("red")
        ecuacion = turtle.Turtle(visible=False)
        ecuacion.pencolor("cyan")
        
        lapiz.penup()
        texto.penup()
        ecuacion.penup()

        self._dibujar_grafo(lapiz, texto, self.nodos, self.dir_edges, self.COORD_DIR, "DÍGRAFO DE ÁRBOL DIRIGIDO", 0, self.GRAPH_TITLE_OFFSET_Y)
        self._dibujar_grafo(lapiz, texto, self.nodos, self.bin_edges, self.COORD_BIN, "DÍGRAFO DE ÁRBOL BINARIO POSICIONAL B(T)", self.SCREEN_WIDTH / 4, self.GRAPH_TITLE_OFFSET_Y)
        self._dibujar_tabla(lapiz, texto)
        self._escribir_extension(ecuacion)

        ventana.update()

    def _dibujar_grafo(self, pen, txt, nodos, aristas, mapa_coords, titulo, off_x, off_y):
        txt.goto(mapa_coords['I'][0] + off_x, mapa_coords['I'][1] + off_y + 20) # Adjusted Y for title
        txt.write(titulo, align="center", font=("Arial", self.TITLE_FONT_SIZE, "bold"))
        
        for u, v in aristas:
            x1, y1 = mapa_coords[u]
            x2, y2 = mapa_coords[v]
            pen.goto(x1 + off_x, y1 + off_y)
            pen.pendown()
            pen.goto(x2 + off_x, y2 + off_y)
            pen.penup()

        for n in nodos:
            x, y = mapa_coords[n]
            txt.goto(x + off_x, y + off_y + self.NODE_LABEL_OFFSET_Y)
            txt.write(n, align="center", font=("Arial", self.NODE_FONT_SIZE, "normal"))

    def _dibujar_tabla(self, pen, txt):
        filas = self.construir_matriz()
        
        txt.goto(self.TABLE_TITLE_POS_X, self.TABLE_TITLE_POS_Y)
        txt.write("ARREGLOS", align="left", font=("Arial", self.TITLE_FONT_SIZE, "bold"))
        
        headers = ["INDICE", "LEFT", "DATA", "RIGHT"]
        
        for i, h in enumerate(headers):
            txt.goto(self.TABLE_START_X + (i * self.TABLE_COL_WIDTH), self.TABLE_START_Y)
            txt.write(h, font=("Arial", self.TABLE_HEADER_FONT_SIZE, "bold"))

        y_actual = self.TABLE_START_Y - self.TABLE_ROW_HEIGHT
        for col1, col2, col3, col4 in filas:
            txt.goto(self.TABLE_START_X + self.TABLE_CELL_X_OFFSET, y_actual)
            txt.write(col1, font=("Arial", self.TABLE_CONTENT_FONT_SIZE, "normal"))
            txt.goto(self.TABLE_START_X + self.TABLE_COL_WIDTH + self.TABLE_CELL_X_OFFSET, y_actual)
            txt.write(col2, font=("Arial", self.TABLE_CONTENT_FONT_SIZE, "normal"))
            txt.goto(self.TABLE_START_X + (2 * self.TABLE_COL_WIDTH) + self.TABLE_CELL_X_OFFSET, y_actual)
            txt.write(col3, font=("Arial", self.TABLE_CONTENT_FONT_SIZE, "normal"))
            txt.goto(self.TABLE_START_X + (3 * self.TABLE_COL_WIDTH) + self.TABLE_CELL_X_OFFSET, y_actual)
            txt.write(col4, font=("Arial", self.TABLE_CONTENT_FONT_SIZE, "normal"))
            y_actual -= self.TABLE_ROW_HEIGHT

        pen.penup()
        y_grid = self.GRID_START_Y
        for _ in range(len(filas) + 2): # +2 for header and one empty row for spacing
            pen.goto(self.GRID_MIN_X, y_grid)
            pen.pendown()
            pen.goto(self.GRID_MAX_X, y_grid)
            pen.penup()
            y_grid -= self.TABLE_ROW_HEIGHT

        x_grid = self.GRID_MAX_X
        for _ in range(5): # 4 columns + 1 for the start of the first column
            pen.goto(x_grid, self.GRID_START_Y)
            pen.pendown()
            pen.goto(x_grid, y_grid + self.TABLE_ROW_HEIGHT) # Adjust grid height
            pen.penup()
            x_grid -= self.TABLE_COL_WIDTH

    def _escribir_extension(self, eq):
        eq.goto(self.EQUATION_TITLE_POS_X, self.EQUATION_TITLE_POS_Y)
        eq.write("ELEMENTOS DE T POR EXTENSIÓN", align="center", font=("Arial", self.TITLE_FONT_SIZE, "bold"))
        
        conjunto = ",".join([f"({u},{v})" for u, v in self.dir_edges])
        string_final = f"T = {{{conjunto}}}"
        
        eq.goto(self.EQUATION_CONTENT_POS_X, self.EQUATION_CONTENT_POS_Y)
        if len(string_final) > self.EQUATION_LINE_BREAK_THRESHOLD:
            eq.write(string_final[:self.EQUATION_LINE_BREAK_THRESHOLD], align="left", font=("Times New Roman", self.EQUATION_FONT_SIZE, "normal"))
            eq.goto(self.EQUATION_CONTENT_POS_X + self.EQUATION_LINE_BREAK_X_OFFSET, self.EQUATION_CONTENT_POS_Y + self.EQUATION_LINE_BREAK_Y_OFFSET)
            eq.write(string_final[self.EQUATION_LINE_BREAK_THRESHOLD:], align="left", font=("Times New Roman", self.EQUATION_FONT_SIZE, "normal"))
        else:
            eq.write(string_final, align="left", font=("Times New Roman", self.EQUATION_FONT_SIZE, "normal"))

def ejecutar_aplicacion():
    a_val = entrada1.get()
    b_val = entrada2.get()
    
    if a_val.isdigit() and b_val.isdigit():
        a, b = int(a_val), int(b_val)
        if 10 <= a <= 15 and 2 <= b <= 4:
            motor = MotorArboles(a, b)
            motor.renderizar()
        else:
            messagebox.showerror('Error', 'Restricción paramétrica: 10 <= elementos <= 15 | 2 <= n-arbol <= 4')
    else:
        messagebox.showerror('Error', 'Se requieren valores enteros (int).')
#TRAS
if __name__ == '__main__':
    raiz = tk.Tk()
    raiz.title('MÓDULO DE ÁRBOLES')
    raiz.resizable(0,0)
    raiz.geometry("350x170+100+100")
    tk.Label(raiz, text="Numero de elementos:").place(x=25, y=25)
    entrada1 = tk.Entry(raiz)
    entrada1.place(x=200, y=25)
    tk.Label(raiz, text="Numero de n-arbol:").place(x=25, y=75)
    entrada2 = tk.Entry(raiz)
    entrada2.place(x=200, y=75)
    tk.Button(raiz, text='EJECUTAR RENDER', command=ejecutar_aplicacion).place(x=120, y=120)
    raiz.mainloop()