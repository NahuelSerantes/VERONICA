# VERONICA

Proyecto VERONICA – Asistente I.A

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/NahuelSerantes/VERONICA
cd VERONICA
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar entorno (Windows):

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución

```bash
python main.py
```

---

## Variables de entorno

Crear un archivo `.env` basado en `.env.example`:

```env
API_KEY=tu_clave
```

---

##  Estructura

```
veronica/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Notas

* Asegurate de tener Python instalado (recomendado 3.10+)
* Si algo falla, revisá que el entorno virtual esté activado
* En ALGUNOS WINDOWS NO VIENE INSTALADO --> ffmpeg (Un complemento que necesita para funcionar)
  DESCARGALO AQUÍ --> https://ffmpeg.org/download.html y ponlo en la carpeta C:\ffmpeg\bin

---

## Licencia

MIT
