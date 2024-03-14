## Talk to PDF
**PDF Text Extraction and Query Handling Service**

This service provides functionalities for extracting text from PDF files and handling queries based on the extracted text. It utilizes FastAPI for the web framework, Pydantic for data validation, and various libraries for PDF processing, text embeddings, and conversational retrieval.

## Dependencies and Installation
----------------------------

To install the App, please follow these steps:

Clone/Download the repository to your local machine.

### Backend Setup

1. **Installation**

   From the root directory of the project, navigate to the backend directory:

    ```
    cd backend/api
    ```

2. **Create the virtual environment**
   Run the following command to create a virtual environment named "myenv":
   
   **For Windows:**
   ```cmd
   python -m venv myenv
   ```
   
   **For macOS and Linux:**
   ```bash
   python3 -m venv myenv
   ```
   
   This will create a directory named `myenv` in your project folder which will contain a Python interpreter and other necessary files for the virtual environment.
   
   ### Activate the virtual environment
   Activating the virtual environment ensures that any Python-related commands (e.g., `python`, `pip`) you run will use the environment's Python interpreter and packages. Run the appropriate activation script for your operating system:
   
   **For Windows:**
   ```cmd
   myenv\Scripts\activate
   ```
   
   **For macOS and Linux:**
   ```bash
   source myenv/bin/activate
   ```
   
   After activating the environment, you'll notice that the command prompt changes, indicating that you're now working within the virtual environment.


3. **Install backend dependencies using npm:**

    ```
    pip install -r requirements.txt
    ```

    This command installs all the required Python dependencies specified in the `requirements.txt` file. Make sure to execute this command from the `backend/api` directory.

4. **Environment Variables**

    Create a `.env` file in the `backend/api` directory with the following variables, you can also check the `.env example` file:

    ```
    # Hugging Face Credentials (if using Hugging Face)
    HUGGINGFACEHUB_API_TOKEN=your_hugging_face_api_key

    # OpenAI Credentials (if using OpenAI)
    OPENAI_API_KEY=your_open_ai_api_key

5. **Running the Backend Server**

    After installing the dependencies and setting up the environment variables, start the backend server using the following command:

    ```
    uvicorn server:app --reload
    ```

    This command runs the FastAPI server with automatic reloading enabled, allowing for easy development.

### Frontend Setup

1. **Installation**

    From the root directory, navigate to the frontend directory:

    ```
    cd frontend/pdf
    ```

    Install frontend dependencies using npm:

    ```
    npm install
    ```

    This command installs all the required Node.js dependencies specified in the `package.json` file.

2. **Running the Frontend Server**

    After installing the dependencies, start the frontend server using the following command:

    ```
    npm start
    ```

    This command launches the frontend development server, enabling you to view and interact with the web application in your browser.

### Usage

1. **Endpoints**

    - **Upload PDF**: `POST /upload-pdf`
        - Uploads a PDF file to the server for text extraction.
        - Requires a file upload with the key `file`.
        - Returns a JSON response with the uploaded filename and a success message.

    - **Handle Query**: `POST /handle-query`
        - Handles a query based on the extracted text from uploaded PDFs.
        - Requires a JSON object with a `question` field containing the query.
        - Returns a JSON response with the answer to the query.

### Components

- **server.py**: Contains the FastAPI application with endpoints for uploading PDFs and handling queries. It integrates with PDF processing and query handling modules.

- **utils.py**: Provides utility functions for extracting text from PDF files.

- **hugging_face_provider.py**: Implements an alternative provider for text embeddings and conversational retrieval using Hugging Face models. It handles text chunking, vector embeddings, and query processing.

### Notes

- The `SQLALCHEMY_DATABASE_URL` specifies the path to the SQLite database used for storing document metadata. Adjust it as per your database configuration.
- If using Hugging Face models, make sure to set the `HUGGINGFACEHUB_API_TOKEN` environment variable with a valid API key and also install additional dependencies as mentioned in `requirements.txt` inside the `backend/api` directory.
- This service supports CORS for specific origins, as configured in `server.py`.

- I couldn't test the OpenAI provider because while creating embeddings I was getting this error:
```Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. 
For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', '
type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
```
- So, as an alternative I've used HuggingFaceInstructEmbeddings



Hope u like it :)
