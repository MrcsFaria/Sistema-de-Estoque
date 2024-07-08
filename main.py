from datetime import datetime
import random
from tkinter import messagebox
from tkinter.messagebox import askyesno
from customtkinter import *
import os
from PIL import Image, ImageTk
import os
import pandas as pd
import sqlite3
import tkinter
from tkinter import ttk
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from barcode import EAN13
from barcode.writer import ImageWriter
import locale

locale.setlocale(locale.LC_TIME,'pt_BR.UTF-8')

dia_atual = datetime.now().strftime("%d/%m/%Y")

data_atual = datetime.now()
nome_mes = data_atual.strftime("%B/%Y")

# Obtém o diretório do usuário
diretorio = os.getcwd()

# Constrói o caminho completo do diretório dos itens
caminh_banco = os.path.join(diretorio, "Banco_de_Dados", "estoque.db")
caminh_img_lat = os.path.join(diretorio, "assets", "side-img.png")
caminh_icon_user = os.path.join(diretorio, "assets", "user-icon.png")
caminh_icon_senha = os.path.join(diretorio, "assets", "password-icon.png")

# Definindo a Tela Principal
tela_login = CTk()
tela_login.geometry("{}x{}+0+0".format(tela_login.winfo_screenwidth(), tela_login.winfo_screenheight()))
tela_login.title("Estoque - Login")

#Criando variavel para coletar as dimensões de tamanho da tela
altura_tela = tela_login.winfo_screenheight()
largura_tela = tela_login.winfo_screenwidth()

# Carregando as imagens usando PIL
img_lat_pil = Image.open(caminh_img_lat)
icone_user_pil = Image.open(caminh_icon_user)
icone_senha_pil = Image.open(caminh_icon_senha)

#Puxando as imagens para usar na interface
img_lat = CTkImage(dark_image=img_lat_pil, light_image=img_lat_pil, size=(int(0.4*largura_tela), altura_tela))
icone_user = CTkImage(dark_image=icone_user_pil, light_image=icone_user_pil, size=(20, 20))
icone_senha = CTkImage(dark_image=icone_senha_pil, light_image=icone_senha_pil, size=(17, 17))

def sair_do_app():
    ans = askyesno(title='Sair', message='Tem certeza que quer Sair?')
    if ans:
        sys.exit()

def autenticacao():
    global login, senha, tela_menu
    login = logn.get()
    senha = passw.get()

    if (login == "admin" and senha == "admin"):

        tela_login.withdraw()

        tela_menu = CTkToplevel()
        tela_menu.geometry("{}x{}+0+0".format(largura_tela,altura_tela))
        tela_menu.title('Estoque - Menu')
        tela_menu.protocol("WM_DELETE_WINDOW", sair_do_app)

        CTkLabel(master=tela_menu, text="", image=img_lat).pack(expand=True, side="left")

        frame_cabecalho_menu = CTkFrame(master=tela_menu, width=int(0.6 * largura_tela), height=int(0.14 * altura_tela))
        frame_cabecalho_menu.pack(expand=True, side="top")

        CTkLabel(master=frame_cabecalho_menu, text="------------------------------------- Estoque -------------------------------------", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(0,0), padx=(0, 0))

        scrollable_frame_menu = CTkScrollableFrame(master=tela_menu, width=int(0.6 * largura_tela), height=int(0.85 * altura_tela), fg_color="#ffffff")
        scrollable_frame_menu.pack(expand=True, side="right")

        frame_menu = CTkFrame(master=scrollable_frame_menu, fg_color="#ffffff")
        frame_menu.pack(expand=True, anchor="w", pady=(10, 0))

        CTkLabel(master=frame_menu, text="  Verificar Estoque:", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(35, 0), padx=(int(0.2*frame_menu.winfo_screenwidth()), 0))
        CTkButton(master=frame_menu, text="Estoque", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=ver_estoque).pack(anchor="w", pady=(15, 0), padx=(int(0.2*frame_menu.winfo_screenwidth()), 0))

        CTkLabel(master=frame_menu, text="  Ver Gráficos:", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(35, 0), padx=(int(0.2*frame_menu.winfo_screenwidth()), 0))
        CTkButton(master=frame_menu, text="Gráficos", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=menu_graficos).pack(anchor="w", pady=(15, 0), padx=(int(0.2*frame_menu.winfo_screenwidth()), 0))
    else:
        messagebox.showerror("Erro!", "Login ou Senha incorretos")

