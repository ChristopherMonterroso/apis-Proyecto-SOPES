#routes
from flask import Blueprint, request, jsonify
import asyncio
from scraping import get_social_media_links
from flask_cors import CORS
api_blueprint = Blueprint('api', __name__)
CORS(api_blueprint, resources={r"/*": {"origins": "*"}})
@api_blueprint.route('/domain-social-info', methods=['POST'])
def get_social_media():
    print("Iniciando Playwright")
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "Debes proporcionar la URL del sitio web"}), 400
        try:
            social_media_links =  get_social_media_links(url)
            return jsonify({"social_media_links": social_media_links})
        except Exception as e:
            return jsonify({"error": str(e)}), 500