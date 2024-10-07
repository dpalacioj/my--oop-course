import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key_openai = os.getenv("OPENAI_API_KEY")


openai.api_key = api_key_openai

# Instrucciones
system_rol = """Actúa como un experto en analizar sentimientos.
                El usuario te ingresará diferentes mensajes y vos analizas
                los sentimientos y darás una respuesta con al menos 1 carácter
                y máximo 4 caracteres.
                Es MUY IMPORTANTE que tengas en cuenta que solo quiero respuesta
                NUMÉRICAS, donde -1 es algo muy negativo, 0 es neutral y 1 es 
                muy positivo. También puedes responder rangos intermedios como
                0.7, 0.4, 0.1, etcétera. De acuerdo a lo que te ingrese el usuario.
                Recuerda que son válidos todos los rangos.
                (Solo puedes contestar con ints o floats)"""

# Rol que tendrá GPT
mensajes = [{"role": "system", "content": system_rol}]

class AnalizadorDeSentimientos:
    def analizar_sentimiento(self, polaridad):
        if polaridad > -0.8 and polaridad <= -0.3:
            return "\x1b[1;31m" + "Negativo" + "\x1b[1;37m" # Se agrega al final esta expresion apra que el texto siga siendo blanco
        elif polaridad > -0.3 and polaridad < -0.1:
            return "\x1b[1;31m" + "Algo Negativo" + "\x1b[1;37m"
        elif polaridad >= -0.1 and polaridad <= 0.1:
            return "\x1b[1;33m" + "Neutral" + "\x1b[1;37m"
        elif polaridad > 0.1 and polaridad <= 0.4:
            return "\x1b[1;32m" + "Algo positivo" + "\x1b[1;37m"
        elif polaridad >= 0.4 and polaridad <= 0.9:
            return "\x1b[1;32m" + "Positivo" + "\x1b[1;37m"
        elif polaridad > 0.9:
            return "\x1b[1;32m" + "Muy Positivo" + "\x1b[1;37m"
        else:
            return "\x1b[1;32m" + "MUY Negativo" + "\x1b[1;37m"
        
        
analizador = AnalizadorDeSentimientos()

while True:
    user_prompt = input("\x1b[1;37m" + "Escribe algo para luego yo analizar el texto: " + "\x1b[1;37m")
    mensajes.append({"role": "user", "content": user_prompt}) # Lista de mensajes para que gpt analice

    try:
        completion = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = mensajes,
            max_tokens = 8
        )

        # Verificar si hay respuesta en la estructura esperada
        respuesta = completion.choices[0].message.content

        # Convertir la respuesta a floar
        mensajes.append({"role": "assistant", "content": respuesta})

        # Análisis de sentimiento
        sentimiento = analizador.analizar_sentimiento(float(respuesta))
        print(sentimiento)

    except ValueError:
        print("\x1b[1;31m" + "Error: La respuesta no es un número válido." + "\x1b[1;37m")
    except Exception as e:
        print("\x1b[1;31m" + f"Error: {e}" + "\x1b[1;37m")
