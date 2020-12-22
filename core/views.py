from flask import render_template, request,Blueprint
from myproject.models import Zajezd
core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    zajezdy = Zajezd.query.order_by(Zajezd.date.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',zajezdy=zajezdy)

@core.route('/info')
def info():
    return render_template('info.html')
