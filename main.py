import os
import glob
import time
import wave
import pyaudio
import whisper
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI

##### ACCEDE A FFMPEG ######
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# Cargar variables del archivo .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No se encontró OPENAI_API_KEY en el archivo .env")

# CLIENTE OPEN AI
client = OpenAI(api_key=api_key)

# HISTORIAL DE CONVERSACION
chat_history = [
    {
        "role": "system",
        "content": "Sos un asistente conversacional en español llamado Verónica. Respondés de forma clara, natural, breve y amable. Cuando sea apropiado, podés referirte a vos misma como Verónica."
    }
]

# CARGAMOS WHISHPERO UNA SOLA VEZ --> MODELO QUE PASA DE AUDIO A TEXTO
stt_model = whisper.load_model("base") # --> HAY VARIOS MODELOS "base" ES EL MAS LIVIANO

# PARAMETROS GLOBALES DE AUDIO
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DURACION = 7
ARCHIVO_WAV = "grabacion.wav"
ARCHIVO_MP3 = "respuesta.mp3"

# GRABAMOS EL AUDIO 
def grabar_audio():
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Preparate para grabar tu consulta de 7 segundos")
    time.sleep(0.5)
    print("Grabando...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * DURACION)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Grabación terminada")

    stream.stop_stream()
    stream.close()

    sample_width = audio.get_sample_size(FORMAT)
    audio.terminate()

    with wave.open(ARCHIVO_WAV, "wb") as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(RATE)
        wave_file.writeframes(b"".join(frames))

#TRANSCRIBIMOS DE AUDIO A TEXTO
def transcribir_audio():
    print("Procesando grabación...")
    result = stt_model.transcribe(ARCHIVO_WAV, fp16=False)
    texto = result["text"].strip()
    return texto

# PREGUNTAMOS AL MODELO DE IA
def preguntar_modelo(texto_usuario):
    chat_history.append({"role": "user", "content": texto_usuario})

    # SETEAMOS LOS PAREMATROS DEL MODELO 
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history,
        max_tokens=150,
        temperature=0.5
    )

    texto_respuesta = response.choices[0].message.content.strip()

    chat_history.append({"role": "assistant", "content": texto_respuesta})

    return texto_respuesta

# VERONICA VA HABLAR USANDO EL REPRODUCTOR DE AUDIO DE LA COMPUTADORA

def hablar(texto):
    limpiar_mp3()
    nombre_archivo = f"respuesta_{int(time.time())}.mp3"
    tts = gTTS(texto, lang="es", slow=False)
    tts.save(nombre_archivo)
    os.system(f'start "" "{nombre_archivo}"')


# BORRA LOS AUDIOS DE LAS CONVERSACIONES VIEJAS 

def limpiar_mp3():
    archivos = glob.glob("respuesta_*.mp3")
    for archivo in archivos[:-5]:  # deja los últimos 5
        try:
            os.remove(archivo)
        except:
            pass

# INTERFAZ GRAFICA POR CONSOLA
def main():
    while True:
        seguir = input("¿Seguimos conversando? Y / N: ").strip().upper()

        if seguir == "N":
            print("Fin de la conversación.")
            break

        try:
            grabar_audio()

            consulta = transcribir_audio()
            print(f"Vos dijiste: {consulta}")

            if not consulta:
                print("No se detectó texto en la grabación.")
                continue

            respuesta = preguntar_modelo(consulta)
            print(f"Asistente: {respuesta}")

            hablar(respuesta)

        except Exception as e:
            print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    main()
