#Imports
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# My App
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#Data Class ~ Row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key = True);
    content = db.Column(db.String(100), nullable = False);
    complete = db.Column(db.Integer);
    created = db.Column(db.DateTime, default =datetime.utcnow);


    def __repr__(self) ->str:
            return f"Task {self.id}"


# Decorator route to index
#Home page
@app.route('/',methods = ["POST","GET"])
def index():
    #Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content = current_task)
        try:
             db.session.add(new_task)
             db.session.commit()
             return redirect('/')
        except Exception as e:
             print(f"ERROR: {e}")
             return f"ERROR:{e}"
    #See all current tasks
    else:
         tasks = MyTask.query.order_by(MyTask.created).all()
         return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id:int):
     delete_task = MyTask.query.get_or_404(id)
     try:
          db.session.delete(delete_task)
          db.session.commit()
          return redirect("/")
     except Exception as e:
          return f"ERROR: {e}"
     

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def edit(id:int):
    edit_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        edit_task.content = request.form['content']
        try:
             db.session.commit()
             return redirect("/")
        except Exception as e:
             return f"ERROR: {e}"
    else:
         return render_template('edit.html',task = edit_task)

#Run with debugger
if __name__ in "__main__":
    with app.app_context():
         db.create_all()

    app.run(debug = True)