from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input1 = db.Column(db.String(255), default='0')
    input2 = db.Column(db.String(255), default='0')
    input3 = db.Column(db.String(255), default='0')
    input4 = db.Column(db.String(255), default='0')
    input5 = db.Column(db.String(255), default='0')  # Rain condition
    input6 = db.Column(db.String(255), default='0')  # Current cases
    input7 = db.Column(db.String(255), default='0')  # Disease outbreak result

with app.app_context():
    db.drop_all()  # Drop existing tables
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def store():
    input1 = int(request.form['input1'])
    input2 = int(request.form['input2'])
    input3 = int(request.form['input3'])
    input4 = int(request.form['input4'])
    rain_condition = request.form['rain_condition']
    current_cases = int(request.form['current_cases'])
    prediction = predict_disease(rain_condition, current_cases)

    # Retrieve the existing data
    data = Data.query.first()

    if data is None:
        # If no data exists, create a new entry
        prediction = predict_disease(rain_condition, current_cases)
        new_data = Data(
            input1=str(input1),
            input2=str(input2),
            input3=str(input3),
            input4=str(input4),
            input7=prediction
        )
        db.session.add(new_data)
    else:
        # Update the existing data
        data.input1 = str(int(data.input1) + input1)
        data.input2 = str(int(data.input2) + input2)
        data.input3 = str(int(data.input3) + input3)
        data.input4 = str(int(data.input4) + input4)
        data.input7 = prediction

    db.session.commit()

    return redirect(url_for('index'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from the form
        rain_condition = request.form.get('rain_condition')
        current_cases = int(request.form.get('current_cases'))

        # Perform your prediction logic here
        prediction = predict_disease(rain_condition, current_cases)

        # Return the prediction as JSON
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)})

def predict_disease(rain_condition, current_cases):
    # Assign numerical values to rain conditions
    rain_values = {'Low': 1, 'Moderate': 2, 'High': 3}

    # Assign categories for disease cases
    disease_risk = {0: 'Low', 1: 'Moderate', 2: 'High'}

    # Calculate the average of rainfall and cases
    average_value = (rain_values[rain_condition] + determine_case_category(current_cases)) // 2

    # Use the average to determine disease risk category
    risk_category = disease_risk[average_value]

    return f'{risk_category}'

def determine_case_category(current_cases):
    if current_cases <= 1000:
        return 0  # Low
    elif 1001 <= current_cases <= 5000:
        return 1  # Moderate
    else:
        return 2  # High
    
    
if __name__ == '__main__':
    app.run(debug=True)