def ver_estoque():

    global tela_estoque, treeviewF, nome_entry, qtd_entry, un_entry, preco_compra_entry, preco_venda_entry, forn_entry, val_entry, nome_entry_pes

    tela_menu.withdraw()
    
    tela_estoque = CTkToplevel()
    tela_estoque.geometry("{}x{}+0+0".format(largura_tela, altura_tela))
    tela_estoque.title("Estoque - Estoque Físico")
    tela_estoque.protocol("WM_DELETE_WINDOW", sair_do_app)

    frame_estoque = tkinter.Frame(tela_estoque, width= int(0.7 * largura_tela), height=int(altura_tela))
    frame_estoque.pack_propagate(0)
    frame_estoque.pack(expand=True, side="right")

    frame_treeview_estoque = tkinter.Frame(frame_estoque, width= int(0.7 * largura_tela), height=int(altura_tela))
    frame_treeview_estoque.pack_propagate(0)
    frame_treeview_estoque.pack(expand=True, side="right")

    # Criar a Treeview
    treeviewF = ttk.Treeview(frame_treeview_estoque, columns=("Nome", "Descrição"), show="headings")
    treeviewF.heading("Nome", text="Nome")
    treeviewF.heading("Descrição", text="Descrição")

    # Adicionar Scrollbars
    scrollbar_y = ttk.Scrollbar(frame_treeview_estoque, orient="vertical", command=treeviewF.yview)
    scrollbar_y.pack(side="right", fill="y")
    treeviewF.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(frame_treeview_estoque, orient="horizontal", command=treeviewF.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    treeviewF.configure(xscrollcommand=scrollbar_x.set)

    frame_widgets_estoque = CTkScrollableFrame(tela_estoque, width=int(0.3 * largura_tela), height=altura_tela)
    frame_widgets_estoque.pack(side='left', fill="both", expand=True)

    # Widgets no FrameFB
    ttk.Label(frame_widgets_estoque)
    nome_entry = ttk.Entry(frame_widgets_estoque)
    nome_entry.insert(0, "Nome do Produto")
    nome_entry.bind("<FocusIn>", lambda e: nome_entry.delete('0','end'))
    nome_entry.pack(pady=90, padx=20, fill="x")

    qtd_entry = ttk.Entry(frame_widgets_estoque)
    qtd_entry.insert(0,"Quantidade")
    qtd_entry.bind("<FocusIn>", lambda e: qtd_entry.delete('0','end'))
    qtd_entry.pack(pady=10, padx=20, fill="x")

    un_entry = ttk.Entry(frame_widgets_estoque)
    un_entry.insert(0,"Unidade")
    un_entry.bind("<FocusIn>", lambda e: un_entry.delete('0','end'))
    un_entry.pack(pady=10, padx=20, fill="x")

    preco_compra_entry = ttk.Entry(frame_widgets_estoque)
    preco_compra_entry.insert(0,"Preço de Compra")
    preco_compra_entry.bind("<FocusIn>", lambda e: preco_compra_entry.delete('0','end'))
    preco_compra_entry.pack(pady=10, padx=20, fill="x")

    preco_venda_entry = ttk.Entry(frame_widgets_estoque)
    preco_venda_entry.insert(0,"Preço de Venda")
    preco_venda_entry.bind("<FocusIn>", lambda e: preco_venda_entry.delete('0','end'))
    preco_venda_entry.pack(pady=10, padx=20, fill="x")

    forn_entry = ttk.Entry(frame_widgets_estoque)
    forn_entry.insert(0,"Fornecedor")
    forn_entry.bind("<FocusIn>", lambda e: forn_entry.delete('0','end'))
    forn_entry.pack(pady=10, padx=20, fill="x")

    val_entry = ttk.Entry(frame_widgets_estoque)
    val_entry.insert(0,"Validade")
    val_entry.bind("<FocusIn>", lambda e: val_entry.delete('0','end'))
    val_entry.pack(pady=10, padx=20, fill="x")

    botao = ttk.Button(frame_widgets_estoque, text="Inserir", command=inserir_item)
    botao.pack(pady=10, padx=20, fill="x")

    separator = ttk.Separator(frame_widgets_estoque)
    separator.pack(pady=10, padx=20, fill="x")

    nome_entry_pes = ttk.Entry(frame_widgets_estoque)
    nome_entry_pes.insert(0, "Nome do Produto")
    nome_entry_pes.bind("<FocusIn>", lambda e: nome_entry_pes.delete('0','end'))
    nome_entry_pes.pack(pady=10, padx=20, fill="x")

    botao_pes = ttk.Button(frame_widgets_estoque, text="Pesquisar",command=pesquisar_produto)
    botao_pes.pack(pady=10, padx=20, fill="x")
        
    botao_vw = ttk.Button(frame_widgets_estoque, text="Limpar Pesquisa",command=limpar_pesquisa)
    botao_vw.pack(pady=10, padx=20, fill="x")

    botao_vw_cdb = ttk.Button(frame_widgets_estoque, text="Ver Código de Barras", command=exibir_codigo_barras_selecionado)
    botao_vw_cdb.pack(pady=10, padx=20, fill="x")

    botao_pesq_cdb= ttk.Button(frame_widgets_estoque, text="Pesquisar Código de Barras", command=pesquisar_codigo_de_barras)
    botao_pesq_cdb.pack(pady=10, padx=20, fill="x")

    botao_back = ttk.Button(frame_widgets_estoque, text="Voltar", command=voltar_menu)
    botao_back.pack(pady=10, padx=20, fill="x")
    try:
            conn = sqlite3.connect(caminh_banco)
            cursor = conn.cursor()

            cursor.execute("SELECT nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras FROM fisico")
            rows = cursor.fetchall()

            treeviewF.delete(*treeviewF.get_children())

            cols = ["Produto", "QTD", "UN", "Preço de Venda","Preço de Compra","Fornecedor","Validade", "Código Barras"]
            treeviewF["columns"] = cols

            for col_name in cols:
                treeviewF.heading(col_name, text=col_name)
                treeviewF.column(col_name, anchor=tkinter.CENTER)

            for row in rows:
                treeviewF.insert('', tkinter.END, values=row)
            treeviewF.pack(expand=True, fill="both")  
            messagebox.showinfo("Aviso!","Dados carregados com sucesso!")
    except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados do banco de dados: {str(e)}")
    finally:
            if conn:
                conn.close()

def inserir_item():
    try:
        prod = nome_entry.get()
        qtd = qtd_entry.get()
        un = un_entry.get()
        preco_compra = preco_compra_entry.get()
        preco_venda = preco_venda_entry.get()
        fornecedor = forn_entry.get()
        val = val_entry.get()
        if not all([prod, qtd, un, preco_compra, preco_venda, fornecedor, val]) or prod == "Nome do Produto" or qtd == "Quantidade" or val == "Validade" or un == "Unidade" or preco_compra =="Preço de Compra" or preco_venda =="Preço de Venda" or fornecedor =="Fornecedor": 
            messagebox.showwarning("Aviso!", "Preencha todos os campos")
        else:
            if validar_data(val):
                data_formatada = datetime.strptime(val, "%d/%m/%Y").strftime("%d/%m/%Y")
                prod = nome_entry.get()
                qtd = qtd_entry.get()
                un = un_entry.get()
                preco_compra = preco_compra_entry.get()
                preco_venda = preco_venda_entry.get()
                fornecedor = forn_entry.get()
                val = data_formatada
                # Inserir a nova linha no Treeview
                codigo = gerar_codigo_barras_unico()
                codigo_barras = gerar_codigo_barras(codigo)
                
                dados = (prod,int(qtd),un,float(preco_venda),float(preco_compra),fornecedor, val, codigo_barras)
                dados_entrada = (prod,int(qtd),un,float(preco_venda),float(preco_compra),fornecedor, val, codigo_barras, dia_atual,nome_mes)

                treeviewF.insert('', tkinter.END, values=dados)
                conn = sqlite3.connect(caminh_banco)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO fisico (nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dados)
                conn.commit()
                conn.close()

                conn = sqlite3.connect(caminh_banco)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO entrada (nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras, data_entrada, mes_entrada) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dados_entrada)
                conn.commit()
                conn.close()

                        # Limpar os widgets de entrada após a inserção
                nome_entry.delete(0, tkinter.END)
                qtd_entry.delete(0, tkinter.END)
                un_entry.delete(0, tkinter.END)
                preco_compra_entry.delete(0, tkinter.END)
                preco_venda_entry.delete(0, tkinter.END)
                forn_entry.delete(0, tkinter.END)
                val_entry.delete(0, tkinter.END)

                nome_entry.insert(0,"Nome do Produto")
                qtd_entry.insert(0,"Quantidade")
                un_entry.insert(0,"Unidade")
                preco_compra_entry.insert(0,"Preço de Compra")
                preco_venda_entry.insert(0,"Preço de Venda")
                forn_entry.insert(0,"Fornecedor")
                val_entry.insert(0,"Validade")


                messagebox.showinfo("Aviso!","Item inserido com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir item: {str(e)}")

def validar_data(entrada):
    global data
    try:
        # Tenta converter a entrada para um objeto de data
        data = datetime.strptime(entrada, "%d/%m/%Y").date()
        return True
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Utilize DD/MM/AAAA.")
        return False

def gerar_sequencia_aleatoria():
    sequencia = ''.join(str(random.randint(0, 9)) for _ in range(12))
    return str(sequencia)

