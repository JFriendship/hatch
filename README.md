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

### Run with Docker Compose

Install Docker with the Docker Compose plugin (Docker Desktop includes both), and make sure Docker is running. You do not need Python or Node.js installed on your host for this option. Allow enough disk space for the images and model cache, and enough memory for the 4B-parameter model; Docker Desktop must have sufficient memory allocated to its virtual machine.

From the repository root, build and start both services:

```bash
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173) once the frontend is running.

> **First-launch warning:** downloading the model and tokenizer can take about **10 minutes**, depending on your connection and hardware. Internet access is required for this download. The frontend may open before the backend is ready; wait for `Application startup complete` in the backend logs before sending a prompt. Startup also includes loading the model into memory.

Downloaded model files are stored in the named Docker volume `huggingface_cache`, mounted at `/home/appuser/.cache/huggingface` in the backend container. Compose normally prefixes the volume name with the project name (for example, `hatch_huggingface_cache`). The cache survives container recreation, image rebuilds, and `docker compose down`, so later launches reuse the download. The model must still load into memory on each backend startup. Changing the Compose project name creates a separate volume and may trigger another download.

To run in the background and follow backend startup:

```bash
docker compose up --build -d
docker compose logs -f backend
```

Stop the services while keeping the model cache:

```bash
docker compose down
```

**Cache reset:** `docker compose down --volumes` also deletes the model cache and other Compose-managed volumes. Use it only when you intend to discard that data; the next launch will download the model again.

The API is exposed at [http://localhost:8000](http://localhost:8000), with interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs) after startup completes. Ports `5173` and `8000` must be available on your host.

The current Docker image installs **CPU-only PyTorch** and does not configure GPU acceleration. Generation can be slow, even after the initial download. The Compose setup runs the Vite development server and mounts the source directories into the containers; it is intended for local development. Backend source changes require a service restart (`docker compose restart backend`); dependency or Dockerfile changes require rebuilding the affected image.

### Run without Docker

#### Prerequisites

- Python 3 with virtual environment support and a compatible [PyTorch installation](https://pytorch.org/get-started/locally/).
- Node.js and npm compatible with the project's Vite version. See [Vite prerequisites](https://vite.dev/guide/).
- Internet access for the initial model download.
- Sufficient disk space and RAM/VRAM to load and run the model.

The commands below assume a macOS or Linux shell.

#### Backend

From the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

`backend/requirements.txt` pins the backend and model dependencies, including PyTorch, Transformers, and Accelerate.

The first startup downloads the model and tokenizer and can take about **10 minutes**. When running without Docker, these files use the host's Hugging Face cache (normally `~/.cache/huggingface`), separate from the Docker volume. Subsequent startups can reuse cached files but still need to load the model into memory. Wait for `Application startup complete` before submitting requests.

Interactive API documentation is available at:

<http://localhost:8000/docs>

#### Frontend

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
| Maximum new tokens | `50` |
| Sampling enabled | `True` |
| Temperature | `0.7` |
| Top-p | `0.9` |
| Return input prompt with output | `False` |

Generation settings are configured in source rather than supplied per request.

## Project structure

```text
hatch/
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/generate_text.py
│   │   ├── schemas/model_inference.py
│   │   └── services/model_inference.py
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/chat.ts
    │   ├── components/
    │   ├── types/chat.ts
    │   └── App.tsx
    ├── Dockerfile
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
npm run preview -- --host localhost --port 5173 --strictPort
```

The build command performs TypeScript checking before bundling into `frontend/dist/`. Preview requires a successful build first; it does not build the app itself. Open [http://localhost:5173](http://localhost:5173) after starting preview with the command above. Stop any frontend development server or Docker frontend using port `5173` first.

The preview command explicitly uses port `5173` to match the backend's allowed CORS origin. Plain `npm run preview` defaults to port `4173`, which the backend currently does not allow. The backend must be running separately and have finished loading the model for chat requests to work. If you change `VITE_API_URL`, rebuild before restarting preview because the API URL is embedded at build time.

## Troubleshooting

- **Frontend opens but requests fail:** check `docker compose logs -f backend`. The API cannot serve requests until the model finishes downloading and loading. If startup fails, the logs contain the underlying error.
- **Backend exits or is killed while loading:** check available memory and Docker Desktop's memory allocation. Also check disk space for image builds and the model cache.
- **Port already in use:** stop the conflicting process or adjust the host port in `docker-compose.yml`. If you change the backend's host port, update `VITE_API_URL`; if you change the frontend's origin, update the backend's CORS configuration as described above.

The Compose port mappings listen on all host interfaces by default. For access only from your computer, bind them to `127.0.0.1` (for example, `127.0.0.1:8000:8000` and `127.0.0.1:5173:5173`). The application has no authentication and should not be exposed as a public service.
