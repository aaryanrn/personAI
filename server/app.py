import subprocess
import time
import signal
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store process reference globally
assistant_process = None

def restart_assistant():
    """Stops the existing process (if running) and starts run_assistant.py again."""
    global assistant_process

    # Stop the previous process if it's running
    if assistant_process:
        assistant_process.terminate()  # Graceful stop
        time.sleep(2)  # Wait for process to terminate
        assistant_process = None

    # Start the assistant in the background
    assistant_process = subprocess.Popen(["py", "run_assistant.py", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("✅ AI Assistant restarted successfully!")

@app.route('/api/update_persona', methods=['POST'])
def update_persona():
    """Update the persona and restart the assistant."""
    try:
        new_persona_data = request.json

        # Update the global persona (you can store this in memory)
        global PERSONA
        PERSONA = new_persona_data
        
        # Restart the assistant with the new persona
        restart_assistant()

        return jsonify({"status": "success", "message": "Persona updated and AI Assistant restarted"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Start Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)
