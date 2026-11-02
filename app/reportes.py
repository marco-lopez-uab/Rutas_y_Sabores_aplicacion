import io
from flask import Response, make_response
from flask_appbuilder import BaseView, expose, has_access
from sqlalchemy import func
from app import appbuilder, db
from .models import ReservaExcursion, Excursion, Ruta, Cliente, Guia, Refrigerio

# Librerías para exportar a PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReportesView(BaseView):
    default_view = 'reporte_rutas'

    # --- REPORTE 1: Reservas y Pasajeros por Ruta ---
    @expose('/rutas/')
    @has_access
    def reporte_rutas(self):
        resultados = db.session.query(
            Ruta.nombre.label('ruta_nombre'),
            Ruta.dificultad,
            func.count(ReservaExcursion.id).label('total_reservas'),
            func.coalesce(func.sum(ReservaExcursion.num_personas), 0).label('total_personas')
        ).join(Excursion, Ruta.id == Excursion.ruta_id)\
         .join(ReservaExcursion, Excursion.id == ReservaExcursion.excursion_id)\
         .group_by(Ruta.id).all()

        return self.render_template('reporte_reservas.html', resultados=resultados)

    # --- REPORTE 2: Top Excursiones más Solicitadas ---
    @expose('/top_excursiones/')
    @has_access
    def reporte_top_excursiones(self):
        resultados = db.session.query(
            Excursion.id.label('excursion_id'),
            Ruta.nombre.label('ruta_nombre'),
            Excursion.fecha_salida,
            func.coalesce(func.sum(ReservaExcursion.num_personas), 0).label('total_pasajeros')
        ).join(Ruta, Excursion.ruta_id == Ruta.id)\
         .join(ReservaExcursion, Excursion.id == ReservaExcursion.excursion_id)\
         .group_by(Excursion.id, Ruta.nombre)\
         .order_by(func.sum(ReservaExcursion.num_personas).desc())\
         .limit(5).all()

        return self.render_template('reporte_top.html', resultados=resultados)

    # --- REPORTE 3: Balance de Ingresos Totales ---
    @expose('/ingresos/')
    @has_access
    def reporte_ingresos(self):
        resultados = db.session.query(
            Excursion.id.label('excursion_id'),
            Ruta.nombre.label('ruta_nombre'),
            Excursion.precio,
            func.coalesce(func.sum(ReservaExcursion.num_personas), 0).label('total_pasajeros'),
            (func.coalesce(func.sum(ReservaExcursion.num_personas), 0) * Excursion.precio).label('total_ingresos')
        ).join(Ruta, Excursion.ruta_id == Ruta.id)\
         .join(ReservaExcursion, Excursion.id == ReservaExcursion.excursion_id)\
         .group_by(Excursion.id, Ruta.nombre, Excursion.precio).all()

        return self.render_template('reporte_ingresos.html', resultados=resultados)

    # --- DESCARGA / EXPORTACIÓN A PDF ---
    @expose('/ingresos/exportar_pdf')
    @has_access
    @expose('/ingresos/exportar_pdf')
    @has_access
    def exportar_ingresos_pdf(self):
        resultados = db.session.query(
            Ruta.nombre.label('ruta_nombre'),
            Excursion.precio,
            func.coalesce(func.sum(ReservaExcursion.num_personas), 0).label('total_pasajeros'),
            (func.coalesce(func.sum(ReservaExcursion.num_personas), 0) * Excursion.precio).label('total_ingresos')
        ).join(Ruta, Excursion.ruta_id == Ruta.id)\
         .join(ReservaExcursion, Excursion.id == ReservaExcursion.excursion_id)\
         .group_by(Excursion.id, Ruta.nombre, Excursion.precio).all()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("<b>Reporte de Ingresos - Rutas y Sabores</b>", styles['Title']))
        elements.append(Spacer(1, 12))

        data = [["Ruta", "Precio U.", "Pasajeros", "Total Generado (Bs.)"]]
        gran_total = 0

        for row in resultados:
            ingreso = row.total_ingresos or 0
            data.append([row.ruta_nombre, f"Bs. {row.precio:,.2f}", str(row.total_pasajeros), f"Bs. {ingreso:,.2f}"])
            gran_total += ingreso

        data.append(["TOTAL GENERAL", "", "", f"Bs. {gran_total:,.2f}"])

        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ECF0F1')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(t)
        doc.build(elements)

        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=Reporte_Ingresos_Rutas_Sabores.pdf'
        return response

# Integración al Menú de Flask-AppBuilder
appbuilder.add_view(
    ReportesView,
    "Reservas por Ruta",
    category="Reportes",
    icon="fa-map"
)
appbuilder.add_link(
    "Top Excursiones",
    href="/reportesview/top_excursiones/",
    category="Reportes",
    icon="fa-trophy"
)
appbuilder.add_link(
    "Balance de Ingresos",
    href="/reportesview/ingresos/",
    category="Reportes",
    icon="fa-money"
)