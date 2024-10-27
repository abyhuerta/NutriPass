from flask import Blueprint, jsonify, request
from .item_search import web_scrape
from flask_cors import CORS  # Import CORS


scrape_walmart = Blueprint('scrape_walmart', __name__)

@scrape_walmart.route('/scrape', methods=['GET'])
def scrape():
    search_item = request.args.get('query', '', type=str)
    if not search_item.strip():
        return jsonify({"error": "search_item parameter is required"}), 400
    
    try:
        results = web_scrape(search_item)
        if results is None:
            raise ValueError("No results returned from web_scrape.")
        return jsonify(results)
    except Exception as e:
        print(f"Error during scraping: {e}")  # Print detailed error for debugging
        return jsonify({"error": str(e)}), 500
