from flask import Blueprint, render_template

type_d_bp = Blueprint('type_d', __name__, url_prefix='/type-d')

@type_d_bp.route('/')
def form():
    return render_template('coming_soon.html', training_type='Type D', training_name='Custom Training')

@type_d_bp.route('/generate', methods=['POST'])
def generate_report():
    return "Type D report generation coming soon!"
