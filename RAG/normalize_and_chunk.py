import json
import os
import re
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configuration
# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data", "Indian-Law-Penal-Code-Json")
OUTPUT_DIR = os.path.join(BASE_DIR, "RAG", "cleaned_corpus")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# File to Act Mapping
# Note: Years are hardcoded based on common knowledge of these acts. 
# If exact years are in the text, we could extract them, but this is safer for now.
ACT_MAPPING = {
    "ipc.json": {"act": "Indian Penal Code", "year": 1860},
    "crpc.json": {"act": "Code of Criminal Procedure", "year": 1973},
    "iea.json": {"act": "Indian Evidence Act", "year": 1872},
    "cpc.json": {"act": "Code of Civil Procedure", "year": 1908},
    "MVA.json": {"act": "Motor Vehicles Act", "year": 1988},
    "hma.json": {"act": "Hindu Marriage Act", "year": 1955},
    "ida.json": {"act": "Industrial Disputes Act", "year": 1947},
    "nia.json": {"act": "Negotiable Instruments Act", "year": 1881}
}

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000, # Approx 700 tokens (assuming ~4 chars/token)
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

def normalize_entry(entry: Dict[str, Any], act_info: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes a single entry from the raw JSON."""
    
    # Handle variations in keys
    section_num = entry.get("Section") or entry.get("section") or ""
    section_title = entry.get("section_title") or ""
    section_desc = entry.get("section_desc") or ""
    
    # Construct meaningful text
    # We combine title and desc to ensure semantic completeness
    full_text = f"Section {section_num}: {section_title}\n{section_desc}"
    
    return {
        "act": act_info["act"],
        "year": act_info["year"],
        "section": str(section_num),
        "section_title": section_title,
        "text": full_text,
        "source": "CivicTech-India"
    }

def process_file(filename: str):
    if filename not in ACT_MAPPING:
        print(f"Skipping {filename} (No mapping defined)")
        return

    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading {filename}")
            return

    act_info = ACT_MAPPING[filename]
    chunks = []
    
    print(f"Processing {act_info['act']}...")

    for i, entry in enumerate(raw_data):
        normalized = normalize_entry(entry, act_info)
        
        # Chunking Logic
        # If text is small enough, keep as one chunk
        # If too large, split
        
        # Simple heuristic: 1 char ~ 0.25 tokens. 700 tokens ~ 2800 chars. 
        # Using 3000 chars as a safe upper bound for splitting.
        
        if len(normalized["text"]) > 3000:
            split_texts = text_splitter.split_text(normalized["text"])
            for j, split_text in enumerate(split_texts):
                chunk = normalized.copy()
                chunk["text"] = split_text
                chunk["chunk_id"] = f"{act_info['act'].replace(' ', '')}_{normalized['section']}_{i}_{j}"
                chunks.append(chunk)
        else:
            chunk = normalized.copy()
            chunk["chunk_id"] = f"{act_info['act'].replace(' ', '')}_{normalized['section']}_{i}_0"
            chunks.append(chunk)

    # Save cleaned file
    output_filename = filename.replace(".json", "_cleaned.json")
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(chunks)} chunks to {output_filename}")

def main():
    files = os.listdir(DATA_DIR)
    for f in files:
        if f.endswith(".json"):
            process_file(f)

if __name__ == "__main__":
    main()
