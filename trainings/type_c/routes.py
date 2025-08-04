from flask import Blueprint, render_template

type_c_bp = Blueprint('type_c', __name__, url_prefix='/type-c')

@type_c_bp.route('/')
def form():
    return render_template('coming_soon.html', training_type='Type C', training_name='Professional Development')

@type_c_bp.route('/generate', methods=['POST'])
def generate_report():
    return "Type C report generation coming soon!"
