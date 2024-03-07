from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dummy data (replace with your actual data)
projects = [
    {"id": 1, "name": "Project A", "description": "Description of Project A", "category": "Environment", "county": "Nairobi"},
    {"id": 2, "name": "Project B", "description": "Description of Project B", "category": "Health", "county": "Mombasa"},
    # Add more projects as needed
]

@app.route('/')
def index():
    return render_template('catalog.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('searchInput')
    category_filter = request.form.get('categoryFilter')
    county_filter = request.form.get('countyFilter')

    # Perform search logic based on the query, category, and county filters
    filtered_projects = filter_projects(search_query, category_filter, county_filter)

    # Return the filtered results as JSON
    return jsonify(filtered_projects)

def filter_projects(query, category, county):
    # Perform filtering based on query, category, and county
    results = [project for project in projects if
               (not query or query.lower() in project['name'].lower()) and
               (not category or category.lower() == project['category'].lower()) and
               (not county or county.lower() == project['county'].lower())]

    return results

if __name__ == '__main__':
    app.run(debug=True)
