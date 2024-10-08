
from src.helper import load_pdf_file,text_split,download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
import os
from pinecone.grpc  import PineconeGRPC as Pinecone
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
extracted_data = load_pdf_file(data = "data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

pc = Pinecone(api_key = PINECONE_API_KEY)

index_name = "comptachatbot"
pc.create_index(
    name=index_name,
    dimension= 384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

docsearch = PineconeVectorStore.from_documents(
    documents = text_chunks,
    index_name=index_name,
    embedding=embeddings
    )
