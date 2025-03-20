import subprocess
import time
import signal
from flask import Flask, request, jsonify
from flask_cors import CORS

from persona import generate_system_prompt  
from persona import PERSONA
from persona import update_persona_ai

from run_main import start_server

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Store process reference globally
assistant_process = None

def restart_assistant():
    """Stops the existing process (if running) and starts main.py again."""
    global assistant_process
    print("restart assist")

    # Stop the previous process if it's running
    if assistant_process:
        assistant_process.terminate()  # Graceful stop
        time.sleep(2)  # Wait for process to terminate
        print("stopped previous processs")
        assistant_process = None

    # Start the assistant in the background
    # start_server()
    # assistant_process = subprocess.Popen(["py", "main.py", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print("✅ AI Assistant restarted successfully!")
    # # Wait a moment for the process to initialize
    # time.sleep(1)

    # if assistant_process.poll() is None:
    #     print("Process started successfully and is running.")
    # else:
    #     print("Process terminated or failed to start.")
        


    assistant_process = subprocess.Popen(
        ["py", "main.py", "start"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Ensures output is in string format
        bufsize=1,  # Line buffering
        universal_newlines=True  # Helps with cross-platform compatibility
    )

    print("✅ AI Assistant restarted successfully!")
    # Wait a moment for the process to initialize
    time.sleep(1)
    print(f"in resaster ass {generate_system_prompt()}")

    if assistant_process.poll() is None:
        print("Process started successfully and is running.")
    else:
        print("Process terminated or failed to start.")

    print("random")

    stdout, stderr = assistant_process.communicate(timeout=2)
    if stdout:
        print("Process output:", stdout.decode())
    if stderr:
        print("Process error:", stderr.decode())

    # Read stdout and stderr in real time
    # for line in assistant_process.stdout:
    #     print("STDOUT:", line, end="")  # `end=""` prevents extra newlines

    # for line in assistant_process.stderr:
    #     print("STDERR:", line, end="")


@app.route('/api/update_persona', methods=['POST'])
def update_persona():
    """Update the persona and restart the assistant."""
    try:
        new_persona_data = request.json

        # Update the global persona (you can store this in memory)
        # global PERSONA
        # print(new_persona_data)
        update_persona_ai(new_persona_data)
        # print(f"new_ne{new_persona_data}")

        # print(f"post place {PERSONA}")
        # print(f"in after update post {generate_system_prompt()}")

        
        # Restart the assistant with the new persona
        restart_assistant()

        return jsonify({"status": "success", "message": "Persona updated and AI Assistant restarted"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Start Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)

    # if __name__ == "__main__":
    # app.run(debug=False)  # Prevents unexpected restarts
