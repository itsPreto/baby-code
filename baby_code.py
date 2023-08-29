#!/usr/bin/env python3
import os
import json
import subprocess
import time
import argparse
import csv
import webbrowser
import magic
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pandas as pd
import zipfile
import tarfile
from pydub.utils import mediainfo
from moviepy.editor import VideoFileClip
# PyPDF2 and python-docx will be used for document extraction
import PyPDF2
from docx import Document

# Assuming the ChatSession class is in a file named chat_session.py
from memory.chat_session import ChatSession

app = Flask(__name__)
CORS(app)

TEXT_EXTENSIONS = ['.txt', '.md', '.csv', '.tsv', '.log', '.json', '.xml','.yml', '.yaml', '.ini', '.conf']
CODE_EXTENSIONS = ['.py', '.js', '.html', '.css', '.c', '.cpp', '.java', '.sh','.bat']
DATA_EXTENSIONS = ['.csv', '.json', '.xls', '.xlsx', '.xml', '.sql', '.db', '.h5', '.pkl']
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico','.svg']
DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.odt', '.ods','.rtf']
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.flv', '.mov', '.wmv', '.webm']
ARCHIVE_EXTENSIONS = ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2']
OTHER_EXTENSIONS = ['.iso', '.img']

parser = argparse.ArgumentParser( description="An example of using server.cpp with a similar API to OAI. It must be used together with server.cpp.")

parser.add_argument("--stop", type=str, help="the end of response in chat completions(default: '</s>')", default="</s>")
parser.add_argument("--llama-api", type=str, help="Set the address of server.cpp in llama.cpp(default: http://127.0.0.1:8080)", default='http://127.0.0.1:8080')
parser.add_argument("--api-key", type=str, help="Set the api key to allow only few user(default: NULL)", default="")
parser.add_argument("--host", type=str, help="Set the ip address to listen.(default: 127.0.0.1)", default='127.0.0.1')
parser.add_argument("--model_path", type=str, help="Set the port to listen.(default: 8081)", default="./llama.cpp/models/CodeLlama-7b-Python/codellama-7b-python.Q5_K_M.gguf")
parser.add_argument("--port", type=int, help="Set the port to listen.(default: 8081)", default=8081)

args = parser.parse_args()


@app.route('/run_python_code', methods=['POST'])
def run_python_code():
    """
    Run Python code and return the stdout and stderr.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the stdout and stderr.

    Raises:
        None
    """
    code = request.json['code']
    stdout, stderr = execute(code)

    # Check if there's a "ModuleNotFoundError"
    if "ModuleNotFoundError" in stderr:
        module_name = stderr.split("'")[
            1]  # Extract the module name from the error message
        response = install_dependency(module_name)

        # If the module was installed successfully, re-run the code
        if response['status'] == 'success':
            stdout, stderr = execute(code)

    return {"stdout": stdout, "stderr": stderr}


@app.route('/install_module', methods=['POST'])
def install_module():
    """
    Installs the specified Python module.

    Parameters:
    - module_name (str): The name of the Python module to install.

    Returns:
    - Status message indicating the result of the installation.
    """
    module_name = request.json['module_name']
    response = install_dependency(module_name)
    return response


