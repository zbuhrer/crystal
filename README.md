# Crystal Cortex Container Architecture

```mermaid
classDiagram
    class DockerHost {
        +Docker Network
        +Volume: SharedStorage
    }

    class CrystalCoreContainer {
        +Flask App
        +gRPC Client
        -handle_user_request()
        -coordinate_processing()
    }

    class VoiceProcessorContainer {
        +gRPC Server
        +SpeechRecognition Model
        +TTS Model
        -process_speech()
        -generate_speech()
    }

    class NoteManagerContainer {
        +gRPC Server
        +Markdown Library
        -parse_markdown()
        -edit_note()
    }

    class ModelOrchestratorContainer {
        +gRPC Server
        +LangChain
        +Model Server
        -process_language()
        -serve_model()
    }

    DockerHost -- CrystalCoreContainer
    DockerHost -- VoiceProcessorContainer
    DockerHost -- NoteManagerContainer
    DockerHost -- ModelOrchestratorContainer

    CrystalCoreContainer ..> VoiceProcessorContainer : gRPC
    CrystalCoreContainer ..> NoteManagerContainer : gRPC
    CrystalCoreContainer ..> ModelOrchestratorContainer : gRPC

    note for DockerHost "Single machine hosting\nall containers"
    ```