def codigo_barras_existe_no_bd(codigo_barras):
    conn = sqlite3.connect(caminh_banco)   
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fisico WHERE codigo_barras = ?", (codigo_barras,))
    quantidade = cursor.fetchone()[0]
    conn.close()
    return quantidade > 0

def gerar_codigo_barras_unico():
    while True:
        nova_sequencia = gerar_sequencia_aleatoria()
        if not codigo_barras_existe_no_bd(nova_sequencia):
            return str(nova_sequencia)

def gerar_codigo_barras(codigo):
    return str(EAN13(codigo, writer=ImageWriter()))

def gerar_codigo_barras_img(codigo):
    return EAN13(codigo, writer=ImageWriter())

def pesquisar_produto():
    nome_pesq = nome_entry_pes.get().lower()

    try:
        conn = sqlite3.connect(caminh_banco)
        cursor = conn.cursor()

        cursor.execute(f"SELECT nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras FROM fisico WHERE nome_produto = '{nome_pesq}'")
        rows = cursor.fetchall()

        treeviewF.delete(*treeviewF.get_children())

        cols = ["Produto", "QTD", "UN", "Preço de Venda","Preço de Compra","Fornecedor","Validade", "Código Barras"]
        treeviewF["columns"] = cols

        for col_name in cols:
            treeviewF.heading(col_name, text=col_name)
            treeviewF.column(col_name, anchor=tkinter.CENTER)

        for row in rows:
            treeviewF.insert('', tkinter.END, values=row)

    except Exception as e:
        messagebox.showerror("Erro", f"Item não encontrado: {str(e)}")
    finally:
        if conn:
            conn.close()

def limpar_pesquisa():
    try:
            conn = sqlite3.connect(caminh_banco)
            cursor = conn.cursor()

            cursor.execute("SELECT nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras FROM fisico")
            rows = cursor.fetchall()

            treeviewF.delete(*treeviewF.get_children())

            cols = ["Produto", "QTD", "UN", "Preço de Venda","Preço de Compra","Fornecedor","Validade", "Código Barras"]
            treeviewF["columns"] = cols

            for col_name in cols:
                treeviewF.heading(col_name, text=col_name)
                treeviewF.column(col_name, anchor=tkinter.CENTER)

            for row in rows:
                treeviewF.insert('', tkinter.END, values=row)
            treeviewF.pack(expand=True, fill="both")  
            messagebox.showinfo("Aviso!","Dados carregados com sucesso!")
    except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados do banco de dados: {str(e)}")
    finally:
            if conn:
                conn.close()

def exibir_codigo_barras_selecionado():
    #Obtém o item selecionado na treeview
    item_selecionado = treeviewF.selection()

    if item_selecionado:
        #Obtém o código de barras associado ao item selecionado
        codigo_barras = treeviewF.item(item_selecionado, 'values')[7]
        produto = treeviewF.item(item_selecionado, 'values')[0]

        # Exibe o código de barras na nova janela
        codigo = gerar_codigo_barras_img(codigo_barras)
        codigo_imagem = ImageTk.PhotoImage(codigo.render())

        tela_estoque.withdraw()

        global tela_cod_de_barras

        tela_cod_de_barras = CTkToplevel()
        tela_cod_de_barras.geometry("{}x{}+0+0".format(largura_tela, altura_tela))
        tela_cod_de_barras.title("Estoque - Código de Barras")
        tela_cod_de_barras.protocol("WM_DELETE_WINDOW", sair_do_app)

        CTkLabel(master=tela_cod_de_barras, text="", image=img_lat).pack(expand=True, side="left")

        #Traz a imagem gerada do Código de Barras
        frame_cod_de_barras = CTkScrollableFrame(master=tela_cod_de_barras, width= int(0.6 * largura_tela), height=int(altura_tela), fg_color="#ffffff")
        frame_cod_de_barras.pack_propagate(0)
        frame_cod_de_barras.pack(expand=True, side="right")

        frame_info_cod_de_barras = ttk.Frame(frame_cod_de_barras)
        frame_info_cod_de_barras.grid(row=0, column=0, padx=10, pady=10)

        CTkLabel(master=frame_info_cod_de_barras, text="-----------------", text_color="#ffffff", anchor="w", justify="left", font=("Arial Bold", 18)).grid(row=1, column=0, padx=10, pady=10)
        CTkLabel(master=frame_info_cod_de_barras, text=f"Estoque - Código de Barras - {produto} ", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 18)).grid(row=1, column=1, padx=10, pady=10)   
        CTkLabel(master=frame_info_cod_de_barras, text="--------------", text_color="#ffffff", anchor="w", justify="left", font=("Arial Bold", 18)).grid(row=1, column=2, padx=10, pady=10)        
        CTkButton(master=frame_info_cod_de_barras, text="Voltar", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=voltar_tela_cdb).grid(row=1, column=3, padx=10, pady=10)

        frame_img_cd_barras = ttk.Label(frame_info_cod_de_barras, image=codigo_imagem)
        frame_img_cd_barras.image = codigo_imagem
        frame_img_cd_barras.grid(row=2, column=1, padx=10, pady=10)
        CTkButton(master=frame_info_cod_de_barras, text="Imprimir", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=lambda: salvar_imagem(produto, codigo_imagem, codigo_barras)).grid(row=4, column=1, padx=10, pady=10)

    else:
        messagebox.showinfo("Aviso!", "escolha o item que você gostaria de acessar o Código de barras")

def salvar_imagem(produto, imagem, cbar):
    diretorio_projeto = os.getcwd()
    print(diretorio_projeto)
    file_path = f"{diretorio_projeto}\códigos_de_barras\{produto} - {cbar}.png"

    #Converte a imagem
    imagem_pil = ImageTk.getimage(imagem)

    #Salva a imagem no diretório
    imagem_pil.save(file_path)

    messagebox.showinfo("Sucesso", f"Imagem do código de barras salva em {file_path}")

def voltar_tela_cdb():
    tela_cod_de_barras.withdraw()
    tela_estoque.deiconify()

