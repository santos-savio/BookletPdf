import PyPDF2

def step1(input_pdf):
    # Abrir o arquivo PDF de entrada
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        paginas = len(reader.pages)  # Obter o número de páginas do PDF

        # Verificar se o número de páginas é múltiplo de 4
        if paginas % 4 != 0:
            paginas_completas = paginas + (4 - (paginas % 4))  # Adicionar páginas até ser múltiplo de 4
            print(f"Adicionando {paginas_completas - paginas} página(s) em branco.")
            print(f"Total de páginas: ", paginas_completas)
            paginas = paginas_completas

        # Lista de páginas
        lista = list(range(1, paginas + 1))
        nova_lista = step2(lista)
        reorganizar_pdf(input_pdf, "output.pdf", nova_lista)

def step2(lista):
    nova_lista = []

    while len(lista) >= 4:
        nova_lista.append(lista.pop())  # Adiciona o número da última página e remove da lista
        nova_lista.append(lista.pop(0))  # Adiciona o número da primeira página e remove da lista
        nova_lista.append(lista.pop(0))  # Adiciona o número da segunda página e remove da lista
        nova_lista.append(lista.pop())  # Adiciona o número da penúltima página e remove da lista

    print("Nova lista: ", nova_lista)
    if len(lista) != 0:
        print("Sobrou da lista inicial, os seguintes elementos:", lista)

    return nova_lista

def reorganizar_pdf(input_pdf, output_pdf, nova_ordem):
    # Abrir o arquivo PDF de entrada
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Reorganizar as páginas de acordo com a nova ordem
        for page_num in nova_ordem:
            writer.add_page(reader.pages[page_num - 1])

        # Escrever o novo PDF com as páginas reorganizadas
        with open(output_pdf, 'wb') as new_file:
            writer.write(new_file)

if __name__ == "__main__":
    input_pdf = "Código-civil.pdf"  # Substitua pelo caminho do seu arquivo PDF de entrada
    step1(input_pdf)