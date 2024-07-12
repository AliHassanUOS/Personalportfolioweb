from flask import Flask, render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    project_description = db.Column(db.Text)

    def __repr__(self):
        return f"Project {self.id}"



@app.route("/",methods = ["POST","GET"])
def first_function():
    return render_template('home.html')

@app.route("/about")
def about_me():
    return render_template('about.html')





@app.route("/projects", methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']

        new_project = Project(project_name=project_name, project_description=project_description)
        db.session.add(new_project)
        db.session.commit()

        # Redirect to the same route to refresh the page with updated projects
        return redirect(url_for('projects'))

    projects = Project.query.all()
    return render_template('projects.html', projects=projects)





@app.route("/contact")
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    
    with app.app_context():
       db.create_all()


    app.run(host='0.0.0.0', debug=True)
