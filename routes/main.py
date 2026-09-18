import io
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from extensions import db
from models.models import Constancia, EquipoItem
from xhtml2pdf import pisa

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Obtener historial de constancias recientes
    constancias = Constancia.query.order_by(Constancia.created_at.desc()).all()
    return render_template('index.html', constancias=constancias)

@main_bp.route('/guardar', methods=['POST'])
def guardar_constancia():
    try:
        # Recuperar campos del formulario
        nombre = request.form.get('nombre')
        area = request.form.get('area')
        puesto = request.form.get('puesto')
        fecha = request.form.get('fecha')
        plaza = request.form.get('plaza')

        gerencia = request.form.get('gerencia', 'Gerencia IT')
        sitio = request.form.get('sitio')
        tecnico = request.form.get('tecnico')
        asunto = request.form.get('asunto', 'Entrega de equipo')
        licencia = request.form.get('licencia', 'Básica')

        nombre_entrega = request.form.get('nombre_entrega')
        firma_base64 = request.form.get('firma_base64')

        # Crear objeto Constancia
        nueva_constancia = Constancia(
            nombre=nombre,
            area=area,
            puesto=puesto,
            fecha=fecha,
            plaza=plaza,
            gerencia=gerencia,
            sitio=sitio,
            tecnico=tecnico,
            asunto=asunto,
            licencia=licencia,
            nombre_entrega=nombre_entrega,
            firma_base64=firma_base64
        )

        db.session.add(nueva_constancia)
        db.session.flush() # Obtiene el ID generado

        # Guardar lista de equipos agregados dinámicamente
        equipos_list = request.form.getlist('equipo[]')
        marcas_list = request.form.getlist('marca[]')
        modelos_list = request.form.getlist('modelo[]')
        series_list = request.form.getlist('serie[]')
        estados_list = request.form.getlist('estado[]')

        for i in range(len(equipos_list)):
            if equipos_list[i].strip():
                item = EquipoItem(
                    constancia_id=nueva_constancia.id,
                    equipo=equipos_list[i],
                    marca=marcas_list[i],
                    modelo=modelos_list[i],
                    serie=series_list[i],
                    estado=estados_list[i]
                )
                db.session.add(item)

        db.session.commit()
        return redirect(url_for('main.generar_pdf', constancia_id=nueva_constancia.id))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar la constancia: {str(e)}', 'danger')
        return redirect(url_for('main.index'))

@main_bp.route('/pdf/<int:constancia_id>')
def generar_pdf(constancia_id):
    constancia = Constancia.query.get_or_404(constancia_id)
    
    # Renderizar la plantilla HTML destinada al PDF
    html_rendered = render_template('constancia_pdf.html', c=constancia)
    
    # Convertir HTML a PDF
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_rendered), dest=pdf_buffer)

    if pisa_status.err:
        return f"Error al generar PDF: {pisa_status.err}", 500

    pdf_buffer.seek(0)
    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=constancia_{constancia.id}.pdf'
    return response 