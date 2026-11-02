from app import app, db, appbuilder

with app.app_context():
    appbuilder.add_permissions()
    rol_public = appbuilder.sm.find_role("Public")
    
    if rol_public:
        # Intentar con los nombres comunes con los que FAB registra la función chat
        posibles_acciones = ["can_chat", "chat", "can_this_form_get", "can_this_form_post"]
        
        for accion in posibles_acciones:
            pview = appbuilder.sm.find_permission_view_menu(accion, "AsistenteView")
            if not pview:
                # Si no existe, forzamos su creación en el SecurityManager
                pview = appbuilder.sm.add_permission_view_menu(accion, "AsistenteView")
            
            if pview:
                appbuilder.sm.add_permission_role(rol_public, pview)
                print(f" Permiso vinculado: {accion} -> AsistenteView")

        db.session.commit()
        print("\n ¡Proceso completado con éxito!")