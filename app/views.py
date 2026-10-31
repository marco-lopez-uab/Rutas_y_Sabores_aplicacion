from flask_appbuilder import ModelView, IndexView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder, db
from .models import Cliente, Guia, Ruta, Refrigerio, Excursion, ReservaExcursion

# Vistas de la aplicación (se configurarán progresivamente)