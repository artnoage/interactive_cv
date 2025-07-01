#!/usr/bin/env python3
"""
Test agent for metadata extraction using LangChain and OpenRouter
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


# First, let's test the connection
def test_openrouter_connection():
    """Test if we can connect to OpenRouter"""
    try:
        # Initialize LLM with OpenRouter
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="google/gemini-2.5-flash",
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Interactive CV Metadata Extractor",
            }
        )
        
        # Simple test prompt
        print("Testing OpenRouter connection with Gemini 2.5 Flash...")
        response = llm.invoke("Say 'Hello! Connection successful!' if you can read this.")
        print(f"✅ Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


class ChronicleMetadata(BaseModel):
    """Schema for chronicle note metadata"""
    date: str = Field(description="Date of the note")
    mood: Optional[str] = Field(description="Mood if mentioned")
    work_focus: List[str] = Field(description="Main activities or projects worked on")
    technical_breakthroughs: List[Dict[str, str]] = Field(
        description="List of insights with context and impact"
    )
    problems_solved: List[Dict[str, str]] = Field(
        description="Problems encountered and their solutions"
    )
    tools_used: List[str] = Field(description="Technologies and tools mentioned")
    project_progress: Dict[str, str] = Field(
        description="Status updates for each project"
    )
    key_learnings: List[str] = Field(description="Important things learned")
    future_tasks: List[str] = Field(description="Planned next steps")


class MetadataExtractor:
    def __init__(self, model_name: str = "google/gemini-2.5-flash"):
        """
        Initialize the metadata extractor with OpenRouter
        Using Gemini 2.5 Flash for fast, efficient extraction
        """
        
        # Check for API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        # OpenRouter setup with Gemini
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model=model_name,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Interactive CV Metadata Extractor",
            },
            temperature=0.1,  # Low temperature for consistent extraction
        )
        
        # Set up the output parser
        self.parser = PydanticOutputParser(pydantic_object=ChronicleMetadata)
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at extracting structured metadata from daily notes. Extract the key information according to the provided schema."),
            ("human", "Extract metadata from this daily note:\n\n{content}\n\n{format_instructions}")
        ])
        
        # Create the chain
        self.chain = self.prompt | self.llm | self.parser

    def extract_metadata(self, content: str) -> ChronicleMetadata:
        """Extract metadata from a chronicle note"""
        try:
            result = self.chain.invoke({
                "content": content,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            raise

    def process_file(self, file_path: Path) -> Dict:
        """Process a single markdown file"""
        print(f"Processing: {file_path}")
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        metadata = self.extract_metadata(content)
        
        # Convert to dict and add file info
        result = metadata.dict()
        result['file_path'] = str(file_path)
        result['processed_at'] = datetime.now().isoformat()
        
        return result


def test_single_file():
    """Test the extractor on a single chronicle note"""
    
    # Initialize the extractor
    print("Initializing metadata extractor with Gemini 2.5 Flash...")
    extractor = MetadataExtractor()
    
    # Test on a recent daily note
    test_file = Path("chronicle/Daily Notes/2025-06-30.md")
    
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    # Extract metadata
    print(f"\nExtracting metadata from: {test_file}")
    metadata = extractor.process_file(test_file)
    
    # Pretty print the results
    print("\n=== Extracted Metadata ===")
    print(json.dumps(metadata, indent=2))
    
    # Save to file
    output_file = "test_metadata_output.json"
    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"\nMetadata saved to: {output_file}")


def test_multiple_files():
    """Test on multiple chronicle notes"""
    
    extractor = MetadataExtractor()
    chronicle_dir = Path("chronicle/Daily Notes")
    
    all_metadata = []
    
    # Process all markdown files
    for file_path in chronicle_dir.glob("*.md"):
        if "test" not in file_path.name:  # Skip test files
            try:
                metadata = extractor.process_file(file_path)
                all_metadata.append(metadata)
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
    
    # Save all metadata
    with open("chronicle_metadata_test.json", 'w') as f:
        json.dump(all_metadata, f, indent=2)
    
    print(f"\nProcessed {len(all_metadata)} files")
    print("Results saved to: chronicle_metadata_test.json")


if __name__ == "__main__":
    # First test the connection
    print("🔌 Testing OpenRouter connection...")
    if not test_openrouter_connection():
        print("\n❌ Please check your OPENROUTER_API_KEY in .env file")
        exit(1)
    
    print("\n✅ Connection successful! Now testing metadata extraction...")
    print("-" * 50)
    
    # Run the metadata extraction test
    test_single_file()
    
    # Uncomment to test multiple files
    # test_multiple_files()