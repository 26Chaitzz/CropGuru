import joblib
from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')

@app.route('/form', methods=["POST"])
def brain():
    Nitrogen=float(request.form['Nitrogen'])
    Phosphorus=float(request.form['Phosphorus'])
    Potassium=float(request.form['Potassium'])
    Temperature=float(request.form['Temperature'])
    Humidity=float(request.form['Humidity'])
    Ph=float(request.form['ph'])
    Rainfall=float(request.form['Rainfall'])
     
    values=[Nitrogen,Phosphorus,Potassium,Temperature,Humidity,Ph,Rainfall]
    
    if Ph>0 and Ph<=14 and Temperature<100 and Humidity>0:
        joblib.load('crop_app','r')
        model = joblib.load(open('crop_app','rb'))
        arr = [values]
        acc = model.predict(arr)
        # print(acc)
        prediction = acc[0]
        return render_template('prediction.html', prediction=str(acc))
    else:
        return "Sorry...  Error in entered values in the form Please check the values and fill it again"

@app.route('/contact')
def contact_page():
    return render_template('Contact.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='Crop'
        )
        cursor = conn.cursor()
        
        # Insert data into database table
        cursor.execute("INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        return 'Form submitted successfully!'


if __name__ == '__main__':
    app.run(debug=True)

