import sys
import os

# Forzar UTF-8 en Windows para soportar emojis y caracteres especiales
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

import datetime

import pytz
import yaml
from dotenv import load_dotenv
from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    FinalAnswerTool,
    HfApiModel,
    load_tool,
    tool,
)
from Gradio_UI import GradioUI

# =====================================================
# 1️⃣ Cargar variables de entorno (.env)
# =====================================================
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN no encontrado en el archivo .env")


# =====================================================
# 2️⃣ Definir Tools locales
# =====================================================
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A simple demo tool.
    Args:
        arg1: first argument
        arg2: second argument (integer)
    """
    return f"You sent arg1={arg1} and arg2={arg2}"


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Get the current local time in a specified timezone.
    Args:
        timezone: A valid timezone string (e.g., 'America/New_York')
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current time in {timezone} is {local_time}"
    except Exception as e:
        return f"Error: {str(e)}"


# =====================================================
# 3️⃣ Tools externas
# =====================================================
final_answer = FinalAnswerTool()

search_tool = DuckDuckGoSearchTool()

image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)


# =====================================================
# 4️⃣ Modelo LLM
# =====================================================


model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HF_TOKEN,
    max_tokens=2092,
    temperature=0.5,
)


# =====================================================
# 5️⃣ Cargar System Prompt
# =====================================================
with open("prompts.yaml", "r", encoding="utf-8") as stream:
    prompt_templates = yaml.safe_load(stream)


# =====================================================
# 6️⃣ Crear el CodeAgent
# =====================================================
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        get_current_time_in_timezone,
        my_custom_tool,
        search_tool,
        image_generation_tool,
    ],
    max_steps=6,
    verbosity_level=1,
    prompt_templates=prompt_templates,
)


# =====================================================
# 7️⃣ Lanzar interfaz Gradio
# =====================================================
GradioUI(agent).launch()
