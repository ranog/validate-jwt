import base64
import json


def extract_jwt_claims(jwt: str) -> dict:
    header, payload, _ = jwt.split(".")
    decoded_payload = base64.b64decode(payload + "===").decode("utf-8")
    claims = json.loads(decoded_payload)
    return {key.capitalize(): value for key, value in claims.items()}
