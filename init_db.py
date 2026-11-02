from app import app, db, appbuilder

with app.app_context():
    # 1. Crear las tablas en la base de datos
    db.create_all()
    
    # 2. Sincronizar y asignar permisos al rol 'User'
    rol_usuario = appbuilder.sm.find_role("User")
    if rol_usuario:
        # Permisos para el Asistente Virtual (IA)
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_chat", "AsistenteView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "menu_access", "Asistente Virtual")
        
        # Permisos para Catálogo y Rutas
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_list", "RutaView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_show", "RutaView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_list", "ExcursionView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_show", "ExcursionView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "menu_access", "Catálogo")
        appbuilder.sm.add_permission_to_role(rol_usuario, "menu_access", "Rutas")
        appbuilder.sm.add_permission_to_role(rol_usuario, "menu_access", "Excursiones")
        
        # Permisos para Reservas
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_list", "ReservaExcursionView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_show", "ReservaExcursionView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "can_add", "ReservaExcursionView")
        appbuilder.sm.add_permission_to_role(rol_usuario, "menu_access", "Operaciones")
        appbuilder.sm.add_permission_to_role(rol_usuario, "menu_access", "Reservas")

    print("BDD, tablas e inicialización de permisos completada.")