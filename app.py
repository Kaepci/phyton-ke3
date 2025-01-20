import streamlit as st
import sqlite3
import pandas as pd

def init_db():
    # Initialize database connection and create tables if not exist
    conn = sqlite3.connect('dashboard.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        quantity INTEGER,
                        price REAL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS finance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT,
                        amount REAL,
                        type TEXT,  -- income or expense
                        date TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name TEXT,
                        item_id INTEGER,
                        quantity INTEGER,
                        total_price REAL,
                        date TEXT,
                        FOREIGN KEY (item_id) REFERENCES stock (id)
                    )''')
    conn.commit()
    conn.close()

def upload_csv_to_table(file, table_name):
    conn = sqlite3.connect('dashboard.db')
    cursor = conn.cursor()
    df = pd.read_csv(file)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

def show_stock():
    st.header("Stock Management")
    conn = sqlite3.connect('dashboard.db')
    cursor = conn.cursor()

    uploaded_file = st.file_uploader("Upload Stock CSV", type="csv")
    if uploaded_file:
        upload_csv_to_table(uploaded_file, 'stock')
        st.success("Stock data uploaded successfully!")

    with st.form("add_stock"):
        name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=0)
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Add Stock")
        if submitted:
            cursor.execute('INSERT INTO stock (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
            conn.commit()
            st.success("Stock added successfully!")

    cursor.execute('SELECT * FROM stock')
    items = cursor.fetchall()
    st.table(items)
    conn.close()

def show_finance():
    st.header("Finance Management")
    conn = sqlite3.connect('dashboard.db')
    cursor = conn.cursor()

    uploaded_file = st.file_uploader("Upload Finance CSV", type="csv")
    if uploaded_file:
        upload_csv_to_table(uploaded_file, 'finance')
        st.success("Finance data uploaded successfully!")

    with st.form("add_finance"):
        description = st.text_input("Description")
        amount = st.number_input("Amount", format="%.2f")
        type = st.selectbox("Type", ["Income", "Expense"])
        date = st.date_input("Date")
        submitted = st.form_submit_button("Add Record")
        if submitted:
            cursor.execute('INSERT INTO finance (description, amount, type, date) VALUES (?, ?, ?, ?)', (description, amount, type, date))
            conn.commit()
            st.success("Finance record added successfully!")

    cursor.execute('SELECT * FROM finance')
    records = cursor.fetchall()
    st.table(records)
    conn.close()

def show_sales():
    st.header("Sales Management")
    conn = sqlite3.connect('dashboard.db')
    cursor = conn.cursor()

    uploaded_file = st.file_uploader("Upload Sales CSV", type="csv")
    if uploaded_file:
        upload_csv_to_table(uploaded_file, 'sales')
        st.success("Sales data uploaded successfully!")

    with st.form("add_sale"):
        customer_name = st.text_input("Customer Name")
        item_id = st.number_input("Item ID", min_value=1)
        quantity = st.number_input("Quantity", min_value=1)
        date = st.date_input("Date")
        submitted = st.form_submit_button("Add Sale")
        if submitted:
            cursor.execute('SELECT price FROM stock WHERE id = ?', (item_id,))
            price = cursor.fetchone()
            if price:
                total_price = price[0] * quantity
                cursor.execute('INSERT INTO sales (customer_name, item_id, quantity, total_price, date) VALUES (?, ?, ?, ?, ?)', (customer_name, item_id, quantity, total_price, date))
                cursor.execute('UPDATE stock SET quantity = quantity - ? WHERE id = ?', (quantity, item_id))
                conn.commit()
                st.success("Sale recorded successfully!")
            else:
                st.error("Item not found")

    cursor.execute('SELECT * FROM sales')
    records = cursor.fetchall()
    st.table(records)
    conn.close()

def main():
    st.title("Business Dashboard")
    init_db()

    menu = ["Stock", "Finance", "Sales"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Stock":
        show_stock()
    elif choice == "Finance":
        show_finance()
    elif choice == "Sales":
        show_sales()

if __name__ == '__main__':
    main()
