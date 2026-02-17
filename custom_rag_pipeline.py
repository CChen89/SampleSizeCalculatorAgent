import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- CONFIG ---
ILIAD_API_KEY = os.environ.get('ILIAD_API_KEY')
ILIAD_URL_BASE = os.environ.get('ILIAD_URL_BASE')
API_VERSION = os.environ.get('API_VERSION')
DEPLOYMENT = os.environ.get('DEPLOYMENT')

pdf_dir = './RAG/data'          # Input PDFs
parsed_dir = './RAG/parsed_text' # Extracted text files
chunks_dir = './RAG/chunks'      # Text chunks
embeddings_dir = './RAG/embeddings' # Save embeddings here

os.makedirs(parsed_dir, exist_ok=True)
os.makedirs(chunks_dir, exist_ok=True)
os.makedirs(embeddings_dir, exist_ok=True)

# --- STEP 1: Parse PDFs to text ---
def parse_pdfs_to_text(pdf_dir, out_dir):
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        try:
            loader = PyPDFLoader(pdf_path, mode='single')
            docs = loader.load()
            text = docs[0].page_content
            out_text = os.path.splitext(pdf_file)[0] + '.txt'
            out_path = os.path.join(out_dir, out_text)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Parsed {pdf_path} -> {out_path}")
        except Exception as e:
            print(f"ERROR: Could not parse {pdf_path}. Reason: {e}")

# --- STEP 2: Chunk text files ---
def chunk_parsed_text_files(parsed_dir, chunks_dir, chunk_size=1000, chunk_overlap=100):
    txt_files = [f for f in os.listdir(parsed_dir) if f.endswith('.txt')]
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    for txt_file in txt_files:
        txt_path = os.path.join(parsed_dir, txt_file)
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            docs = [text]
            splits = splitter.create_documents(docs)
            for i, chunk in enumerate(splits):
                chunk_name = f'{os.path.splitext(txt_file)[0]}_chunk{i+1}.txt'
                chunk_path = os.path.join(chunks_dir, chunk_name)
                with open(chunk_path, 'w', encoding='utf-8') as cf:
                    cf.write(chunk.page_content)
            print(f'Chunked {txt_file}: created {len(splits)} chunks.')
        except Exception as e:
            print(f"ERROR: Could not chunk {txt_file}. Reason: {e}")

# --- STEP 3: Prepare docs for embedding ---
def load_all_chunks(chunks_dir):
    chunk_files = [f for f in os.listdir(chunks_dir) if f.endswith('.txt')]
    docs = []
    for chunk_file in chunk_files:
        chunk_path = os.path.join(chunks_dir, chunk_file)
        loader = TextLoader(chunk_path)
        doc = loader.load()
        # Add metadata for traceability
        for d in doc:
            d.metadata['chunk_file'] = chunk_file
        docs.extend(doc)
    print(f"Loaded {len(docs)} chunks for embedding.")
    return docs

# --- STEP 4: Create embeddings, save to folder, build vector store ---
def build_vectorstore_and_save_embeddings(docs, embeddings_dir):
    embedding_model = AzureOpenAIEmbeddings(
        api_key=ILIAD_API_KEY,
        azure_endpoint=ILIAD_URL_BASE,
        openai_api_version=API_VERSION,
    )
    # Compute and save each embedding
    all_embeddings = []
    for i, doc in enumerate(docs):
        emb = embedding_model.embed_documents([doc.page_content])[0]  # returns list; get first
        emb_file = os.path.join(
            embeddings_dir, f"{doc.metadata.get('chunk_file', f'doc_{i+1}.txt')}.json")
        with open(emb_file, 'w', encoding='utf-8') as ef:
            json.dump({'embedding': emb, 'chunk_file': doc.metadata.get('chunk_file'), 'content': doc.page_content}, ef)
        all_embeddings.append((doc, emb))
    print(f"Saved {len(docs)} embeddings to {embeddings_dir}")
    # Reconstruct vector store
    vector_store = InMemoryVectorStore(embedding_model)
    # Add all docs (embedding will be computed again internally, if needed)
    _ = vector_store.add_documents(documents=docs)
    print("Embeddings loaded into vector store.")
    return vector_store

# --- STEP 5: RAG Q&A with Iliad chatbot ---
def ask_rag_question(question, vector_store, llm_k=3):
    llm = AzureChatOpenAI(
        api_key=ILIAD_API_KEY,
        azure_endpoint=ILIAD_URL_BASE,
        openai_api_version=API_VERSION,
        azure_deployment=DEPLOYMENT,
    )
    retrieved_docs = vector_store.similarity_search(question, k=llm_k)
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    system_message_content = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:
    """
    prompt = ChatPromptTemplate.from_messages([
        ('system', system_message_content),
    ])
    messages = prompt.invoke({"question": question, "context": docs_content})
    response = llm.invoke(messages)
    print('Q:', question)
    print('A:', response.content)

# --- MAIN PIPELINE EXECUTION ---
if __name__ == '__main__':
    # 1. PDF -> Text
    parse_pdfs_to_text(pdf_dir, parsed_dir)
    # 2. Text -> Chunks
    chunk_parsed_text_files(parsed_dir, chunks_dir)
    # 3. Chunks -> LangChain Docs
    docs = load_all_chunks(chunks_dir)
    # 4. Embeddings + Vector Store + Save Embeddings Locally
    vector_store = build_vectorstore_and_save_embeddings(docs, embeddings_dir)
    # 5. RAG Q&A (example)
    sample_question = "What does the Job Aid for Statistical Analysis Plan v4.0 say about validation?"
    ask_rag_question(sample_question, vector_store, llm_k=3)
