from flask import Flask, render_template, request, send_file, jsonify
import PyPDF2
import io

app = Flask(__name__)


def _reorder_for_booklet(page_list):
    nova_lista = []
    while len(page_list) >= 4:
        nova_lista.append(page_list.pop())
        nova_lista.append(page_list.pop(0))
        nova_lista.append(page_list.pop(0))
        nova_lista.append(page_list.pop())
    return nova_lista


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/verificar', methods=['POST'])
def verificar():
    if 'pdf' not in request.files or request.files['pdf'].filename == '':
        return jsonify({'erro': 'Nenhum arquivo enviado.'}), 400

    file = request.files['pdf']
    try:
        reader = PyPDF2.PdfReader(file.stream)
        paginas = len(reader.pages)
    except Exception:
        return jsonify({'erro': 'Arquivo PDF inválido.'}), 400

    paginas_em_branco = (4 - paginas % 4) % 4
    return jsonify({
        'paginas': paginas,
        'paginas_em_branco': paginas_em_branco,
        'paginas_total': paginas + paginas_em_branco,
    })


@app.route('/processar', methods=['POST'])
def processar():
    if 'pdf' not in request.files or request.files['pdf'].filename == '':
        return jsonify({'erro': 'Nenhum arquivo enviado.'}), 400

    file = request.files['pdf']
    try:
        pdf_bytes = file.read()
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        paginas = len(reader.pages)
    except Exception:
        return jsonify({'erro': 'Arquivo PDF inválido.'}), 400

    paginas_em_branco = (4 - paginas % 4) % 4

    # None marks a blank page placeholder
    page_list = list(range(1, paginas + 1)) + [None] * paginas_em_branco
    nova_ordem = _reorder_for_booklet(page_list)

    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    writer = PyPDF2.PdfWriter()
    first = reader.pages[0]
    width = float(first.mediabox.width)
    height = float(first.mediabox.height)

    for page_num in nova_ordem:
        if page_num is None:
            writer.add_blank_page(width=width, height=height)
        else:
            writer.add_page(reader.pages[page_num - 1])

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    original = file.filename or 'documento.pdf'
    download_name = original.rsplit('.', 1)[0] + '-booklet.pdf'

    return send_file(
        output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=download_name,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5059, debug=False)
