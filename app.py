
from flask import Flask, request, render_template, redirect
import pandas as pd
import os

app = Flask(__name__)
DATA_FILE = 'customer_data.xlsx'

def censor(text):
    if len(text) <= 4:
        return '*' * len(text)
    return text[:2] + '*' * (len(text) - 4) + text[-2:]

@app.route('/', methods=['GET', 'POST'])
def form():
    message = ''
    censored = {}
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        job = request.form['job']
        id_card = request.form['id_card']

        if os.path.exists(DATA_FILE):
            df = pd.read_excel(DATA_FILE)
        else:
            df = pd.DataFrame(columns=['Name', 'Phone', 'Email', 'Address', 'Job', 'ID Card'])

        if id_card in df['ID Card'].values:
            message = 'Error: Identity Card Number already exists.'
        else:
            new_data = {
                'Name': name,
                'Phone': phone,
                'Email': email,
                'Address': address,
                'Job': job,
                'ID Card': id_card
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_excel(DATA_FILE, index=False)

            censored = {
                'name': censor(name),
                'phone': censor(phone),
                'email': censor(email),
                'address': censor(address),
                'job': censor(job),
                'id_card': censor(id_card)
            }
            message = 'Customer data submitted successfully.'

    return render_template('form.html', message=message, censored=censored)

if __name__ == '__main__':
    app.run(debug=True)
