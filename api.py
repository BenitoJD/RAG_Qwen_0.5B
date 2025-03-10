from fastapi import FastAPI, HTTPException
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from typing import List, Dict, Any, Optional


class Item(BaseModel):
    query: str

class SearchResult(BaseModel):
    id: int
    path: Optional[str] = None
    content: str

class SearchResponse(BaseModel):
    results: List[SearchResult]

class AskResponse(BaseModel):
    context: List[SearchResult]
    answer: str

def setup_embeddings():
    model_name = "sentence-transformers/msmarco-bert-base-dot-v5"
    
    if torch.cuda.is_available():
        model_kwargs = {'device': 'cuda'}
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        model_kwargs = {'device': 'mps'}
    else:
        model_kwargs = {'device': 'cpu'}
    
    encode_kwargs = {'normalize_embeddings': True}
    
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def setup_llm():
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            device_map="auto" if torch.cuda.is_available() else "cpu",
            trust_remote_code=True,
        )
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise RuntimeError(f"Failed to load model {model_id}: {str(e)}")

def setup_qdrant():
    try:
        client = QdrantClient(path="qdrant/")
        collection_name = "MyCollection"
        return Qdrant(client, collection_name, hf)
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        raise RuntimeError(f"Failed to connect to Qdrant: {str(e)}")

hf = setup_embeddings()
tokenizer, model = setup_llm()
qdrant = setup_qdrant()

app = FastAPI(title="Document Search and QA API")

@app.get("/")
async def root():
    return {"message": "Hello World", "status": "API is running"}

@app.post("/search", response_model=List[SearchResult])
def search(item: Item):
    try:
        query = item.query
        search_result = qdrant.similarity_search(
            query=query, k=10
        )
        
        list_res = []
        for i, res in enumerate(search_result):
            list_res.append({
                "id": i, 
                "path": res.metadata.get("path"), 
                "content": res.page_content
            })
        return list_res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.post("/ask_localai", response_model=AskResponse)
async def ask_localai(item: Item):
    try:
        query = item.query
        search_result = qdrant.similarity_search(
            query=query, k=10
        )
        
        list_res = []
        context = ""
        
        for i, res in enumerate(search_result):
            doc_text = res.page_content.strip()
            context += f"Document [{i}]:\n{doc_text}\n\n"
            list_res.append({
                "id": i, 
                "path": res.metadata.get("path"), 
                "content": doc_text
            })
        
        system_message = (
            "Answer the user's question using only the provided documents. "
            "Always cite your sources by referencing document IDs in square brackets [ID]. "
            "For example, [0], [1], etc. Use multiple citations as needed."
        )
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {query}"},
        ]
        
        try:
            # For debugging
            print(f"Processing query: {query}")
            print(f"Found {len(list_res)} context documents")
            
            formatted_prompt = f"""<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
Documents:
{context}

Question: {query}<|im_end|>
<|im_start|>assistant
"""
            
            print(f"Formatted prompt created, length: {len(formatted_prompt)}")
            
            inputs = tokenizer(
                formatted_prompt,
                return_tensors="pt",
                padding=True,
                return_attention_mask=True
            )
            
            input_ids = inputs["input_ids"].to(model.device)
            attention_mask = inputs["attention_mask"].to(model.device)
            
            print(f"Input shape: {input_ids.shape}")
            
            terminators = [
                tokenizer.eos_token_id,
                tokenizer.convert_tokens_to_ids("<|endoftext|>")
            ]
            
            outputs = model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_new_tokens=8192,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id,
            )
            
            print(f"Generation completed, output shape: {outputs.shape}")
            
            generated_text = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
            print(f"Decoded text: {generated_text[:100]}...")
            
            if not generated_text.strip():
                print("Warning: Generated empty response")
                generated_text = "I couldn't find a specific answer to your question in the provided documents."
            
            return {"context": list_res, "answer": generated_text}
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error during generation: {str(e)}\n{error_details}")
            raise HTTPException(status_code=500, detail=f"Model inference error: {str(e)}")
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Processing error: {str(e)}\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")