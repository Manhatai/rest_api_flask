from flask import send_from_directory, Blueprint


web_bp = Blueprint("web_handling", __name__)

@web_bp.route('/web/<path:filename>', methods=['GET'])
def send_report(filename):
    return send_from_directory('web', filename)