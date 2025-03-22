import base64
import json


def extract_jwt_claims(jwt: str) -> dict:
    _, payload, _ = jwt.split(".")
    decoded_payload = base64.b64decode(payload + "===").decode("utf-8")
    claims = json.loads(decoded_payload)
    return {key.lower(): value for key, value in claims.items()}