def pesquisar_codigo_de_barras():
    global tela_saida, frame_saida
    global cd_entry
    tela_estoque.withdraw()

    tela_saida = CTkToplevel()
    tela_saida.geometry("{}x{}+0+0".format(largura_tela, altura_tela))
    tela_saida.title("Estoque")
    tela_saida.protocol("WM_DELETE_WINDOW", sair_do_app)

    CTkLabel(master=tela_saida, text="", image=img_lat).pack(expand=True, side="left")

    frame_cabecalho_saida = CTkFrame(master=tela_saida, width=int(0.6 * largura_tela), height=int(0.14 * altura_tela))
    frame_cabecalho_saida.pack(expand=True, side="top")

    CTkButton(master=frame_cabecalho_saida, text="Voltar", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=voltar_pesq_cdb).pack(anchor="w", pady=(0,0), padx=(int(0.55*frame_cabecalho_saida.winfo_screenwidth()), 0))
    CTkLabel(master=frame_cabecalho_saida, text="Estoque - Pesquisar Código de Barras", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 18)).pack(anchor="w", pady=(10,0), padx=(0, 0))

    frame_saida_scroll = CTkScrollableFrame(master=tela_saida, width= int(0.6 * largura_tela), height=int(0.85 * altura_tela), fg_color="#ffffff")
    frame_saida_scroll.pack(expand=True, side="right")

    frame_saida = ttk.Frame(frame_saida_scroll)
    frame_saida.grid(row=0, column=0, padx=10, pady=20)

    CTkLabel(master=frame_saida, text="-------------------", text_color="#ffffff", anchor="w", justify="left", font=("Arial Bold", 18)).grid(row=1, column=0, padx=10, pady=20)
    CTkLabel(master=frame_saida, text="Estoque - Pesquisar Código de Barras", text_color="#ffffff", anchor="w", justify="left", font=("Arial Bold", 18)).grid(row=1, column=1, padx=10, pady=20)
    cd_entry = CTkEntry(master=frame_saida, width=225, fg_color="#EEEEEE", border_color="#00009C", border_width=1, text_color="#000000")
    cd_entry.grid(row=2, column=1, padx=10, pady=20)
    CTkButton(master=frame_saida, text="Escanear", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=escanear_codigo_de_barras).grid(row=3, column=1, padx=10, pady=20)

def escanear_codigo_de_barras():
    global codigo_pesquisado, produto_cde
    # Capturar a entrada
    codigo_pesquisado = cd_entry.get()

    try:
            diretorio_projeto = os.getcwd()
            conn = sqlite3.connect(caminh_banco)
            cursor = conn.cursor()

            cursor.execute(f"SELECT nome_produto FROM fisico WHERE codigo_barras = '{codigo_pesquisado}'")
            produto_cd = cursor.fetchone()
            conn.close()
            if produto_cd:
                produto_cde = produto_cd[0]

                imagem_cd_pesquisado = f"{diretorio_projeto}/códigos_de_barras/{produto_cde} - {codigo_pesquisado}.png"  
                imagem_cd_pesquisado_pillow = Image.open(imagem_cd_pesquisado)

                imagem_cd_pesquisado_tk = ImageTk.PhotoImage(imagem_cd_pesquisado_pillow)

                frame_saida_cdbarras = ttk.Label(frame_saida, image=imagem_cd_pesquisado_tk)
                frame_saida_cdbarras.image = imagem_cd_pesquisado_tk  
                frame_saida_cdbarras.grid(row=3, column=1, padx=10, pady=10)
                CTkLabel(master=frame_saida, text=f"Produto - {produto_cde}", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 18)).grid(row=4, column=1, padx=10, pady=10)
                
                CTkButton(master=frame_saida, text="Ver Informações", fg_color="#00009C", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=mostrar_info_produto_pesquisado).grid(row=5, column=1, pady=10)
                CTkButton(master=frame_saida, text="Excluir", fg_color="#00009C", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=inserir_info_para_saida).grid(row=6, column=1, padx=10, pady=10)          
            else:
                messagebox.showerror("Aviso!", "Item não encontrado")

    except Exception as e:
        messagebox.showerror("Erro!", f"{str(e)}")

def mostrar_info_produto_pesquisado():
    tela_saida.withdraw()
    tela_estoque.deiconify()
    try:
        conn = sqlite3.connect(caminh_banco)
        cursor = conn.cursor()

        cursor.execute(f"SELECT nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras FROM fisico WHERE nome_produto = '{produto_cde}'")
        rows = cursor.fetchall()

        treeviewF.delete(*treeviewF.get_children())

        cols = ["Produto", "QTD", "UN", "Preço de Venda","Preço de Compra","Fornecedor","Validade", "Código Barras"]
        treeviewF["columns"] = cols

        for col_name in cols:
            treeviewF.heading(col_name, text=col_name)
            treeviewF.column(col_name, anchor=tkinter.CENTER)

        for row in rows:
            treeviewF.insert('', tkinter.END, values=row)

    except Exception as e:
        messagebox.showerror("Erro", f"Item não encontrado: {str(e)}")
    finally:
        if conn:
            conn.close()

def voltar_pesq_cdb():
    tela_saida.withdraw()
    tela_estoque.deiconify()
    try:
            conn = sqlite3.connect(caminh_banco)
            cursor = conn.cursor()

            cursor.execute("SELECT nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras FROM fisico")
            rows = cursor.fetchall()

            treeviewF.delete(*treeviewF.get_children())

            cols = ["Produto", "QTD", "UN", "Preço de Venda","Preço de Compra","Fornecedor","Validade", "Código Barras"]
            treeviewF["columns"] = cols

            for col_name in cols:
                treeviewF.heading(col_name, text=col_name)
                treeviewF.column(col_name, anchor=tkinter.CENTER)

            for row in rows:
                treeviewF.insert('', tkinter.END, values=row)
            treeviewF.pack(expand=True, fill="both")
            messagebox.showinfo("Aviso!","Dados carregados com sucesso!")
    except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados do banco de dados: {str(e)}")
    finally:
            if conn:
                conn.close()

def inserir_info_para_saida():
    global quant
    CTkLabel(master=frame_saida, text="Digite a Quantidade que foi vendida", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 14)).grid(row=7, column=1, padx=10, pady=10)        
    quant = CTkEntry(master=frame_saida, width=225, fg_color="#EEEEEE", border_color="#00009C", border_width=1, text_color="#000000")
    quant.grid(row=8, column=1, padx=10, pady=10)
    CTkButton(master=frame_saida, text="Confirmar", fg_color="#00009C", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=retirar_item).grid(row=13, column=1, padx=10, pady=10)        

