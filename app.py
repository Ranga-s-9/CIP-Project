from flask import Flask, render_template, request, jsonify
import pandas as pd
import webbrowser
import threading
import os
import time

app = Flask(__name__)

csv_file = os.path.join(os.path.dirname(__file__), 'sales_data.csv')

# Load DataFrame initially
def load_data():
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
        return pd.DataFrame(columns=['Date', 'Region', 'Product', 'Category', 'Sales', 'Profit', 'Quantity'])

df = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    global df
    filtered_df = df.copy()
    
    # Optional backend filtering (frontend can also handle it)
    region = request.args.get('region', 'All')
    product = request.args.get('product', 'All')
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if product != 'All':
        filtered_df = filtered_df[filtered_df['Product'] == product]
        
    records = filtered_df.to_dict(orient='records')
    # Add an index mapping for deletion purposes
    for i, record in enumerate(records):
        record['_id'] = i 
    return jsonify(records)

@app.route('/api/data', methods=['POST'])
def add_data():
    global df
    data = request.json
    try:
        new_row = {
            'Date': data.get('Date', ''),
            'Region': data.get('Region', ''),
            'Product': data.get('Product', ''),
            'Category': data.get('Category', 'Electronics'),
            'Sales': float(data.get('Sales', 0)),
            'Profit': float(data.get('Profit', 0)),
            'Quantity': int(data.get('Quantity', 0))
        }
        
        # Append to DataFrame
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        # Save to CSV
        df.to_csv(csv_file, index=False)
        
        return jsonify({"success": True, "record": new_row})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_data(record_id):
    global df
    try:
        if 0 <= record_id < len(df):
            df = df.drop(df.index[record_id]).reset_index(drop=True)
            df.to_csv(csv_file, index=False)
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Record not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

def open_browser():
    time.sleep(1.5)
    print("\n--- LAUNCHING SALES DASHBOARD IN BROWSER ---")
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(port=5000, debug=False)
