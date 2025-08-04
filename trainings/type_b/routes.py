from flask import Blueprint, render_template

type_b_bp = Blueprint('type_b', __name__, url_prefix='/type-b')

@type_b_bp.route('/')
def form():
    return render_template('coming_soon.html', training_type='Type B', training_name='Technical Workshop')

@type_b_bp.route('/generate', methods=['POST'])
def generate_report():
    return "Type B report generation coming soon!"