def retirar_item():
    codigo = codigo_pesquisado

    if not quant.get():
        messagebox.showwarning("Aviso", "Por favor, insira a quantidade desejada para excluir.")
        return
    try:
        quantidade = int(quant.get())
    except ValueError:
        messagebox.showerror("Erro", "A quantidade inserida não é um número válido.")
        return
    
    try:
        conn = sqlite3.connect(caminh_banco)
        cursor = conn.cursor()

        # Obter a quantidade atual do banco de dados
        cursor.execute(f"SELECT nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras FROM fisico WHERE codigo_barras = '{codigo}'")
        resultado_qtd = cursor.fetchone()

        if resultado_qtd:
            produto = str(resultado_qtd[0])
            qtd =  int(resultado_qtd[1])
            un =  str(resultado_qtd[2])
            preco_venda = str(resultado_qtd[3])
            preco_compra =  str(resultado_qtd[4])
            fornecedor =  str(resultado_qtd[5])
            valid =  str(resultado_qtd[6])
            cd_bar =  str(resultado_qtd[7])

            if quantidade < qtd:
                # Atualizar a quantidade no banco de dados
                nova_quantidade = qtd - quantidade
                cursor.execute(f"UPDATE fisico SET qtd = {nova_quantidade} WHERE codigo_barras = '{codigo}'")
                conn.commit()

                dados_saida = (produto,int(quantidade),un,float(preco_venda),float(preco_compra), fornecedor, valid, cd_bar, dia_atual, nome_mes)

                conn = sqlite3.connect(caminh_banco)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO saida (nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras, data_saida,mes_saida) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dados_saida)
                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", f"{quantidade} removidos com sucesso.")
            elif quantidade == qtd:
                # Deletar completamente o item do banco de dados
                cursor.execute(f"DELETE FROM fisico WHERE codigo_barras = '{codigo}'")
                conn.commit()

                dados_saida = (produto,int(quantidade),un,float(preco_venda),float(preco_compra), fornecedor, valid, cd_bar, dia_atual, nome_mes)

                conn = sqlite3.connect(caminh_banco)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO saida (nome_produto, qtd, un, preco_venda, preco_compra, fornecedor, validade, codigo_barras, data_saida, mes_saida) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dados_saida)
                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Item completamente removido do banco de dados.")
            else:
                messagebox.showerror("Erro", "Quantidade a ser deletada é maior que a quantidade atual.")
        else:
            messagebox.showerror("Erro", "Material não encontrado no banco de dados.")

    except Exception as e:
        messagebox.showerror("Erro", f"{str(e)}")
    finally:
        if conn:
            conn.close()

def voltar_menu():
    tela_estoque.withdraw()
    tela_menu.deiconify()

def menu_graficos():
    global tela_menu_graf
    tela_menu.withdraw()

    tela_menu_graf = CTkToplevel()
    tela_menu_graf.geometry("{}x{}+0+0".format(largura_tela, altura_tela))
    tela_menu_graf.title('Estoque - Menu - Gráficos')
    tela_menu_graf.protocol("WM_DELETE_WINDOW", sair_do_app)

    CTkLabel(master=tela_menu_graf, text="", image=img_lat).pack(expand=True, side="left")

    frame_cabecalho_graf = CTkFrame(master=tela_menu_graf, width=int(0.6 * largura_tela), height=int(0.14 * altura_tela))
    frame_cabecalho_graf.pack(expand=True, side="top")

    CTkLabel(master=frame_cabecalho_graf, text="------------------------------------- Estoque -------------------------------------", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="w", pady=(0,0), padx=(0, 0))

    scrollable_frame_graf = CTkScrollableFrame(master=tela_menu_graf, width=int(0.6 * largura_tela), height=int(0.85 * altura_tela), fg_color="#ffffff")
    scrollable_frame_graf.pack(expand=True, side="right")

    frame_tela_graf = CTkFrame(master=scrollable_frame_graf, fg_color="#ffffff")
    frame_tela_graf.pack(expand=True, anchor="w", pady=(10, 0))

    CTkLabel(master=frame_tela_graf, text="Gráficos", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 28), compound="left").pack(anchor="w", pady=(10, 0), padx=(20, 0))

    CTkLabel(master=frame_tela_graf, text="  Acompanhamento de Entrada/Saída:", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(70, 0), padx=(int(0.2*frame_tela_graf.winfo_screenwidth()), 0))
    CTkButton(master=frame_tela_graf, text="Ver Gráficos", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=graf_entrada_saida).pack(anchor="w", pady=(15, 0), padx=(int(0.2*frame_tela_graf.winfo_screenwidth()), 0))

    CTkLabel(master=frame_tela_graf, text="  Acompanhamento Estoque Físico:", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(35, 0), padx=(int(0.2*frame_tela_graf.winfo_screenwidth()), 0))
    CTkButton(master=frame_tela_graf, text="Ver Gráficos", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=graf_estoque).pack(anchor="w", pady=(15, 0), padx=(int(0.2*frame_tela_graf.winfo_screenwidth()), 0))

    CTkLabel(master=frame_tela_graf, text="  Voltar", text_color="#00009C", anchor="w", justify="center", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(35, 0), padx=(int(0.24*frame_tela_graf.winfo_screenwidth()), 0))
    CTkButton(master=frame_tela_graf, text="Voltar ao Menu", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=voltar_menu_visib).pack(anchor="w", pady=(15, 0), padx=(int(0.2*frame_tela_graf.winfo_screenwidth()), 0))

def graf_estoque():
    tela_menu_graf.withdraw()

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(caminh_banco)
    df_estoque_visib= pd.read_sql_query("SELECT nome_produto, qtd, fornecedor, preco_compra FROM fisico",conn)

    conn.close()

    df_estoque_visib['qtd'] = df_estoque_visib['qtd'].astype(int)
    df_estoque_visib['preco_compra'] = df_estoque_visib['preco_compra'].astype(float)

    global tela_graf_estoque

    tela_graf_estoque = CTkToplevel()
    tela_graf_estoque.geometry("{}x{}+0+0".format(largura_tela, altura_tela))
    tela_graf_estoque.title("Estoque - Estoque Físico - Gráficos")
    tela_graf_estoque.protocol("WM_DELETE_WINDOW", sair_do_app)

    frame_scroll_graf_estoque = CTkScrollableFrame(master=tela_graf_estoque, width= int(largura_tela), height=int(altura_tela), fg_color="#ffffff")
    frame_scroll_graf_estoque.pack_propagate(0)
    frame_scroll_graf_estoque.pack(expand=True, side="right")

    frame_cabecalho_graf_estoque = ttk.Frame(frame_scroll_graf_estoque)
    frame_cabecalho_graf_estoque.grid(row=0, column=0, padx=60, pady=10)

    CTkButton(master=frame_cabecalho_graf_estoque, text="Voltar", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=voltar_graf_estoque).grid(row=1, column=1, padx=10, pady=10)
    CTkLabel(master=frame_cabecalho_graf_estoque, text="Estoque - Gráficos Estoque Físico", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 24)).grid(row=1, column=0, padx=10, pady=10)

    #Criar gráfico de barras para Quantidade por Produto
    df_agrupado_prod_qtd = df_estoque_visib.groupby('nome_produto')['qtd'].sum().reset_index()
    plt.figure(figsize=(7, 4))
    bars1 = plt.bar(df_agrupado_prod_qtd['nome_produto'], df_agrupado_prod_qtd['qtd'], color='blue')
    plt.xlabel('Produtos')
    plt.ylabel('Quantidade')
    plt.title('Quantidade por Produto')
    plt.xticks(rotation=20, ha='right',  fontsize=6)
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_qtd_prod = ttk.Frame(frame_scroll_graf_estoque)
    frame_grafico_qtd_prod.grid(row=2, column=0, padx=10, pady=10)

    canvas_qtd_prod = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_qtd_prod)
    canvas_qtd_prod.draw()
    canvas_qtd_prod.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()

    #Criar gráfico de barras para qtd por Fornecedor
    df_agrupado_forn_qtd = df_estoque_visib.groupby('fornecedor')['qtd'].sum().reset_index()
    plt.figure(figsize=(7, 4))
    bars1 = plt.bar(df_agrupado_forn_qtd['fornecedor'], df_agrupado_forn_qtd['qtd'], color='blue')
    plt.xlabel('Fornecedores')
    plt.ylabel('Quantidade')
    plt.title('Quantidade por Fornecedor')
    plt.xticks(rotation=20, ha='right',  fontsize=6)
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_qtd_forn = ttk.Frame(frame_scroll_graf_estoque)
    frame_grafico_qtd_forn.grid(row=2, column=1, padx=10, pady=10)

    canvas_qtd_forn = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_qtd_forn)
    canvas_qtd_forn.draw()
    canvas_qtd_forn.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()

    #Criar gráfico de barras para Custo por Produto
    df_agrupado_prod_custo = df_estoque_visib.groupby('nome_produto')['preco_compra'].sum().reset_index()
    plt.figure(figsize=(7, 4))
    bars1 = plt.bar(df_agrupado_prod_custo['nome_produto'], df_agrupado_prod_custo['preco_compra'], color='blue')
    plt.xlabel('Produtos')
    plt.ylabel('Custo')
    plt.title('Custo por Produto')
    plt.xticks(rotation=20, ha='right',  fontsize=6)
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_custo_prod = ttk.Frame(frame_scroll_graf_estoque)
    frame_grafico_custo_prod.grid(row=3, column=0, padx=10, pady=10)

    canvas_custo_prod = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_custo_prod)
    canvas_custo_prod.draw()
    canvas_custo_prod.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()

    #Criar gráfico de barras para Custo por Fornecedor
    df_agrupado_forn_custo = df_estoque_visib.groupby('fornecedor')['preco_compra'].sum().reset_index()
    plt.figure(figsize=(7, 4))
    bars1 = plt.bar(df_agrupado_forn_custo['fornecedor'], df_agrupado_forn_custo['preco_compra'], color='blue')
    plt.xlabel('Fornecedores')
    plt.ylabel('Custo')
    plt.title('Custo por Fornecedor')
    plt.xticks(rotation=20, ha='right',  fontsize=6)
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_custo_forn = ttk.Frame(frame_scroll_graf_estoque)
    frame_grafico_custo_forn.grid(row=3, column=1, padx=10, pady=10)

    canvas_custo_forn = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_custo_forn)
    canvas_custo_forn.draw()
    canvas_custo_forn.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()

