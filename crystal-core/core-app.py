from flask import Flask, request, jsonify
import grpc

# Import gRPC stubs
import voice_processor_pb2 as vp_pb2
import voice_processor_pb2_grpc as vp_pb2_grpc
import note_manager_pb2 as nm_pb2
import note_manager_pb2_grpc as nm_pb2_grpc
import model_orchestrator_pb2 as mo_pb2
import model_orchestrator_pb2_grpc as mo_pb2_grpc

# gRPC clients
class VoiceProcessorClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = vp_pb2_grpc.VoiceProcessorStub(self.channel)

    def recognize_speech(self, audio: bytes) -> str:
        request = vp_pb2.RecognizeSpeechRequest(audio=audio)
        response = self.stub.RecognizeSpeech(request)
        return response.text

    def synthesize_speech(self, text: str) -> bytes:
        request = vp_pb2.SynthesizeSpeechRequest(text=text)
        response = self.stub.SynthesizeSpeech(request)
        return response.audio

class NoteManagerClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50052')
        self.stub = nm_pb2_grpc.NoteManagerStub(self.channel)

    def create_note(self, content: str) -> str:
        request = nm_pb2.CreateNoteRequest(content=content)
        response = self.stub.CreateNote(request)
        return response.note_id

    def update_note(self, note_id: str, content: str) -> bool:
        request = nm_pb2.UpdateNoteRequest(note_id=note_id, content=content)
        response = self.stub.UpdateNote(request)
        return response.success

    def delete_note(self, note_id: str) -> bool:
        request = nm_pb2.DeleteNoteRequest(note_id=note_id)
        response = self.stub.DeleteNote(request)
        return response.success

    def get_note(self, note_id: str) -> str:
        request = nm_pb2.GetNoteRequest(note_id=note_id)
        response = self.stub.GetNote(request)
        return response.content

class ModelOrchestratorClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50053')
        self.stub = mo_pb2_grpc.ModelOrchestratorStub(self.channel)

    def process_language(self, text: str) -> dict:
        request = mo_pb2.ProcessTextRequest(text=text)
        response = self.stub.ProcessText(request)
        return {"result": response.result}

    def get_model_prediction(self, model_name: str, data: dict) -> dict:
        request = mo_pb2.GetPredictionRequest(model_name=model_name, input_data=str(data))
        response = self.stub.GetPrediction(request)
        return {"prediction": response.prediction}

# RequestHandler class to handle incoming requests
class RequestHandler:
    def __init__(self, voice_client, note_client, model_client):
        self.voice_client = voice_client
        self.note_client = note_client
        self.model_client = model_client

    def handle_user_request(self, request: dict):
        if 'voice_command' in request:
            return self.process_voice_command(request['voice_command'])
        elif 'note_data' in request:
            return self.manage_note(request['note_data'])
        elif 'task' in request:
            return self.orchestrate_models(request['task'])
        else:
            return {'error': 'Invalid request'}

    def process_voice_command(self, command: str):
        # Use voice_client to process the command
        audio = self.voice_client.synthesize_speech(command)
        recognized_text = self.voice_client.recognize_speech(audio)
        return {'response': f'Processed voice command: {recognized_text}'}

    def manage_note(self, note_data: dict):
        # Use note_client to manage notes
        if 'action' not in note_data:
            return {'error': 'Missing action in note_data'}
        
        action = note_data['action']
        if action == 'create':
            note_id = self.note_client.create_note(note_data.get('content', ''))
            return {'response': f'Created note with ID: {note_id}'}
        elif action == 'update':
            success = self.note_client.update_note(note_data.get('note_id'), note_data.get('content', ''))
            return {'response': f'Updated note: {success}'}
        elif action == 'delete':
            success = self.note_client.delete_note(note_data.get('note_id'))
            return {'response': f'Deleted note: {success}'}
        elif action == 'get':
            content = self.note_client.get_note(note_data.get('note_id'))
            return {'response': f'Note content: {content}'}
        else:
            return {'error': 'Invalid note action'}

    def orchestrate_models(self, task: str):
        # Use model_client to orchestrate models
        processed_result = self.model_client.process_language(task)
        prediction = self.model_client.get_model_prediction("default_model", processed_result)
        return {'response': f'Model prediction for task "{task}": {prediction["prediction"]}'}

# CrystalCore class to initialize and run the Flask app
class CrystalCore:
    def __init__(self):
        self.flask_app = Flask(__name__)
        self.voice_client = VoiceProcessorClient()
        self.note_client = NoteManagerClient()
        self.model_client = ModelOrchestratorClient()
        self.request_handler = RequestHandler(self.voice_client, self.note_client, self.model_client)
        self.initialize_app()

    def initialize_app(self):
        @self.flask_app.route('/', methods=['POST'])
        def handle_request():
            data = request.json or {}
            response = self.request_handler.handle_user_request(data)
            return jsonify(response)

    def run_server(self):
        self.flask_app.run(host='0.0.0.0', port=5005)

if __name__ == '__main__':
    crystal_core = CrystalCore()
    crystal_core.run_server()