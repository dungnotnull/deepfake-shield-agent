from faster_whisper import WhisperModel

def run_asr():
    print("Initializing faster-whisper ASR...")
    # model = WhisperModel("base", device="cpu", compute_type="int8")
    print("ASR Ready. Streaming audio to text...")

if __name__ == "__main__":
    run_asr()