def voltar_graf_estoque():
    tela_graf_estoque.withdraw()
    tela_menu_graf.deiconify()

def graf_entrada_saida():
    tela_menu_graf.withdraw()
    global df_entrada, df_saida, combo_produto,  combo_mes, frame_graf_scroll_entrada_saida
    global frame_grafico_entrada_produto, frame_grafico_saida_produto 
    conn = sqlite3.connect(caminh_banco)

    df_entrada= pd.read_sql_query("SELECT * FROM entrada",conn)
    df_saida= pd.read_sql_query("SELECT * FROM saida",conn)

    conn.close()

    df_entrada['qtd'] = df_entrada['qtd'].astype(int)
    df_entrada['preco_compra'] = df_entrada['preco_compra'].astype(float)
    df_entrada['preco_venda'] = df_entrada['preco_venda'].astype(float)

    df_saida['qtd'] = df_saida['qtd'].astype(int)
    df_saida['preco_compra'] = df_saida['preco_compra'].astype(float)
    df_saida['preco_venda'] = df_saida['preco_venda'].astype(float)

    produtos_entrada = [item for item in df_entrada['nome_produto']]
    mes_entrada = [item for item in df_entrada['mes_entrada']]

    produtos_saida = [item for item in df_saida['nome_produto']]
    mes_saida = [item for item in df_saida['mes_saida']]

    global tela_graf_entrada_saida

    tela_graf_entrada_saida = CTkToplevel()
    tela_graf_entrada_saida.geometry("{}x{}+0+0".format(largura_tela, altura_tela))
    tela_graf_entrada_saida.title("Estoque - Histórico Entrada/Saída")
    tela_graf_entrada_saida.protocol("WM_DELETE_WINDOW", sair_do_app)

    frame_cabecalho_entrada_saida = CTkFrame(master=tela_graf_entrada_saida, width=int(0.6 * largura_tela), height=int(0.14 * altura_tela), fg_color="#ffffff")
    frame_cabecalho_entrada_saida.pack(expand=True, side="top")

    frame_filtro_entrada_saida = ttk.Frame(frame_cabecalho_entrada_saida)
    frame_filtro_entrada_saida.grid(row=0, column=0, padx=10, pady=10)

    CTkButton(master=frame_filtro_entrada_saida, text="Voltar", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=50, command=voltar_graf_entrada_saida).grid(row=1, column=2, padx=10, pady=10)
    CTkLabel(master=frame_filtro_entrada_saida, text="Estoque - Histórico Entrada/Saída", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 24)).grid(row=1, column=0, padx=10, pady=10)
    
    produtos_unicos = list(set(produtos_entrada + produtos_saida))
    combo_produto = ttk.Combobox(master=frame_filtro_entrada_saida, values=produtos_unicos)
    combo_produto.grid(row=2, column=0, padx=10, pady=10)
    combo_produto.set("Selecione um Produto")

    meses_unicos = list(set(mes_entrada + mes_saida))
    combo_mes = ttk.Combobox(master=frame_filtro_entrada_saida, values=meses_unicos)
    combo_mes.grid(row=2, column=1, padx=20, pady=10)
    combo_mes.set("Selecione um Mês")

    btn_filtro = CTkButton(master=frame_filtro_entrada_saida, width=10, text="Filtrar", command=filtro_entrada_saida)
    btn_filtro.grid(row=3, column=0, padx=10, pady=10)

    btn_limpar_filtro = CTkButton(master=frame_filtro_entrada_saida, width=10, text="Limpar Filtro", command=limpar_filtro_graf_entrada_saida)
    btn_limpar_filtro.grid(row=3, column=1, padx=10, pady=10)
    
    frame_graf_scroll_entrada_saida = CTkScrollableFrame(master=tela_graf_entrada_saida, width= int(largura_tela), height=int(altura_tela), fg_color="#ffffff")
    frame_graf_scroll_entrada_saida.pack_propagate(0)
    frame_graf_scroll_entrada_saida.pack(expand=True, side="right")

    frame_graf_entrada_saida = ttk.Frame(frame_graf_scroll_entrada_saida)
    frame_graf_entrada_saida.grid(row=0, column=0, padx=10, pady=10)

    # Fazer Gráfico de Barras de Entrada de Produtos por dia
    df_agrupado_entrada = df_entrada.groupby('data_entrada')['qtd'].sum().reset_index()
    plt.figure(figsize=(9, 5.5))
    bars_ent = plt.bar(df_agrupado_entrada['data_entrada'], df_agrupado_entrada['qtd'], color='blue')
    plt.xlabel('Data')
    plt.ylabel('Quantidade')
    plt.title('Entrada (Quantidade) por Dia')
    plt.xticks(rotation=30, ha='right')

    for bar in bars_ent:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_entrada_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
    frame_grafico_entrada_produto.grid(row=2, column=1, padx=10, pady=10)

    canvas_entrada_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_entrada_produto)
    canvas_entrada_produto.draw()
    canvas_entrada_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()
    
    # Fazer Gráfico de Barras de Saida de Produtos por dia
    df_agrupado_saida = df_saida.groupby('data_saida')['qtd'].sum().reset_index()
    plt.figure(figsize=(9, 5.5))
    bars_sai = plt.bar(df_agrupado_saida['data_saida'], df_agrupado_saida['qtd'], color='red')
    plt.xlabel('Data')
    plt.ylabel('Quantidade')
    plt.title('Saída (Quantidade) por Dia')
    plt.xticks(rotation=30, ha='right')

    for bar in bars_sai:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_saida_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
    frame_grafico_saida_produto.grid(row=2, column=2, padx=10, pady=10)

    canvas_saida_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_saida_produto)
    canvas_saida_produto.draw()
    canvas_saida_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()

