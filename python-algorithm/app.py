#!/usr/bin/env python3
"""
Main Flask application for the recommendation algorithm API.
"""
from flask import Flask, jsonify, request
import json
import os

from recommendation.algorithm import generate_recommendations
from recommendation.models import UserHistory, ProductCategory, BusinessRule

app = Flask(__name__)

# Load sample data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Create data files if they don't exist
if not os.path.exists(os.path.join(DATA_DIR, "user_history.json")):
    with open(os.path.join(DATA_DIR, "user_history.json"), "w") as f:
        json.dump({
            "users": {
                "user1": {
                    "viewed_products": ["product1", "product2", "product5"],
                    "purchased_products": ["product3"]
                },
                "user2": {
                    "viewed_products": ["product2", "product4", "product7"],
                    "purchased_products": ["product2", "product7"]
                }
            }
        }, f, indent=2)

if not os.path.exists(os.path.join(DATA_DIR, "product_categories.json")):
    with open(os.path.join(DATA_DIR, "product_categories.json"), "w") as f:
        json.dump({
            "categories": {
                "electronics": ["product1", "product3", "product8"],
                "clothing": ["product2", "product5", "product7"],
                "home": ["product4", "product6"]
            },
            "relationships": {
                "electronics": ["home"],
                "clothing": ["home"],
                "home": ["electronics", "clothing"]
            }
        }, f, indent=2)

if not os.path.exists(os.path.join(DATA_DIR, "business_rules.json")):
    with open(os.path.join(DATA_DIR, "business_rules.json"), "w") as f:
        json.dump({
            "rules": [
                {"type": "boost", "category": "electronics", "factor": 1.2},
                {"type": "filter", "min_relevance": 0.3},
                {"type": "max_items_per_category", "count": 3}
            ]
        }, f, indent=2)


# API endpoints
@app.route('/api/user/<user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Retrieve browsing history for a specific user"""
    try:
        with open(os.path.join(DATA_DIR, "user_history.json"), "r") as f:
            data = json.load(f)
        
        if user_id not in data["users"]:
            return jsonify({"error": f"User {user_id} not found"}), 404
        
        return jsonify(data["users"][user_id])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Retrieve product categories and their relationships"""
    try:
        with open(os.path.join(DATA_DIR, "product_categories.json"), "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/business-rules', methods=['GET'])
def get_business_rules():
    """Retrieve business rules for recommendations"""
    try:
        with open(os.path.join(DATA_DIR, "business_rules.json"), "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Generate recommendations for a specific user"""
    try:
        # Load user history
        with open(os.path.join(DATA_DIR, "user_history.json"), "r") as f:
            history_data = json.load(f)
        
        if user_id not in history_data["users"]:
            return jsonify({"error": f"User {user_id} not found"}), 404
        
        user_history = UserHistory(
            user_id=user_id,
            viewed_products=history_data["users"][user_id]["viewed_products"],
            purchased_products=history_data["users"][user_id]["purchased_products"]
        )
        
        # Load product categories
        with open(os.path.join(DATA_DIR, "product_categories.json"), "r") as f:
            categories_data = json.load(f)
        
        product_categories = []
        for category, products in categories_data["categories"].items():
            related_categories = categories_data["relationships"].get(category, [])
            product_categories.append(
                ProductCategory(
                    name=category,
                    products=products,
                    related_categories=related_categories
                )
            )
        
        # Load business rules
        with open(os.path.join(DATA_DIR, "business_rules.json"), "r") as f:
            rules_data = json.load(f)
        
        business_rules = [BusinessRule(**rule) for rule in rules_data["rules"]]
        
        # Get limit parameter with default of 5
        limit = request.args.get('limit', default=5, type=int)
        
        # Generate recommendations
        recommendations = generate_recommendations(
            user_history=user_history,
            product_categories=product_categories,
            business_rules=business_rules,
            limit=limit
        )
        
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

