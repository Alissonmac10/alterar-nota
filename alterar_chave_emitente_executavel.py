import tkinter as tk
from tkinter import filedialog, messagebox
from lxml import etree
import random


def carregar_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
    if arquivo:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, arquivo)


def gerar_chave_aleatoria():
    chave = ''.join(random.choices('0123456789', k=44))
    entrada_chave.delete(0, tk.END)
    entrada_chave.insert(0, chave)


def alterar_dados_e_salvar():
    caminho_arquivo_original = entrada_arquivo.get()
    chave = entrada_chave.get()
    cnpj_fornecedor = entrada_cnpj_fornecedor.get()
    nome_fornecedor = entrada_nome_fornecedor.get()
    cnpj_unidade_negocio = entrada_cnpj_unidade_negocio.get()
    nome_unidade_negocio = entrada_nome_unidade_negocio.get()

    if not caminho_arquivo_original:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo XML.")
        return

    try:
        # Carregar o arquivo XML original
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(caminho_arquivo_original, parser)
        root = tree.getroot()

        # Alterar a tag chNFe se houver chave especificada
        if chave:
            namespaces = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
            chNFe = root.find('.//ns:chNFe', namespaces=namespaces)

            if chNFe is not None:
                chNFe.text = chave
            else:
                messagebox.showerror("Erro", "A tag chNFe não foi encontrada no arquivo.")
                return

        # Alterar dados do fornecedor (emit)
        if cnpj_fornecedor or nome_fornecedor:
            emit = root.find('.//ns:emit', namespaces=namespaces)
            if emit is not None:
                if cnpj_fornecedor:
                    cnpj_fornecedor_tag = emit.find('.//ns:CNPJ', namespaces=namespaces)
                    if cnpj_fornecedor_tag is not None:
                        cnpj_fornecedor_tag.text = cnpj_fornecedor
                    else:
                        messagebox.showerror("Erro", "A tag CNPJ do fornecedor não foi encontrada no arquivo.")
                        return
                if nome_fornecedor:
                    nome_fornecedor_tag = emit.find('.//ns:xNome', namespaces=namespaces)
                    if nome_fornecedor_tag is not None:
                        nome_fornecedor_tag.text = nome_fornecedor
                    else:
                        messagebox.showerror("Erro", "A tag xNome do fornecedor não foi encontrada no arquivo.")
                        return
            else:
                messagebox.showerror("Erro", "A tag emit (fornecedor) não foi encontrada no arquivo.")
                return

        # Alterar dados da unidade de negócio (dest)
        if cnpj_unidade_negocio or nome_unidade_negocio:
            dest = root.find('.//ns:dest', namespaces=namespaces)
            if dest is not None:
                if cnpj_unidade_negocio:
                    cnpj_unidade_negocio_tag = dest.find('.//ns:CNPJ', namespaces=namespaces)
                    if cnpj_unidade_negocio_tag is not None:
                        cnpj_unidade_negocio_tag.text = cnpj_unidade_negocio
                    else:
                        messagebox.showerror("Erro", "A tag CNPJ da unidade de negócio não foi encontrada no arquivo.")
                        return
                if nome_unidade_negocio:
                    nome_unidade_negocio_tag = dest.find('.//ns:xNome', namespaces=namespaces)
                    if nome_unidade_negocio_tag is not None:
                        nome_unidade_negocio_tag.text = nome_unidade_negocio
                    else:
                        messagebox.showerror("Erro", "A tag xNome da unidade de negócio não foi encontrada no arquivo.")
                        return
            else:
                messagebox.showerror("Erro", "A tag dest (unidade de negócio) não foi encontrada no arquivo.")
                return

        # Solicitar um local para salvar o arquivo modificado
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Arquivos XML", "*.xml")])
        if caminho_salvar:
            tree.write(caminho_salvar, pretty_print=True, xml_declaration=True, encoding='utf-8')
            messagebox.showinfo("Sucesso", "Os dados foram alterados e o arquivo salvo.")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo: {e}")


# Configuração da Interface
root = tk.Tk()
root.title("Alterar Dados do XML")

# Widgets
tk.Label(root, text="Arquivo XML Original:").grid(row=0, column=0, padx=10, pady=10)
entrada_arquivo = tk.Entry(root, width=50)
entrada_arquivo.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Carregar", command=carregar_arquivo).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Chave:").grid(row=1, column=0, padx=10, pady=10)
entrada_chave = tk.Entry(root, width=40)
entrada_chave.grid(row=1, column=1, padx=10, pady=10, sticky="w")
tk.Button(root, text="Gerar", command=gerar_chave_aleatoria).grid(row=1, column=2, padx=10, pady=10, sticky="w")

tk.Label(root, text="CNPJ do Fornecedor:").grid(row=2, column=0, padx=10, pady=10)
entrada_cnpj_fornecedor = tk.Entry(root, width=50)
entrada_cnpj_fornecedor.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Nome do Fornecedor:").grid(row=3, column=0, padx=10, pady=10)
entrada_nome_fornecedor = tk.Entry(root, width=50)
entrada_nome_fornecedor.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="CNPJ da Unidade de Negócio:").grid(row=4, column=0, padx=10, pady=10)
entrada_cnpj_unidade_negocio = tk.Entry(root, width=50)
entrada_cnpj_unidade_negocio.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text="Nome da Unidade de Negócio:").grid(row=5, column=0, padx=10, pady=10)
entrada_nome_unidade_negocio = tk.Entry(root, width=50)
entrada_nome_unidade_negocio.grid(row=5, column=1, padx=10, pady=10)

tk.Button(root, text="Alterar Dados do XML", command=alterar_dados_e_salvar).grid(row=6, column=1, pady=20)

# Iniciar a Interface
root.mainloop()
