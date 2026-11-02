from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder
from .models import Cliente, Guia, Ruta, Refrigerio, Excursion, ReservaExcursion

# Cliente
class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

# Guia
class GuiaView(ModelView):
    datamodel = SQLAInterface(Guia)

# Ruta
class RutaView(ModelView):
    datamodel = SQLAInterface(Ruta)

# Refrigerio
class RefrigerioView(ModelView):
    datamodel = SQLAInterface(Refrigerio)

# Excursion
class ExcursionView(ModelView):
    datamodel = SQLAInterface(Excursion)

# ReservaExcursion
class ReservaExcursionView(ModelView):
    datamodel = SQLAInterface(ReservaExcursion)

#menu

# Categoría: Gestión
appbuilder.add_view(ClienteView, "Clientes", icon="fa-user", category="Gestión")
appbuilder.add_view(GuiaView, "Guías", icon="fa-id-card", category="Gestión")

# Categoría: Catálogo
appbuilder.add_view(RutaView, "Rutas", icon="fa-map-signs", category="Catálogo")
appbuilder.add_view(RefrigerioView, "Refrigerios", icon="fa-coffee", category="Catálogo")

# Categoría: Operaciones
appbuilder.add_view(ExcursionView, "Excursiones", icon="fa-tree", category="Operaciones")
appbuilder.add_view(ReservaExcursionView, "Reservas", icon="fa-calendar-check-o", category="Operaciones")


#bloque IA
# from flask_appbuilder import BaseView, expose

# class AsistenteView(BaseView):
#     default_view = 'index'

#     @expose('/')
#     def index(self):
#         return self.render_template('index.html')

# appbuilder.add_view_no_menu(AsistenteView)
# appbuilder.add_link("Asistente Virtual", href="/api/asistente", icon="fa-comments", category="Operaciones")
from flask_appbuilder import BaseView, expose

class AsistenteView(BaseView):
    default_view = 'chat'

    @expose('/chat/')
    def chat(self):
        return self.render_template('chat.html')

appbuilder.add_view(
    AsistenteView,
    "Asistente Virtual",
    href="/asistenteview/chat/",
    icon="fa-comments",
)