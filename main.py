from flask import Flask, render_template, request, redirect
from json import dump, load

app = Flask(__name__)

@app.route('/')
def index():
    with open ('posts.json') as file:
        dict_file = load(file)
    return render_template("index.html", posts=dict_file)

@app.route('/create_post', methods=["POST"])
def func():
    title = request.form.get('title')
    text = request.form.get('text')
    kartinka = request.files.get('kartinka')

    puti_kartinki = "static\\upload\\" + kartinka.filename

    kartinka.save(puti_kartinki)

    with open ('posts.json') as file:
        dict_file = load(file)
        new_post = {
            'text': text,
            'image': puti_kartinki
        }
        dict_file[title] = new_post
        with open ('posts.json', 'w', encoding='utf-8') as file_2:
            dump(dict_file, file_2)


    return redirect('/')

@app.route('/createPost')
def get_create_post_template():
    return render_template("createPost.html")

@app.route('/registration')
def get_registration_template():
    return render_template('registration.html')

@app.route("/redaktirovanie/<title>")
def get_redaktirovanie_template(title):
    with open ('posts.json') as file:
        dict_file = load(file)
        post = dict_file[title]
    return render_template("redaktirovanie.html", post=post, title=title)

@app.route("/redaktirovanie_post", methods=['POST'])
def save_redaktirovanie():
    title = request.form.get('title')
    text = request.form.get('text')
    kartinka = request.files.get('kartinka')

    puti_kartinki = "static\\upload\\" + kartinka.filename

    if kartinka:
        kartinka.save(puti_kartinki)

    with open ('posts.json') as file:
        dict_file = load(file)
        if kartinka:
            new_post = {
                'text': text,
                'image': puti_kartinki
            }
        else:
            new_post = {
                'text': text,
                'image': dict_file[title]["image"]
            }    
        dict_file[title] = new_post
        with open ('posts.json', 'w', encoding='utf-8') as file_2:
            dump(dict_file, file_2)


    return redirect('/') 

app.run(debug=True)