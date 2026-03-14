from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from flask_migrate import Migrate

# Importamos el Blueprint 
from pedidos.routes import pedidos_bp
from ventas.routes import ventas_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

db.init_app(app)
migrate = Migrate(app, db)

# Registramos el Blueprint en la aplicación principal
app.register_blueprint(pedidos_bp)
app.register_blueprint(ventas_bp, url_prefix='/ventas')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run()