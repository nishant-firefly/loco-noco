# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



# from app.query_builder import QueryBuilder

# def main():
#     query_builder = QueryBuilder()
#     persona = input("Enter persona (admin/user/guest): ").strip()
#     operation = input("Enter operation (select/insert/update/delete): ").strip()
#     table = input("Enter table name: ").strip()
#     query_input = {
#         "operation": operation,
#         "table": table,
#     }

#     if operation == "select":
#         query_input["columns"] = input("Enter columns (comma-separated): ").strip().split(",")
#         query_input["clause"] = eval(input("Enter WHERE clause as dict: "))
#     elif operation in ["insert", "update"]:
#         query_input["values"] = eval(input("Enter values as dict: "))
#         if operation == "update":
#             query_input["clause"] = eval(input("Enter WHERE clause as dict: "))
#     elif operation == "delete":
#         query_input["clause"] = eval(input("Enter WHERE clause as dict: "))

#     query = query_builder.build_query(query_input, persona)
#     print("Generated SQL Query:")
#     print(query)

# if __name__ == "__main__":
#     main()
from query_builder import QueryBuilder

def main():
    # Example usage
    query_builder = QueryBuilder()

    request = {
        "operation": "select",
        "table": "product",
        "columns": ["id", "name", "price"],
        "clause": {
        "price": {"operator": ">", "value": 100},
        "category_id": {"operator": "IN", "value": [1, 2, 3]}
    },
    "joins": [
        {"type": "INNER", "table": "category", "on": "product.category_id = category.id"}
    ],
    "limit": 10,
    "offset": 5
    }

    persona = "user"

    try:
        query_builder = QueryBuilder()
        generated_query = query_builder.build_query(request, persona)
        print("Generated Query:", generated_query)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
