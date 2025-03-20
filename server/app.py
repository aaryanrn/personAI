# app.py - Flask application for persona configuration
from flask import Flask, request, jsonify
import os
import subprocess
import time
import signal
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Hardcoded persona for testing
PERSONA = {
    "persona_name": "Alex",
    "sex": "non-binary",
    "role": "technical advisor",
    "traits": "extensive knowledge in programming and AI",
    "tone": "friendly and informative",
    "purpose": "help users solve technical problems",
    "response_type": "concise yet detailed, with practical examples",
    "backstory": "Alex has 10 years of experience in software development and AI research"
}

# Global variable to track the assistant process
assistant_process = None

def generate_system_prompt(persona):
    """Generate a system prompt from a persona dictionary"""
    return f"""You are {persona['persona_name']}, a {persona['sex']} {persona['role']} known for {persona['traits']}. 
    You communicate in a {persona['tone']} manner. Your primary objective is to {persona['purpose']}. 
    You provide responses that are {persona['response_type']}. 
    Your Backstory is {persona['backstory']}."""

@app.route('/api/update_persona', methods=['POST'])
def update_persona():
    """Update the persona with the provided information."""
    global PERSONA
    try:
        # Get the new persona data from the request
        new_persona_data = request.json
        
        # Validate the persona data
        required_fields = ["persona_name", "sex", "role", "traits", "tone", 
                           "purpose", "response_type", "backstory"]
        
        # Check if all required fields are present
        missing_fields = [field for field in required_fields if field not in new_persona_data]
        if missing_fields:
            return jsonify({
                "status": "error", 
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
            
        # Update the persona
        PERSONA = new_persona_data
        
        # Generate the system prompt
        system_prompt = generate_system_prompt(PERSONA)
        
        # Save the system prompt to a file that the assistant script can read
        with open('system_prompt.txt', 'w') as f:
            f.write(system_prompt)
        
        return jsonify({
            "status": "success", 
            "message": "Persona updated successfully",
            "persona": PERSONA,
            "system_prompt": system_prompt
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)