def filtro_entrada_saida():
    global frame_grafico_entrada_produto, frame_grafico_saida_produto 
    if (combo_produto.get() != "Selecione um Produto" or combo_produto.get() != "") and (combo_mes.get() == "Selecione um Mês" or combo_mes.get() == ""):
        frame_grafico_entrada_produto.destroy()
        frame_grafico_saida_produto.destroy()
        produto_selecionado = str(combo_produto.get())

        df_entrada['qtd'] = df_entrada['qtd'].astype(int)
        df_saida['qtd'] = df_saida['qtd'].astype(int)

        df_entrada['preco_venda'] = df_entrada['preco_venda'].astype(float)
        df_saida['preco_venda'] = df_saida['preco_venda'].astype(float)

        df_entrada['preco_compra'] = df_entrada['preco_compra'].astype(float)
        df_saida['preco_compra'] = df_saida['preco_compra'].astype(float)

        df_entrada_produto = df_entrada[df_entrada['nome_produto'] == produto_selecionado]
        df_saida_produto = df_saida[df_saida['nome_produto'] == produto_selecionado]
        
        df_agrupado_ent = df_entrada_produto.groupby('data_entrada')['qtd'].sum().reset_index()
        df_agrupado_sai = df_saida_produto.groupby('data_saida')['qtd'].sum().reset_index()
        
        plt.figure(figsize=(9, 5.5))
        bars_ent = plt.bar(df_agrupado_ent['data_entrada'], df_agrupado_ent['qtd'], color='blue')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.title('Entrada (Quantidade) por Dia')
        plt.xticks(rotation=30, ha='right')

        for bar in bars_ent:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval - 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'white')

        # Adicionar gráfico de barras ao frame
        frame_grafico_entrada_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
        frame_grafico_entrada_produto.grid(row=2, column=1, padx=10, pady=10)

        canvas_entrada_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_entrada_produto)
        canvas_entrada_produto.draw()
        canvas_entrada_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        plt.close()

        plt.figure(figsize=(9, 5.5))
        bars_sai = plt.bar(df_agrupado_sai['data_saida'], df_agrupado_sai['qtd'], color='red')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.title('Saída (Quantidade) por Dia')
        plt.xticks(rotation=30, ha='right')

        for bar in bars_sai:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval - 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'white')

        # Adicionar gráfico de barras ao frame
        frame_grafico_saida_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
        frame_grafico_saida_produto.grid(row=2, column=2, padx=10, pady=10)

        canvas_saida_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_saida_produto)
        canvas_saida_produto.draw()
        canvas_saida_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        plt.close()
    elif (combo_produto.get() == "Selecione um Produto" or combo_produto.get() == "") and (combo_mes.get() != "Selecione um Mês" or combo_mes.get() != ""):
        frame_grafico_entrada_produto.destroy()
        frame_grafico_saida_produto.destroy()
        mes_selecionado = combo_mes.get()
        df_entrada['qtd'] = df_entrada['qtd'].astype(int)
        df_entrada['mes_entrada'] = df_entrada['mes_entrada'].astype(str)
        df_saida['mes_saida'] = df_saida['mes_saida'].astype(str)
        df_saida['qtd'] = df_saida['qtd'].astype(int)
        df_entrada_produto = df_entrada[df_entrada['mes_entrada'] == mes_selecionado]
        df_saida_produto = df_saida[df_saida['mes_saida'] == mes_selecionado]
        
        df_agrupado_ent = df_entrada_produto.groupby('data_entrada')['qtd'].sum().reset_index()
        df_agrupado_sai = df_saida_produto.groupby('data_saida')['qtd'].sum().reset_index()

        plt.figure(figsize=(9, 5.5))
        bars_ent = plt.bar(df_agrupado_ent['data_entrada'], df_agrupado_ent['qtd'], color='blue')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.title('Entrada (Quantidade) por Dia')
        plt.xticks(rotation=30, ha='right')

        for bar in bars_ent:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval - 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'white')

        # Adicionar gráfico de barras ao frame
        frame_grafico_entrada_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
        frame_grafico_entrada_produto.grid(row=2, column=1, padx=10, pady=10)

        canvas_entrada_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_entrada_produto)
        canvas_entrada_produto.draw()
        canvas_entrada_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        plt.close()

        plt.figure(figsize=(9, 5.5))
        bars_sai = plt.bar(df_agrupado_sai['data_saida'], df_agrupado_sai['qtd'], color='red')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.title('Saída (Quantidade) por Dia')
        plt.xticks(rotation=30, ha='right')

        for bar in bars_sai:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval - 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'white')

        # Adicionar gráfico de barras ao frame
        frame_grafico_saida_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
        frame_grafico_saida_produto.grid(row=2, column=2, padx=10, pady=10)

        canvas_saida_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_saida_produto)
        canvas_saida_produto.draw()
        canvas_saida_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        plt.close()
    else:
        frame_grafico_entrada_produto.destroy()
        frame_grafico_saida_produto.destroy()
        mes_selecionado = combo_mes.get()

        df_entrada['qtd'] = df_entrada['qtd'].astype(int)
        df_saida['qtd'] = df_saida['qtd'].astype(int)

        produto_selecionado = str(combo_produto.get())
        df_entrada['nome_produto'] = df_entrada['nome_produto'].astype(str)
        df_saida['nome_produto'] = df_saida['nome_produto'].astype(str)

        df_entrada_produto = df_entrada[(df_entrada['nome_produto'] == produto_selecionado) & (df_entrada['mes_entrada'] == mes_selecionado)]
        df_saida_produto = df_saida[(df_saida['nome_produto'] == produto_selecionado) & (df_saida['mes_saida'] == mes_selecionado)]
        
        df_agrupado_ent = df_entrada_produto.groupby('data_entrada')['qtd'].sum().reset_index()
        df_agrupado_sai = df_saida_produto.groupby('data_saida')['qtd'].sum().reset_index()

        plt.figure(figsize=(9, 5.5))
        bars_ent = plt.bar(df_agrupado_ent['data_entrada'], df_agrupado_ent['qtd'], color='blue')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.title('Entrada (Quantidade) por Dia')
        plt.xticks(rotation=30, ha='right')

        for bar in bars_ent:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval - 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'white')

        # Adicionar gráfico de barras ao frame
        frame_grafico_entrada_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
        frame_grafico_entrada_produto.grid(row=2, column=1, padx=10, pady=10)

        canvas_entrada_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_entrada_produto)
        canvas_entrada_produto.draw()
        canvas_entrada_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        plt.close()

        plt.figure(figsize=(9, 5.5))
        bars_sai = plt.bar(df_agrupado_sai['data_saida'], df_agrupado_sai['qtd'], color='red')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.title('Saída (Quantidade) por Dia')
        plt.xticks(rotation=30, ha='right')

        for bar in bars_sai:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval - 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'white')

        # Adicionar gráfico de barras ao frame
        frame_grafico_saida_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
        frame_grafico_saida_produto.grid(row=2, column=2, padx=10, pady=10)

        canvas_saida_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_saida_produto)
        canvas_saida_produto.draw()
        canvas_saida_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        plt.close()

