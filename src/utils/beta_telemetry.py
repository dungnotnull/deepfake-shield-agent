import json
import os
from datetime import datetime
from typing import Dict, Any

class BetaTelemetrySystem:
    """
    Production telemetry system for the Public Beta.
    Tracks False Positives and Model Drift.
    """
    def __init__(self, storage_path: str = "data/telemetry.jsonl"):
        self.storage_path = storage_path

    def record_event(self, user_id: str, event_type: str, data: Dict[str, Any]):
        """
        Records a detection event. 
        event_type can be 'DETECTION', 'USER_CORRECTION' (False Positive), 'SESS_END'.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "type": event_type,
            "data": data
        }
        
        with open(self.storage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def compute_metrics(self) -> Dict[str, float]:
        """
        Computes Beta KPIs: False Positive Rate and Detection Accuracy.
        """
        total_alerts = 0
        false_positives = 0
        
        if not os.path.exists(self.storage_path):
            return {"fpr": 0.0, "accuracy": 0.0}
            
        with open(self.storage_path, "r") as f:
            for line in f:
                evt = json.loads(line)
                if evt["type"] == "DETECTION": total_alerts += 1
                if evt["type"] == "USER_CORRECTION": false_positives += 1
        
        fpr = false_positives / total_alerts if total_alerts > 0 else 0.0
        return {"fpr": fpr, "accuracy": 1.0 - fpr}

if __name__ == "__main__":
    telemetry = BetaTelemetrySystem()
    telemetry.record_event("user_1", "DETECTION", {"score": 0.85})
    telemetry.record_event("user_1", "USER_CORRECTION", {"score": 0.85})
    print(f"Current Beta FPR: {telemetry.compute_metrics()}")
