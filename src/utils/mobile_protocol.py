import json
from typing import Dict, Any

class MobileShieldProtocol:
    """
    Defines the communication schema between the Mobile App (Android/iOS) 
    and the Detection Core.
    """
    @staticmethod
    def serialize_stream_packet(packet_id: int, modality: str, data: bytes) -> str:
        """Serializes data for transmission to the core."""
        return json.dumps({
            "id": packet_id,
            "modality": modality,
            "payload": data.hex()
        })

    @staticmethod
    def deserialize_risk_alert(json_alert: str) -> Dict[str, Any]:
        """Parses the risk alert coming from the core to be displayed on mobile."""
        return json.loads(json_alert)

if __name__ == "__main__":
    print("Mobile Protocol Logic Ready.")
