import base64

class Security:
    @staticmethod
    def encrypt(data: str) -> str:
        # Basic base64 encoding (not real encryption)
        return base64.b64encode(data.encode()).decode()

    @staticmethod
    def decrypt(data: str) -> str:
        try:
            return base64.b64decode(data.encode()).decode()
        except Exception:
            return "DECRYPTION_FAILED"
