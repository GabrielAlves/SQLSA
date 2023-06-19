import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog as fd, messagebox as msg

from analisador import Analisador

class SQLSA:
    def __init__(self):
        self.criar_widgets()

    def criar_widgets(self):
        self.criar_janela()
        self.criar_frame1()
        self.criar_botao_de_analise_de_sintaxe()
        self.criar_label_de_resultado()

    def criar_janela(self):
        self.janela = tk.Tk()
        self.configurar_janela()

    def configurar_janela(self):
        self.janela.title("SQLSA")
        self.janela.geometry("325x300")
        self.janela.resizable(False, False)

    def criar_frame1(self):
        self.frame1 = ttk.Frame(self.janela)
        self.frame1.pack(pady = 10)
        self.criar_widgets_do_frame1()

    def criar_widgets_do_frame1(self):
        self.criar_botao_de_selecao_de_arquivo()
        self.criar_campo_com_filename()
        self.criar_campo_com_texto_do_arquivo()

    def criar_botao_de_selecao_de_arquivo(self):
        self.botao_de_selecao_de_arquivo = ttk.Button(self.frame1, text="Selecionar arquivo", command = self.selecionar_arquivo)
        self.botao_de_selecao_de_arquivo.grid(row=0, column=0, padx = 3, sticky = tk.NSEW)

    def selecionar_arquivo(self):
        filename = fd.askopenfilename(title = "Selecione um arquivo", filetypes = [('text files', '*.txt')])
        self.escrever_filename_no_campo(filename)
        self.escrever_texto_do_arquivo_no_campo(filename)

    def escrever_filename_no_campo(self, filename):
        self.campo_com_filename.configure(state="normal")
        self.campo_com_filename.delete(0, tk.END)
        self.campo_com_filename.insert(0, filename)
        self.campo_com_filename.configure(state="readonly")

    def escrever_texto_do_arquivo_no_campo(self, filename):
        with open(filename, mode = "r", encoding = "utf-8") as arquivo:
            texto = arquivo.read()

        self.campo_com_texto_do_arquivo.configure(state="normal")
        self.campo_com_texto_do_arquivo.delete("1.0", tk.END)
        self.campo_com_texto_do_arquivo.insert("1.0", texto)

    def criar_campo_com_filename(self):
        self.campo_com_filename = ttk.Entry(self.frame1)
        self.campo_com_filename.grid(row=0, column=1, padx = 3, sticky = tk.NSEW)
        self.frame1.columnconfigure(1, weight=1)
        self.campo_com_filename.configure(state="readonly")

    def criar_campo_com_texto_do_arquivo(self):
        self.campo_com_texto_do_arquivo = scrolledtext.ScrolledText(self.frame1, width = 30, height=7, font=("Arial", 12),wrap=tk.WORD)
        self.campo_com_texto_do_arquivo.grid(row = 1, columnspan = 2, pady = 5)

    def criar_botao_de_analise_de_sintaxe(self):
        self.botao_de_analise_de_sintaxe = ttk.Button(self.janela, text="Analisar sintaxe", command = self.analisar_sintaxe)
        self.botao_de_analise_de_sintaxe.pack(pady = 3)

    # TODO: Ler comando diretamente da caixa de texto(ele acrescenta "\n"s na string)
    def analisar_sintaxe(self):
        comando = self.campo_com_texto_do_arquivo.get("1.0", tk.END)
        comando = comando.replace("\n", "")

        analisador = Analisador()
        analisador.analisar_comando(comando)     
        resultado = analisador.retornar_resultado()

        if resultado:
            self.label_de_resultado.config(text = "Sucesso!")
            self.label_de_resultado.config(fg = "green")

        else:
            self.label_de_resultado.config(text = "Fracasso!")
            self.label_de_resultado.config(fg = "red")

    def criar_label_de_resultado(self):
        self.label_de_resultado = tk.Label(self.janela, text = "")
        self.label_de_resultado.pack()
        

if __name__ == "__main__":
    gui = SQLSA()
    gui.janela.mainloop()