import random
import string

from smolagents.tools import Tool


class PasswordGeneratorTool(Tool):
    name = "password_generator"
    description = """Generates a secure password based on a security level and length.
    Security levels:
    - 'low': only lowercase letters
    - 'medium': lowercase + uppercase + numbers
    - 'high': lowercase + uppercase + numbers + special characters (!@#$%^&*)
    """
    inputs = {
        "level": {
            "type": "string",
            "description": "Security level: 'low', 'medium', or 'high'",
        },
        "length": {
            "type": "integer",
            "description": "Length of the password (e.g. 8, 12, 16)",
        },
    }
    output_type = "string"

    def forward(self, level: str, length: int) -> str:

        # Definir los caracteres según el nivel
        if level == "low":
            characters = string.ascii_lowercase

        elif level == "medium":
            characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

        elif level == "high":
            characters = (
                string.ascii_lowercase
                + string.ascii_uppercase
                + string.digits
                + "!@#$%^&*"
            )

        else:
            return f"Error: nivel '{level}' no válido. Usa 'low', 'medium' o 'high'."

        # Validar longitud mínima
        if length < 6:
            return "Error: la longitud mínima es 6 caracteres."

        # Generar la contraseña
        password = "".join(random.choice(characters) for _ in range(length))

        return f"Contraseña generada ({level}, {length} caracteres): {password}"

    def __init__(self, *args, **kwargs):
        self.is_initialized = False