def limpar_filtro_graf_entrada_saida():
    global frame_grafico_entrada_produto, frame_grafico_saida_produto
    frame_grafico_entrada_produto.destroy()
    frame_grafico_saida_produto.destroy()
    conn = sqlite3.connect(caminh_banco)

    df_entrada= pd.read_sql_query("SELECT * FROM entrada",conn)
    df_saida= pd.read_sql_query("SELECT * FROM saida",conn)

    conn.close()

    df_entrada['qtd'] = df_entrada['qtd'].astype(int)
    df_entrada['preco_compra'] = df_entrada['preco_compra'].astype(float)
    df_entrada['preco_venda'] = df_entrada['preco_venda'].astype(float)

    df_saida['qtd'] = df_saida['qtd'].astype(int)
    df_saida['preco_compra'] = df_saida['preco_compra'].astype(float)
    df_saida['preco_venda'] = df_saida['preco_venda'].astype(float)

    # Fazer Gráfico de Barras de Entrada de Produtos por dia
    df_agrupado_entrada = df_entrada.groupby('data_entrada')['qtd'].sum().reset_index()
    plt.figure(figsize=(9, 5.5))
    bars_ent = plt.bar(df_agrupado_entrada['data_entrada'], df_agrupado_entrada['qtd'], color='blue')
    plt.xlabel('Data')
    plt.ylabel('Quantidade')
    plt.title('Entrada (Quantidade) por Dia')
    plt.xticks(rotation=30, ha='right')

    for bar in bars_ent:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_entrada_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
    frame_grafico_entrada_produto.grid(row=2, column=1, padx=10, pady=10)

    canvas_entrada_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_entrada_produto)
    canvas_entrada_produto.draw()
    canvas_entrada_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()

    # Fazer Gráfico de Barras de Saida de Produtos por dia
    df_agrupado_saida = df_saida.groupby('data_saida')['qtd'].sum().reset_index()
    plt.figure(figsize=(9, 5.5))
    bars_sai = plt.bar(df_agrupado_saida['data_saida'], df_agrupado_saida['qtd'], color='red')
    plt.xlabel('Data')
    plt.ylabel('Quantidade')
    plt.title('Saída (Quantidade) por Dia')
    plt.xticks(rotation=30, ha='right')

    for bar in bars_sai:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * plt.ylim()[1], round(yval, 2), ha='center', va='top', fontweight='bold' , color = 'black', fontsize=7)

    # Adicionar gráfico de barras ao frame
    frame_grafico_saida_produto = ttk.Frame(frame_graf_scroll_entrada_saida)
    frame_grafico_saida_produto.grid(row=2, column=2, padx=10, pady=10)

    canvas_saida_produto = FigureCanvasTkAgg(plt.gcf(), master=frame_grafico_saida_produto)
    canvas_saida_produto.draw()
    canvas_saida_produto.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    plt.close()

def voltar_graf_entrada_saida():
    tela_graf_entrada_saida.withdraw()
    tela_menu_graf.deiconify()

def voltar_menu_visib():
    tela_menu_graf.withdraw()
    tela_menu.deiconify()

def mostrar_senha():
    stat = check_senha_var.get()
    if stat == "on":
        passw.configure(show='')
    else:
        passw.configure(show='*')

check_senha_var = tkinter.StringVar(master=tela_login)

CTkLabel(master=tela_login, text="", image=img_lat).pack(expand=True, side="left")

frame_login = CTkFrame(master=tela_login, width= int(0.6 * largura_tela), height=int(altura_tela), fg_color="#ffffff")
frame_login.pack_propagate(0)
frame_login.pack(expand=True, side="right")

CTkLabel(master=frame_login, text="Bem Vindo(a)!", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(20, 5), padx=(25, 0))
CTkLabel(master=frame_login, text="Realize o Login", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame_login, text=" Login:", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 14), image=icone_user, compound="left").pack(anchor="w", pady=(100, 0), padx=(int(0.2*frame_login.winfo_screenwidth()), 0))
logn = CTkEntry(master=frame_login, width=225, fg_color="#EEEEEE", border_color="#00009C", border_width=1, text_color="#000000")
logn.pack(anchor="w", padx=(int(0.2*frame_login.winfo_screenwidth()), 0))

CTkLabel(master=frame_login, text=" Senha:", text_color="#00009C", anchor="w", justify="left", font=("Arial Bold", 14), image=icone_senha, compound="left").pack(anchor="w", pady=(21, 0), padx=(int(0.2*frame_login.winfo_screenwidth()), 0))
passw = CTkEntry(master=frame_login, width=225, fg_color="#EEEEEE", border_color="#00009C", border_width=1, text_color="#000000", show="*")
passw.pack(anchor="w", padx=(int(0.2*frame_login.winfo_screenwidth()), 0))

checkbox = CTkCheckBox(master=frame_login, text=" Mostrar Senha:", text_color="#00009C", font=("Arial Bold", 12),command=mostrar_senha,variable=check_senha_var, onvalue="on", offvalue="off").pack(anchor="w", pady=(25, 0), padx=(int(0.2*frame_login.winfo_screenwidth()), 0))

CTkButton(master=frame_login, text="Login", fg_color="#00009C", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=autenticacao).pack(anchor="w", pady=(40, 0), padx=(int(0.2*frame_login.winfo_screenwidth()), 0))
tela_login.protocol("WM_DELETE_WINDOW", sair_do_app)
tela_login.mainloop()
