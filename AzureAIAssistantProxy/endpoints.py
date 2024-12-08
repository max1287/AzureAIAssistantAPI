from flask import jsonify, render_template, request
from AzureAIAssistantProxy import app

from azureAIClient import client
import time
import json

@app.route('/')
def home():
    return "READY"


@app.route('/start-thread', methods=['POST'])
def start_thread():
    try:
        thread = client.beta.threads.create()
        return jsonify({"threadId": thread.id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/process-message', methods=['POST'])
def process_message():
    try:
        data = request.get_json()
        assistantId = data.get('assistantId')
        threadId = data.get('threadId')
        message = data.get('message')

        if not assistantId or not threadId or not message:
            return jsonify({"error": "'assistantId', 'threadId' and 'message' are required."}), 400

        # Retrieve the thread
        thread = client.beta.threads.retrieve(threadId)

        # Add a user question to the thread
        userMessage = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Create a run for the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistantId,
        )

        # Poll the run status until it's completed or an error occurs
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        status = run.status

        while status not in ["completed", "cancelled", "expired", "failed"]:
            time.sleep(5)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            status = run.status

        # Return the final response when the run is completed
        if status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id);
            data = json.loads(messages.model_dump_json(indent=2))
            lastAnswer = data['data'][0]['content'][0]
            return jsonify({"response": lastAnswer}), 200
        else:
            return jsonify({"error": f"Run ended with status: {status}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

