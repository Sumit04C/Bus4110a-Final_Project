#index.html and results.html are copy pasted from the sample project

from flask import Flask, render_template, request
import pandas as pd
#flask is a Python framework used for building web apps

app = Flask(__name__)
data = pd.read_csv('data/TableauSalesData.csv')
data.info()
#converting the Order Date to datetime and extracting the year
data['Order Date'] = pd.to_datetime(data['Order Date'])
data['Year'] = data['Order Date'].dt.year

@app.route('/')
def index():
    # Get unique values for dropdowns
    categories = data['Category'].unique()
    subcategories = data['Sub-Category'].unique()
    regions = data['Region'].unique()
    segments = data['Segment'].unique()
    queries = ['Total Sales', 'Average Sales', 'Top 5 Products by Sales']  # Example queries
    return render_template('index.html', categories=categories, subcategories=subcategories, regions=regions, segments=segments, queries=queries)

@app.route('/results', methods=['POST'])
def results():
    # Get form data
    category = request.form['category']
    subcategory = request.form['subcategory']
    region = request.form['region']
    segment = request.form['segment']
    query = request.form['query']

    # Filter data
    filtered_data = data[
        (data['Category'] == category) &
        (data['Sub-Category'] == subcategory) &
        (data['Region'] == region) &
        (data['Segment'] == segment)
    ]

    # Perform the query
    if query == 'Total Sales':
        result = filtered_data['Sales'].sum()
    elif query == 'Average Sales':
        result = filtered_data['Sales'].mean()
    elif query == 'Top 5 Products by Sales':
        result = filtered_data.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)

    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