def install_dependency(module_name):
    """
    Installs the specified Python module using pip.

    Parameters:
    - module_name (str): The name of the Python module to install.

    Returns:
    - Status message indicating the result of the installation.
    """
    process = subprocess.Popen(["pip", "install", module_name],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return {"status": "success",
                "message": f"Module {module_name} installed successfully."}
    else:
        return {"status": "error", "message": stderr.decode()}


def execute(code):
    process = subprocess.Popen(["python3", "-c", code],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()


@app.route('/read_file_sample', methods=['POST'])
def read_file_sample():
    """
    Reads a sample from the provided file path and returns the content.

    Parameters:
    - filepath (str): The path to the file.

    Returns:
    - If the reading is successful, a sample of the file content.
    - If there's an error, an error message.
    """
    filepath = request.json['filepath']

    if not os.path.exists(filepath):
        return {"error": "File not found."}, 404

    print(f"Received request for {filepath}")

    extension = "." + filepath.split('.').pop().lower()

    # Print detected extension
    print("Detected extension:", extension)

    # Detect MIME type
    mime_detector = magic.Magic(mime=True)
    mime_type = mime_detector.from_file(filepath)

    # Print detected MIME type
    print("Detected MIME type:", mime_type)

    MAX_CHARACTERS = 500  # Or any other number you find suitable

    mime_to_extension = {
        # Text Files
        "text/plain": [".txt", ".md", ".log", ".ini", ".conf", ".sh", ".bat",
                       ".c", ".cpp", ".java", ".py", ".js", ".css", ".html"],
        "text/csv": [".csv"],
        "text/tab-separated-values": [".tsv"],
        "application/json": [".json"],
        "application/xml": [".xml"],
        "application/x-yaml": [".yml", ".yaml"],

        # Image Files
        "image/jpeg": [".jpg", ".jpeg"],
        "image/png": [".png"],
        "image/gif": [".gif"],
        "image/bmp": [".bmp"],
        "image/tiff": [".tiff"],
        "image/x-icon": [".ico"],
        "image/svg+xml": [".svg"],

        # Data Files
        "application/vnd.ms-excel": [".xls"],
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
            ".xlsx"],
        "application/sql": [".sql"],
        "application/x-sqlite3": [".db"],
        "application/x-hdf": [".h5"],
        "application/octet-stream": [".pkl"],
        # General binary, might need more specific handling

        # Document Files
        "application/pdf": [".pdf"],
        "application/msword": [".doc"],
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
            ".docx"],
        "application/vnd.ms-powerpoint": [".ppt"],
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": [
            ".pptx"],
        "application/vnd.oasis.opendocument.text": [".odt"],
        "application/vnd.oasis.opendocument.spreadsheet": [".ods"],
        "application/rtf": [".rtf"],

        # Audio Files
        "audio/mpeg": [".mp3"],
        "audio/wav": [".wav"],
        "audio/ogg": [".ogg"],
        "audio/flac": [".flac"],
        "audio/mp4": [".m4a", ".aac"],

        # Video Files
        "video/mp4": [".mp4"],
        "video/x-msvideo": [".avi"],
        "video/x-matroska": [".mkv"],
        "video/x-flv": [".flv"],
        "video/quicktime": [".mov"],
        "video/x-ms-wmv": [".wmv"],
        "video/webm": [".webm"],

        # Archive Files
        "application/zip": [".zip"],
        "application/x-tar": [".tar"],
        "application/gzip": [".gz"],
        "application/x-rar-compressed": [".rar"],
        "application/x-7z-compressed": [".7z"],
        "application/x-bzip2": [".bz2"],

        # Other
        "application/x-iso9660-image": [".iso"],
        "application/x-apple-diskimage": [".img"],
    }

    # Validate MIME type against the extension
    print(f"Validating MIME type {mime_type} against extension {extension}...")
    # Validate MIME type against the extension
    if mime_type in mime_to_extension and extension not in mime_to_extension[
        mime_type]:
        print(
            f"MIME type validation failed for {mime_type} and extension {extension}.")
        return {
                   "error": f"File extension {extension} does not match detected MIME type {mime_type}."}, 400
    print(
        f"MIME type validation passed for {mime_type} and extension {extension}.")

    try:
        # Handle text-based and code files
        print("TEXT_EXTENSIONS:", TEXT_EXTENSIONS)
        print("CODE_EXTENSIONS:", CODE_EXTENSIONS)
        print("Condition Check:",
              extension in TEXT_EXTENSIONS or extension in CODE_EXTENSIONS)

        if extension in TEXT_EXTENSIONS or extension in CODE_EXTENSIONS:
            print("Handling text-based or code files.")
            with open(filepath, 'r') as f:
                if extension == "json":
                    print("Reading JSON file.")
                    data = json.load(f)
                    sample_data = json.dumps(data[:5], indent=4)[
                                  :MAX_CHARACTERS]
                elif extension == "csv":
                    print("Reading CSV file.")
                    reader = csv.reader(f)
                    header = next(reader, None)  # Get the header
                    rows = [header]
                    chars_read = len(",".join(header))
                    for row in reader:
                        if chars_read + len(",".join(row)) > MAX_CHARACTERS:
                            break
                        chars_read += len(",".join(row))
                        rows.append(row)
                    sample_data = "\n".join([",".join(row) for row in
                                             rows])  # Convert rows to CSV format
                else:
                    print("Reading general text file.")
                    content = f.read()
                    sample_data = content[:MAX_CHARACTERS]

        # Handle document files
        elif extension in DOCUMENT_EXTENSIONS:
            print("Handling document files.")
            if extension == "pdf":
                print("Reading PDF file.")
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfFileReader(f)
                    page = reader.getPage(0)
                    sample_data = page.extractText()[:MAX_CHARACTERS]
            elif extension == "docx":
                print("Reading DOCX file.")
                doc = Document(filepath)
                paragraphs = [p.text for p in doc.paragraphs]
                sample_data = "\n".join(paragraphs)[:MAX_CHARACTERS]
            else:
                sample_data = "Document type not supported for direct reading."

        # Handle audio files
        elif extension in AUDIO_EXTENSIONS:
            print("Handling audio files.")
            info = mediainfo(filepath)
            sample_data = f"Audio file detected. Duration: {info['duration']}s, Channels: {info['channels']}"

        # Handle video files
        elif extension in VIDEO_EXTENSIONS:
            print("Handling video files.")
            clip = VideoFileClip(filepath)
            sample_data = f"Video file detected. Duration: {clip.duration}s, Resolution: {clip.size[0]}x{clip.size[1]}"
            clip.reader.close()
            del clip

        # Handle archive files
        elif extension in ARCHIVE_EXTENSIONS:
            print("Handling archive files.")
            if extension in ['.zip']:
                print("Reading ZIP file.")
                with zipfile.ZipFile(filepath, 'r') as z:
                    sample_data = f"Archive contains: {', '.join(z.namelist())}"
            elif extension in ['.tar', '.gz', '.bz2']:
                print("Reading TAR or compressed TAR file.")
                with tarfile.open(filepath, 'r') as t:
                    sample_data = f"Archive contains: {', '.join(t.getnames())}"
            else:
                sample_data = "Archive type not supported for direct reading."

        # Handle other types
        elif extension in OTHER_EXTENSIONS:
            print("Handling special file types.")
            sample_data = "Special file detected. No direct reading available."

        else:
            return {"error": "Unsupported file type."}, 400

        print(f"Sample data extraction successful: {sample_data}")
        return {"sample_data": sample_data}
    except Exception as e:
        print(f"Error encountered: {str(e)}")
        return {"error": str(e)}, 500


