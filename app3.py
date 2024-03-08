# app2.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input1 = db.Column(db.String(255), nullable=False)
    input2 = db.Column(db.String(255), nullable=False)
    input3 = db.Column(db.String(255), nullable=False)
    input4 = db.Column(db.String(255), nullable=False)
    input5 = db.Column(db.String(255), default='0')
    input6 = db.Column(db.String(255), default='0')
    input7 = db.Column(db.String(255), default='0')  # Disease outbreak result

with app.app_context():
    db.drop_all()  # Drop existing tables
    db.create_all()  # Recreate tables

@app.route('/')
def display_data():
    data_list = Data.query.all()
    return render_template('hospital.html', data_list=data_list)  # Update template name to 'hospital.html'

if __name__ == '__main__':
    app.run(debug=True, port=5010)
