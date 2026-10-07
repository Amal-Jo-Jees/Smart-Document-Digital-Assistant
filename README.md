# Zero-Download Knowledge Assistant

The Zero-Download Knowledge Assistant is a lightweight, high-performance document question-answering application built with Streamlit and integrated with the Groq Cloud API.

Unlike traditional Retrieval-Augmented Generation (RAG) architectures that require downloading local embedding models or configuring vector databases, this solution extracts document text into memory and relies on large-context LLMs hosted on Groq Cloud infrastructure for document analysis.

## Core Features

* **Zero Local Dependencies**: Operates without downloading heavy local embedding models or vector databases.
* **Low-Latency Inference**: Leverages Groq Cloud API infrastructure for rapid query execution.
* **In-Memory PDF Extraction**: Extracts document text directly into memory using `pypdf`.
* **Custom UI Interface**: Utilizes custom CSS styling and SVG visual elements for an enhanced user experience.
* **Session Persistence**: Maintains conversation history for contextual follow-up questions within an active session.

## Technical Architecture

* **Frontend Framework**: Streamlit
* **PDF Parsing**: PyPDF
* **LLM Provider**: Groq Cloud API
* **Language Model**: `openai/gpt-oss-120b` (configurable based on available Groq models)

## Installation and Setup

### 1. Repository Cloning

```bash
git clone https://github.com/your-username/zero-download-assistant.git
cd zero-download-assistant
```

### 2. Environment Configuration

It is recommended to use a virtual environment to manage dependencies.

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Dependency Installation

Install the required Python dependencies:

```bash
pip install streamlit pypdf groq
```

## API Key Management

For production environments, hardcoding API keys directly into source code is strongly discouraged.

### Recommended Configuration

1. Obtain an API key from the Groq Cloud Console.
2. Define the key in Streamlit secrets (`.streamlit/secrets.toml`) or environment variables:

```toml
# .streamlit/secrets.toml
GROQ_API_KEY = "your_groq_api_key_here"
```

3. Retrieve the key dynamically within your code:

```python
import os
import streamlit as st

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
```

## Application Execution

To run the application locally:

```bash
streamlit run SMDAapp.py
```

Access the interface at `http://localhost:8501`.

## Usage Workflow

1. **Upload Document**: Upload a target PDF document using the file uploader widget.
2. **Text Processing**: The application extracts the document text into temporary memory.
3. **Query Submission**: Input your question in the chat interface. The system retrieves relevant context directly from the uploaded document text.

## Security and Usage Considerations

* **API Key Security**: Revoke and regenerate any API key that has been publicly committed to source control. Use environment variables or secrets managers for key management.
* **Context Window Constraints**: The entire document text is provided within the system prompt. Ensure the total token count of the document remains within the context window limits of the selected model.