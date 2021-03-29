from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy    
from flask_migrate import Migrate 
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
app.config['UPLOAD_PATH']='static/uploads'
db=SQLAlchemy(app)
migrate = Migrate(app, db)


class Slides(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(120))
    text=db.Column(db.String(120))
    img=db.Column(db.String(120))
    read_more_url=db.Column(db.String(120))
    duration=db.Column(db.Integer)

class Services(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(120))
    text=db.Column(db.String(120))
    img=db.Column(db.String(120))
    contact_now_url=db.Column(db.String(120))

@app.route('/admin/service/new', methods=['GET' , 'POST'])
def add_service():
    if request.method=='POST':
        file=request.files['img']
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        service=Services(
            title=request.form['title'],
            text=request.form['text'],
            img=filename ,
            contact_now_url=request.form['contact_now_url']
        )
        db.session.add(service)
        db.session.commit()
        return redirect('/admin/service')
    return render_template('admin/add_service.html')   

@app.route('/admin/service')
def app_service():
    service=Services.query.all()
    return render_template('admin/services.html', service=service)

@app.route('/service')
def service():
    return render_template('app/service.html')

@app.route('/')
def index():
    slides=Slides.query.all()
    return render_template('app/index.html', slides=slides)


@app.route('/admin/')
def admin():
    return render_template('admin/index.html')

@app.route('/admin/slider')
def slider():
    slides=Slides.query.all()
    return render_template('admin/slider.html', slides=slides)

@app.route('/admin/slider/new', methods=['GET' , 'POST'])
def add_slide():
    if request.method=='POST':
        file=request.files['img']
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        slide=Slides(
            title=request.form['title'],
            text=request.form['text'],
            img=filename ,
            contact_now_url=request.form['contact_now_url']
        )
        db.session.add(slide)
        db.session.commit()
        return redirect('/admin/slider')
    return render_template('admin/add_slide.html')

@app.route('/admin/news')
def admin_news():
    return render_template('admin/news.html')

if __name__=='__main__':
    app.run(debug=True)

