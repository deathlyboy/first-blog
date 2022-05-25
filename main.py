from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlighter import SQlighter


app = Flask(__name__)
app.config['SECRET_KEY'] = '049ae2f115a91e8a8cf1a553157b13d99a0078e6'
db = SQlighter('пользователи.db')


def cut_title(i):
    if len(i) > 35:
        return i[:35] + '...'
    return i


def admin(email, password, state):
    if db.user_exists(email):
        if db.get_password(email) == password:
            print('успешно вошол')
            session['user'] = email
            if state:
                session.permanent = True
            flash('Вы успешно вошли в акаунт!', category='bg-success')
            return redirect('/')
        else:
            flash('неверный пароль')
            return redirect('admin')
    else:
        flash('пользователя не существует')
        return redirect('admin')


def simg(text):
    links = []
    flag = 0
    while flag != -1:
       flag = text.find('{{')
       p = text.find('}}')
       links.append(text[flag:p+2])
       text = text[p+2:]

    return links


@app.route('/')
def hello_world():
    return render_template('main.html', home='text-secondary', preview=db.all_title_and_preview())


@app.route('/admin', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        return admin(data['email'], data['password'],request.form.get('check'))

    return render_template('sign_up.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html', about='text-secondary')


@app.route('/faq')
def faq():
    return render_template('faq.html', faq='text-secondary')


@app.route('/add')
def add():
    if 'user' not in session:
        flash('Вы не являетесь админом')
    return render_template('add.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'user' not in session:
        return redirect('/add')
    if request.method == 'POST':
        data = request.form

        if db.title_exists(data['title']):
            flash('Заголовок уже существует')
        else:
            db.write_data(data['title'], data['text'], '#lol', request.files['preview'].filename)

            if len(request.files.getlist('files')) > 1:
                print(list(request.files['preview']))
                for i in request.files.getlist('files'):
                    print(i)
                    with open(f'static/images/{i.filename}', 'wb+') as f:
                        f.write(i.read())

            with open(f'static/images/{request.files["preview"].filename}', 'wb+') as f:
                f.write(request.files['preview'].read())

    return redirect('/add')


@app.route('/rewrite', methods=['POST', 'GET'])
def rewrite():
    data = request.form
    if 'user' not in session:
        return redirect(f'/p/{data["title"]}')

    if request.method == 'POST':
        db.delete_post(data['title'])
        db.write_data(data['title'], data['text'], '#lol', request.files['preview'].filename)
        if len(request.files.getlist('files')) > 1:
            for i in request.files.getlist('files'):
                with open(f'static/images/{i.filename}', 'wb+') as f:
                    f.write(i.read())

        with open(f'static/images/{request.files["preview"].filename}', 'wb+') as f:
            f.write(request.files['preview'].read())

    return redirect(f'/p/{data["title"]}')


@app.route('/p/<title>')
def p(title):
    text = db.text(title)
    for i in simg(text)[:-1]:
        print(i)
        text = text.replace(i, f'<img src="/static/images/{i[2:-2]}" alt="упсс.." class="img">')
        print(text)
    return render_template('p.html', title=title, text=text, hidden='d-none' if 'user' not in session else None)


@app.route('/p/<title>/edit')
def edit(title):
    if 'user' not in session:
        flash('Вы не являетесь админом')
    print((title))
    return render_template('add.html', title=title, text=db.text(title), upload='rewrite')


@app.route('/p/<title>/delete')
def delete(title):
    db.delete_post(title)
    return redirect('/')


if __name__ == '__main__':
    app.jinja_env.globals.update(cut_title=cut_title)
    app.run()