CHAT_HISTORY_ENABLED = True
CURRENT_SESSION = None
CHAT_SESSIONS = []

CHAT_SESSIONS_PATH = "chat_sessions.json"


def save_chat_sessions():
    with open(CHAT_SESSIONS_PATH, 'w') as f:
        sessions_data = [session.to_dict() for session in CHAT_SESSIONS]
        json.dump(sessions_data, f)


@app.route('/toggle_chat_history', methods=['POST'])
def toggle_chat_history():
    global CHAT_HISTORY_ENABLED
    CHAT_HISTORY_ENABLED = not CHAT_HISTORY_ENABLED
    return {"status": "success", "enabled": CHAT_HISTORY_ENABLED}


@app.route('/add_message', methods=['POST'])
def add_message():
    global CURRENT_SESSION
    if not CHAT_HISTORY_ENABLED:
        return {"status": "error",
                "message": "Chat history saving is disabled."}

    sender = request.json['sender']
    content = request.json['content']
    timestamp = request.json['timestamp']

    if not CURRENT_SESSION:
        CURRENT_SESSION = ChatSession(session_id=str(time.time()),
                                      timestamp=timestamp)
    CURRENT_SESSION.add_message(sender, content, timestamp)

    return {"status": "success"}


@app.route('/end_session', methods=['POST'])
def end_session():
    global CURRENT_SESSION
    if CURRENT_SESSION:
        CHAT_SESSIONS.append(CURRENT_SESSION)
        save_chat_sessions()
        CURRENT_SESSION = None
    return {"status": "success"}


@app.route('/load_chat_session', methods=['POST'])
def load_chat_session():
    session_id = request.json['session_id']
    for session in CHAT_SESSIONS:
        if session.session_id == session_id:
            return {"status": "success", "session": session.to_dict()}
    return {"status": "error", "message": "Session not found."}


if __name__ == '__main__':
    # Run the server.cpp as a subprocess
    server_process = subprocess.Popen(["./llama.cpp/server", "-m", args.model_path, "-c", "4096", "-ngl", "1", "--path", "."])
    webbrowser.open(args.llama_api)
    # Pause for 5 seconds
    time.sleep(5)
    app.run(args.host, port=args.port)
