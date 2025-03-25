from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def init_db():
    with sqlite3.connect('apidatabase.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     imagem_url TEXT NOT NULL
                     )""")
        print("Banco de dados criado com Sucesso!")


init_db()


@app.route('/')
def index():
    return render_template('index.html')  # 'Bem vindo(a) a Livros Vai na Web!'
    # return render_template


@app.route('/doar', methods=['POST'])
def doar():

    dados = request.get_json()

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    if not all([titulo, categoria, autor, imagem_url]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    with sqlite3.connect('apidatabase.db') as conn:
        conn.execute(""" INSERT INTO livros (titulo, categoria, autor, imagem_url)
                     VALUES(?,?,?,?)
                     """, (titulo, categoria, autor, imagem_url))

        conn.commit()

        return jsonify({"Mensagem": "Livro Cadastrado com Sucesso!"}), 201


@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('apidatabase.db') as conn:
        livros = conn.execute('SELECT * FROM livros').fetchall()

    livros_formatados = []

    for livro in livros:
        dicionario_livros = {
            'id': livro[0],
            'titulo': livro[1],
            'categoria': livro[2],
            'autor': livro[3],
            'imagem_url': livro[4]
        }
        livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados)


@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    # Conecta ao banco de dados e cria um cursor para executar comandos SQL.
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Executa a exclusão do livro com o ID especificado.
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        # Confirma a transação para salvar as mudanças.
        conn.commit()

    # Verifica se algum registro foi afetado (se o livro foi encontrado e excluído).
    if cursor.rowcount == 0:
        # Retorna um erro 400 (Bad Request) se o livro não foi encontrado.
        return jsonify({"erro": "Livro não encontrado"}), 400

    # Retorna uma mensagem de sucesso com o código 200 (OK).
    return jsonify({"menssagem": "Livro excluído com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)
