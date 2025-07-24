
import streamlit as st
import pandas as pd
import os

DATA_FILE = "customer_data.xlsx"

def censor(text):
    if not text:
        return ""
    return text[:2] + "*" * (len(text) - 4) + text[-2:]

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Phone", "Email", "Address", "Job", "ID Card Number"])

def save_data(data):
    data.to_excel(DATA_FILE, index=False)

st.title("Customer Input Form")

with st.form("customer_form"):
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    address = st.text_input("Address")
    job = st.text_input("Job")
    id_card = st.text_input("Identity Card Number")

    submitted = st.form_submit_button("Submit")

    if submitted:
        data = load_data()
        if id_card in data["ID Card Number"].values:
            st.error("This Identity Card Number has already been submitted.")
        else:
            new_entry = {
                "Name": name,
                "Phone": phone,
                "Email": email,
                "Address": address,
                "Job": job,
                "ID Card Number": id_card
            }
            data = data.append(new_entry, ignore_index=True)
            save_data(data)
            st.success("Customer data submitted successfully:")
            st.write("Name:", censor(name))
            st.write("Phone:", censor(phone))
            st.write("Email:", censor(email))
            st.write("Address:", censor(address))
            st.write("Job:", censor(job))
            st.write("ID Card Number:", censor(id_card))
