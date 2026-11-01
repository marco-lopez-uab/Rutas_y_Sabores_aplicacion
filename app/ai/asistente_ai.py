import os
import logging
from flask import Blueprint, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

logger = logging.getLogger(__name__)

asistente_bp = Blueprint(
    "asistente_ai",
    __name__,
    url_prefix="/api"
)

@asistente_bp.route("/asistente", methods=["GET", "POST"])
def consultar_asistente():
    if request.method == "GET":
        return jsonify({
            "estado": "Servicio Activo",
            "mensaje": "El Asistente Virtual de Rutas y Sabores está funcionando correctamente."
        }), 200

    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({"error": "Se esperaba una solicitud JSON válida."}), 400

        mensaje = data.get("mensaje", "").strip()
        historial = data.get("history", [])

        if not mensaje:
            return jsonify({"error": "Debes escribir un mensaje."}), 400

        if not isinstance(historial, list):
            return jsonify({"error": "El historial debe ser una lista."}), 400

        mensajes = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente virtual de inteligencia artificial para la plataforma "
                    "'Rutas y Sabores'. Estás especializado en brindar información, recomendaciones "
                    "y orientación sobre rutas turísticas, excursiones, actividades al aire libre y "
                    "refrigerios o gastronomía local. Responde en español, de forma clara, amable "
                    "y estructurada."
                )
            }
        ]

        for item in historial[-20:]:
            if not isinstance(item, dict):
                continue
            rol = item.get("role")
            contenido = item.get("content")
            if rol in ("user", "assistant") and isinstance(contenido, str) and contenido.strip():
                mensajes.append({"role": rol, "content": contenido.strip()})

        mensajes.append({"role": "user", "content": mensaje})

        api_key = os.getenv("AI_API_KEY")
        modelo = os.getenv("AI_MODEL") or "qwen/qwen3.8-27b"

        if not api_key:
            return jsonify({"error": "No se ha configurado la clave AI_API_KEY en el archivo .env."}), 500

        # Crear cliente nativo de Groq
        cliente = Groq(api_key=api_key)

        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=mensajes,
            temperature=0.7
        )

        contenido = respuesta.choices[0].message.content

        if not contenido:
            contenido = "No se recibió una respuesta de la IA."

        return jsonify({"respuesta": contenido}), 200

    except Exception:
        logger.exception("Error al consultar el asistente de IA.")
        return jsonify({
            "error": "No se pudo obtener una respuesta. Verifica la configuración de la API e inténtalo nuevamente."
        }), 500
# import os
# import logging
# from flask import Blueprint, request, jsonify
# from openai import OpenAI
# from dotenv import load_dotenv

# # cargar variable .env
# load_dotenv()

# logger = logging.getLogger(__name__)

# asistente_bp = Blueprint(
#     "asistente_ai",
#     __name__,
#     url_prefix="/api"
# )


# def obtener_cliente():
#     """Crea el cliente de conexión con la API de IA."""
#     api_key = os.getenv("AI_API_KEY")
#     #base_url = os.getenv("AI_URL")
#     base_url = os.getenv("AI_URL") or "https://api.groq.com/openai/v1"

#     if not api_key:
#         raise RuntimeError("No se configuró AI_API_KEY.")

#     if not base_url:
#         raise RuntimeError("No se configuró AI_URL.")

#     return OpenAI(
#         api_key=api_key,
#         base_url=base_url
#     )


# @asistente_bp.route("/asistente", methods=["GET", "POST"])
# def consultar_asistente():
#     # Si la petición viene directamente desde el navegador (clic en el menú)
#     if request.method == "GET":
#         return jsonify({
#             "estado": "Servicio Activo",
#             "mensaje": "El Asistente Virtual de Rutas y Sabores está funcionando correctamente.",
#             "instrucciones": "Envía una solicitud POST en JSON con el parámetro 'mensaje' para realizar una consulta."
#         }), 200

#     # Petición POST con datos JSON
#     try:
#         data = request.get_json(silent=True)

#         if not isinstance(data, dict):
#             return jsonify({
#                 "error": "Se esperaba una solicitud JSON válida."
#             }), 400

#         mensaje = data.get("mensaje", "").strip()
#         historial = data.get("history", [])

#         if not mensaje:
#             return jsonify({
#                 "error": "Debes escribir un mensaje."
#             }), 400

#         if not isinstance(historial, list):
#             return jsonify({
#                 "error": "El historial debe ser una lista."
#             }), 400

#         mensajes = [
#             {
#                 "role": "system",
#                 "content": (
#                     "Eres un asistente virtual de inteligencia artificial para la plataforma "
#                     "'Rutas y Sabores'. Estás especializado en brindar información, recomendaciones "
#                     "y orientación sobre rutas turísticas, excursiones, actividades al aire libre y "
#                     "refrigerios o gastronomía local. Responde en español, de forma clara, amable "
#                     "y estructurada."
#                 )
#             }
#         ]

#         for item in historial[-20:]:
#             if not isinstance(item, dict):
#                 continue

#             rol = item.get("role")
#             contenido = item.get("content")

#             if (
#                 rol in ("user", "assistant")
#                 and isinstance(contenido, str)
#                 and contenido.strip()
#             ):
#                 mensajes.append({
#                     "role": rol,
#                     "content": contenido.strip()
#                 })

#         mensajes.append({
#             "role": "user",
#             "content": mensaje
#         })

#         cliente = obtener_cliente()

#         respuesta = cliente.chat.completions.create(
#             model=os.getenv("AI_MODEL", "llama-3.1-8b-instant"),
#             messages=mensajes,
#             temperature=0.7
#         )

#         contenido = respuesta.choices[0].message.content

#         if not contenido:
#             contenido = "No se recibió una respuesta de la IA."

#         return jsonify({
#             "respuesta": contenido
#         }), 200

#     except Exception:
#         logger.exception("Error al consultar el asistente de IA.")
#         return jsonify({
#             "error": (
#                 "No se pudo obtener una respuesta. "
#                 "Verifica la configuración de la API e inténtalo nuevamente."
#             )
#         }), 500
