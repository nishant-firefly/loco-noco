from flask import Flask, request, jsonify, render_template
from app.query_builder import QueryBuilder
from app.database import Database

# Initialize the Database object
db = Database()

# Example query
query = "SELECT * FROM product WHERE price > :price_limit"
params = {"price_limit": 100}
results = db.execute_query(query, params)

print("Query Results:", results)


app = Flask(__name__)
query_builder = QueryBuilder()
database = Database()


@app.route("/")
def home():
    return render_template("query_builder.html")


@app.route("/query", methods=["POST"])
def query_endpoint():
    data = request.json
    persona = data.get("persona", "guest")
    try:
        sql_query = query_builder.build_query(data.get("request"), persona)
        result = database.execute_query(sql_query)
        return jsonify({"query": sql_query, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/query-preview", methods=["POST"])
def query_preview():
    data = request.json
    persona = data.get("persona", "guest")
    try:
        sql_query = query_builder.build_query(data.get("request"), persona)
        return jsonify({"query": sql_query})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
