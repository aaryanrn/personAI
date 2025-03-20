from flask import Flask, request, jsonify
from persona import generate_system_prompt  # Ensure PERSONA is imported
from main import restart_assistant_async  # Import the async version
import asyncio
import threading
import nest_asyncio  # Import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

app = Flask(__name__)

# Store process reference globally
assistant_process = None

@app.route('/api/update_persona', methods=['POST'])
def update_persona():
    """Update the persona and restart the assistant."""
    try:
        new_persona_data = request.json

        # Update the global persona (you can store this in memory)
        # global PERSONA
        PERSONA = new_persona_data
        print("👤 Updated Persona:", PERSONA)
        print(generate_system_prompt(PERSONA))  # Generate the new system prompt
        print("✅ Persona updated successfully!")

        # Restart the assistant with the new persona
        # Run the async function in a separate thread to avoid blocking the Flask route
        threading.Thread(target=run_async_restart).start()
        print("🔄 AI Assistant restart initiated")

        return jsonify({"status": "success", "message": "Persona updated and AI Assistant restart initiated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def run_async_restart():
    """Helper function to run the async restart_assistant_async in a new event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(restart_assistant_async())
    finally:
        loop.close()

if __name__ == '__main__':
    # Start Flask server
    print("🚀 Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)