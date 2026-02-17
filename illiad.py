import dotenv    # loads our .env file into environment variables
import os        # reads environment variables
import pathlib   # navigates the file system and opens files
import pprint    # for inspecting Iliad response messages
import requests  # for communicating with the Iliad API]
import json
from pathlib import Path

dotenv_path = Path('./RAG/.env')
dotenv.load_dotenv()

ILIAD_API_KEY = os.environ.get('ILIAD_API_KEY')
# ILIAD_URL = "https://prod.api.abbvienet.com/iliad/abbvie"

ILIAD_URL = "https://api-epic.ir-gateway.abbvienet.com/iliad"

# Get new token from 
# http://gprd-auth:8010/auth.service/auth/token
USER_TOKEN = os.environ.get("USER_TOKEN")

# Create a new source in Illiad named stats-test-source
def create_source():
    try:
        resp = requests.post(
            url= f"{ILIAD_URL}/api/v1/sources",
            headers={
                "x-api-key": ILIAD_API_KEY,
                "x-user-token": USER_TOKEN
            },
            json={
                "source": "spatdocs",
                "description": "spatDocuments"
            }
        )
        resp.raise_for_status()
        data = resp.json()
        print("Source created successfully.")
        return {"success": True, "data": data}

    # Throw an error if unsuccessful
    except requests.exceptions.RequestException as e:
        # Try to extract 'detail' from the response if available
        detail = None
        try:
            detail = resp.json().get("detail")
        except Exception:
            pass
        print(f"Failed to create source: {e}\nDetail: {detail}")
        return {"success": False, "error": str(e), "detail": detail}

# Upload documents that get embedded automatically to source "SPATdocs"
def upload_documents():
    results = []
    for file in pathlib.Path("./RAG/files").iterdir():
        try:
            with file.open("rb") as f:
                resp = requests.post(
                    url=f"{ILIAD_URL}/api/v1/sources/SPATdocs/documents",
                    headers={"x-api-key": ILIAD_API_KEY, "x-user-token": USER_TOKEN},
                    files={"file": f}
                )
            resp.raise_for_status()
            data = resp.json()
            print(f"Uploaded {file.name}: Success.")
            results.append({"file": file.name, "success": True, "data": data})
        except requests.exceptions.RequestException as e:
            detail = None
            try:
                detail = resp.json().get("detail")
            except Exception:
                pass
            print(f"Uploaded {file.name}: Failed. Error: {e}. Detail: {detail}")
            results.append({"file": file.name, "success": False, "error": str(e), "detail": detail})
    return results

# Delete document by document id from source
def delete_document(document_id):
    try:
        resp = requests.delete(
            url=f"{ILIAD_URL}/api/v1/sources/SPATdocs/documents/{document_id}",
            headers={"x-api-key": ILIAD_API_KEY, "x-user-token": USER_TOKEN},
        )
        resp.raise_for_status()
        if resp.content and 'application/json' in resp.headers.get('Content-Type', ''):
            data = resp.json()
        else:
            data = None
        print(f"Document {document_id} deleted successfully.")
        return {"success": True, "data": data}
    except requests.exceptions.RequestException as e:
        detail = None
        if resp is not None and resp.content and 'application/json' in resp.headers.get('Content-Type', ''):
            try:
                detail = resp.json().get('detail')
            except Exception:
                pass
        print(f"Failed to delete document {document_id}: {e}. Detail: {detail}")
        return {"success": False, "error": str(e), "detail": detail}

# List all docs from source
def list_documents():
    try:
        resp = requests.get(
            url=f"{ILIAD_URL}/api/v1/sources/SPATdocs/documents",
            headers={"x-api-key": ILIAD_API_KEY, "x-user-token": USER_TOKEN}
        )
        resp.raise_for_status()
        data = resp.json()
        print("Documents listed successfully.")
        pprint.pprint(data)
        return {"success": True, "data": data}
    except requests.exceptions.RequestException as e:
        detail = None
        try:
            detail = resp.json().get("detail")
        except Exception:
            pass
        print(f"Failed to list documents: {e}. Detail: {detail}")
        return {"success": False, "error": str(e), "detail": detail}

# Ask Illiad a question based on the source
def askasource(message, history = []):
    resp = None
    try:
        resp = requests.post(
            url=f"{ILIAD_URL}/api/v1/sources/SPATdocs/rag",
            headers={"x-api-key": ILIAD_API_KEY, "x-user-token": USER_TOKEN},
            json={
                "messages": history + [{"role": "user", "content": message}]
            }
        ) 
        resp.raise_for_status()
        
        data = resp.json()
        references = data.get("references", [])
        print(f"RAG score: {references[0]["score"]}")
        
        return {"success": True, "data": data}
    except requests.exceptions.RequestException as e:
        detail = None
        if resp is not None and resp.content and 'application/json' in resp.headers.get('Content-Type', ''):
            try:
                detail = resp.json().get('detail')
            except Exception:
                detail = resp.text  # fallback to raw response text
        print(f"Failed to ask source: {e}. Detail: {detail}")
        return {"success": False, "error": str(e), "detail": detail}

# Descrive a source
def describe_source():
    try:
        resp = requests.get(
            url = f"{ILIAD_URL}/api/v1/sources/SPATdocs",
            headers={"x-api-key": ILIAD_API_KEY, "x-user-token": USER_TOKEN},
        )
        pprint.pprint(resp.json())

    except requests.exceptions.RequestException as e:
        detail = None
        if resp is not None and resp.content and 'application/json' in resp.headers.get('Content-Type', ''):
            try:
                detail = resp.json().get('detail')
            except Exception:
                detail = resp.text  # fallback to raw response text
        print(f"Failed to ask source: {e}. Detail: {detail}")
        return {"success": False, "error": str(e), "detail": detail}


if __name__ == "__main__":
     create_source()
    # upload_documents()
    # list_documents()
    # delete_document('5adec050-38ad-4e9d-8db5-64c7bbf9567a')
    # describe_source()
    # print(askasource("Who are the reviewers of SAP?")["data"]['content'])
    #pass

