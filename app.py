from flask import Flask, render_template, request, session, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

csrf = CSRFProtect()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
csrf.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todolist(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Todolist %r>' % f"{self.sno} - {self.title} - {self.description}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        todo = Todolist(title=title, description=description)

        try:
            db.session.add(todo)
            db.session.commit()
            flash('You have successfully added the ToDo')
            return redirect(url_for('index'))
        except:
            flash('There was a problem adding new ToDo.')
            return redirect(url_for('index'))

    else:
        todolist = Todolist.query.all()
        return render_template('index.html', allToDoList=todolist)

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        sno = int(request.form['todo_update'])
        get_todo = Todolist.query.get(sno)

        return render_template('update.html',updateToDo=get_todo)
    else:
        return redirect(url_for('index'))

@app.route('/update_submit', methods=['GET','POST'])
def update_submit():
    if request.method == 'POST':
        sno = int(request.form['update_sno'])
        todo = Todolist.query.get(sno)

        todo.title = request.form['update_title']
        todo.description = request.form['update_description']

        try:
            db.session.add(todo)
            db.session.commit()
            flash('You have successfully updated the ToDo')
            return redirect(url_for('index'))
        except:
            flash('There was a problem updating the ToDo.')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        sno = int(request.form['todo_delete'])
        get_todo = Todolist.query.get(sno)
    
        try:
            db.session.delete(get_todo)
            db.session.commit()
            flash('You have successfully deleted the ToDo')

            return redirect(url_for('index'))

        except:
            flash('There was a problem deleting the ToDo.')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
