from flask import Flask,render_template,request,redirect,url_for,flash
import urllib.request, json
import connectdb


app = Flask(__name__)
app.secret_key = 'some secret key'

lista = []
frutas = []
registros = []
@app.route("/",methods=["GET","POST"])
def principal():
    if request.method == "POST":
        if request.form.get('cadastrofruta'):
            frutas.append(request.form.get("cadastrofruta"))
    return render_template("index.html",frutas=frutas)
    
@app.route("/sobre",methods=["GET","POST"])
def sobre():
    if request.method == "POST":
        if request.form.get("aluno") and request.form.get("nota"):
            registros.append({"aluno":request.form.get("aluno"),"nota":request.form.get("nota")})
    return render_template("sobre.html",registros=registros)

@app.route("/filmes/<slug>")
def filmes(slug):
    url = ''
    if slug == 'populares':
        url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=e0d3d39e900b733bba4661594c7cbd04'
    elif slug == 'kids':
        url = f'https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=e0d3d39e900b733bba4661594c7cbd04'
    elif slug == '2010':
        url = f'https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=e0d3d39e900b733bba4661594c7cbd04'
    elif slug == 'drama':
        url = f'https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=e0d3d39e900b733bba4661594c7cbd04'
    elif slug == 'tom-cruise':
        url = f'https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=e0d3d39e900b733bba4661594c7cbd04'
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    json_data = json.loads(dados)
    return render_template("filmes.html",filmes=json_data['results'])

@app.route("/cursos")
def lista_cursos():
    return render_template("cursos.html",cursos=connectdb.select())

@app.route("/novo_curso",methods=["GET","POST"])
def novo_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    carga_horaria = request.form.get('carga_horaria')
    if request.method == 'POST':
        if not nome or not descricao or not carga_horaria:
            flash("Preencha todos os campos do formulário","error")
        else:
            connectdb.insert(nome=nome,descricao=descricao,carga_horaria=carga_horaria)
            flash('Cadastrado com sucesso','info')
            return redirect(url_for('lista_cursos'))
    return render_template("novo_curso.html")

@app.route("/<id>/edita_curso",methods=['GET','POST'])
def edita_curso(id):
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        carga_horaria = request.form.get('carga_horaria')
        connectdb.edit(nome,descricao,carga_horaria,lista[0])
        flash('Editado com sucesso','info')
        return redirect(url_for('lista_cursos'))
    if len(lista) > 0:
        lista.clear()
    curso = connectdb.consulta_edit(id)
    lista.append(curso['id'])
    return render_template('edita_curso.html',curso=curso)


@app.route("/<id>/deletar", methods=['GET','POST'])
def deletar(id):
    connectdb.delete(id)
    flash('Excluído com sucesso','info')
    return redirect(url_for('lista_cursos')) 


if __name__ == "__main__":
    app.run(debug=True)