# Hatch

Hatch is a local text-generation application built with Hugging Face Transformers, FastAPI, and React. It serves a pretrained Qwen language model through an API and provides a browser interface for submitting prompts and viewing responses.

This project explores LLM inference, model lifecycle management, input validation, and frontend/backend integration. It uses pretrained model weights without training or fine-tuning.

## Features

- Loads `Qwen/Qwen3-4B-Instruct-2507` and its tokenizer through Hugging Face Transformers.
- Initializes the model once during backend startup and reuses it across requests.
- Validates API requests and responses with Pydantic schemas.
- Provides a React/TypeScript interface with message display and loading feedback.
- Supports a configurable backend URL through `VITE_API_URL`.

## Architecture

```text
React interface
    → FastAPI endpoint
    → Pydantic input validation
    → Hugging Face generation pipeline
    → Tokenization, generation, and decoding
    → JSON response
    → Response displayed in the interface
```

The backend stores the generation pipeline in application state. A FastAPI dependency makes it available to the inference endpoint.

## Getting started

### Prerequisites

- Python 3 with virtual environment support and a compatible [PyTorch installation](https://pytorch.org/get-started/locally/).
- Node.js and npm compatible with the project's Vite version. See [Vite prerequisites](https://vite.dev/guide/).
- Internet access for the initial model download.
- Sufficient disk space and RAM/VRAM to load and run the model.

The commands below assume a macOS or Linux shell.

### Backend

From the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
python -m pip install torch transformers accelerate

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The current `requirements.txt` does not include the model libraries, so they are installed separately above. These additional dependencies are not yet pinned. Use a Transformers version that supports Qwen3; see the [model card](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507).

The first startup downloads the model and tokenizer. Subsequent startups can reuse cached files but still need to load the model into memory. Wait for startup to finish before submitting requests.

Interactive API documentation is available at:

<http://localhost:8000/docs>

### Frontend

In a second terminal, from the repository root:

```bash
cd frontend
npm ci
npm run dev -- --host localhost --port 5173 --strictPort
```

Open <http://localhost:5173>.

The frontend defaults to `http://localhost:8000` for API requests. To change this, add the following to `frontend/.env.local` and restart Vite:

```dotenv
VITE_API_URL=http://localhost:8000
```

The backend's CORS configuration currently permits `http://localhost:5173`. Update `backend/app/main.py` if the frontend uses a different origin.

## API

### `POST /gentext/qweninference`

Accepts a `prompt` string between 1 and 2,000 characters.

```bash
curl -X POST http://localhost:8000/gentext/qweninference \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Explain what a language model does in one sentence."}'
```

Example response shape; generated text will vary:

```json
{
  "model_response": "A language model predicts and generates text.",
  "char_count": 45
}
```

`char_count` reports the number of characters in the generated response. Invalid request bodies return HTTP `422`.

## Generation configuration

Settings are defined in `backend/app/services/model_inference.py`.

| Setting | Value |
| --- | --- |
| Model | `Qwen/Qwen3-4B-Instruct-2507` |
| Device placement | `auto` |
| Model dtype | `auto` |
| Maximum new tokens | `250` |
| Sampling enabled | `True` |
| Temperature | `0.7` |
| Top-p | `0.9` |
| Return input prompt with output | `False` |

Generation settings are configured in source rather than supplied per request.

## Project structure

```text
hatch/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/generate_text.py
│   │   ├── schemas/model_inference.py
│   │   └── services/model_inference.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/chat.ts
    │   ├── components/
    │   ├── types/chat.ts
    │   └── App.tsx
    └── package.json
```

## Current limitations

- **Single-turn inference:** the interface displays message history, but each request sends only the latest prompt. History is cleared on refresh.
- **Plain-text prompting:** the backend passes a raw prompt string without explicitly applying a chat template. Responses may continue the prompt instead of answering it directly.
- **One configured model:** model selection is not exposed through the interface or API.
- **Basic error handling:** the API client detects failed requests, but the interface does not display a dedicated error message.
- **Local prototype:** authentication, rate limiting, streaming, and persistent storage are not implemented.
- **Evaluation:** automated tests, model-quality evaluations, and latency benchmarks are not currently included.

## Frontend development

Run from `frontend/`:

```bash
npm run lint
npm run build
npm run preview
```

The build command performs TypeScript checking before bundling. Preview serves an existing frontend build; the backend must be started separately.