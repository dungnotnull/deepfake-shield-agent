import logging
from datetime import datetime

class AlertDispatcher:
    """
    Manages the delivery of alerts to the UI and logging systems.
    """
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("ShieldAlert")

    def dispatch(self, risk_data: Dict[str, Any]):
        level = risk_data["level"]
        score = risk_data["score"]
        
        if level == "ALERT":
            self.logger.error(f"🚨 CRITICAL ALERT: Risk Score {score:.2f}. Triggering Challenge Overlay!")
            # Real: call UI_API.show_hard_alert()
        elif level == "WARN":
            self.logger.warning(f"⚠️ WARNING: Risk Score {score:.2f}. Showing Caution Indicator.")
            # Real: call UI_API.show_soft_warn()
        else:
            self.logger.info(f"✅ Call Secure: Risk Score {score:.2f}.")

if __name__ == "__main__":
    dispatcher = AlertDispatcher()
    dispatcher.dispatch({"level": "ALERT", "score": 0.92})
