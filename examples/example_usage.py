"""Example usage of the Medical Report Analysis API."""

import requests

# API base URL
BASE_URL = "http://localhost:8000/api/v1"


def check_health():
    """Check API health status."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())


def summarize_text():
    """Example: Summarize medical report text."""
    medical_report = """
    Patient: John Doe, Age: 45, Gender: Male
    
    Chief Complaint: Persistent cough and fever for 5 days
    
    History of Present Illness:
    Patient presents with a 5-day history of productive cough with yellow sputum,
    fever up to 101°F, and mild shortness of breath. No chest pain reported.
    
    Physical Examination:
    - Temperature: 101°F
    - Blood Pressure: 130/85 mmHg
    - Heart Rate: 88 bpm
    - Respiratory Rate: 20/min
    - Lung auscultation reveals crackles in the right lower lobe
    
    Assessment:
    Community-acquired pneumonia, right lower lobe
    
    Plan:
    1. Chest X-ray ordered
    2. Started on Amoxicillin-Clavulanate 875mg BID for 7 days
    3. Advised rest and increased fluid intake
    4. Follow-up in 3 days or sooner if symptoms worsen
    """
    
    payload = {
        "text": medical_report,
        "temperature": 0.7
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print("\nSummarization Result:")
    print(response.json())


def analyze_report():
    """Example: Answer specific question about medical report."""
    medical_report = """
    Patient presents with Type 2 Diabetes Mellitus.
    Current medications: Metformin 1000mg twice daily, Lisinopril 10mg once daily.
    Recent HbA1c: 7.2%
    Blood pressure: 135/82 mmHg
    Recommendation: Continue current medications, lifestyle modifications advised.
    """
    
    payload = {
        "text": medical_report,
        "question": "What medications is the patient currently taking?"
    }
    
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    print("\nAnalysis Result:")
    print(response.json())


def upload_document():
    """Example: Upload and process a medical document."""
    # Create a sample text file
    with open("sample_report.txt", "w") as f:
        f.write("""
        Medical Report
        
        Patient: Jane Smith
        Date: 2024-01-15
        
        Diagnosis: Hypertension
        Treatment: Prescribed Amlodipine 5mg daily
        Follow-up: 4 weeks
        """)
    
    with open("sample_report.txt", "rb") as f:
        files = {"file": ("sample_report.txt", f, "text/plain")}
        response = requests.post(f"{BASE_URL}/upload/document", files=files)
    
    print("\nDocument Upload Result:")
    print(response.json())


def rag_summarize():
    """Example: Use RAG to summarize large document."""
    payload = {
        "query": "Provide a comprehensive summary of the patient's condition",
        "top_k": 5
    }
    
    response = requests.post(f"{BASE_URL}/rag/summarize", json=payload)
    print("\nRAG Summarization Result:")
    print(response.json())


def rag_question():
    """Example: Use RAG to answer question about large document."""
    payload = {
        "question": "What are the main findings and recommendations?",
        "top_k": 5
    }
    
    response = requests.post(f"{BASE_URL}/rag/question", json=payload)
    print("\nRAG Question Answering Result:")
    print(response.json())


if __name__ == "__main__":
    print("Medical Report Analysis API - Example Usage\n")
    print("=" * 60)
    
    try:
        # Check if API is running
        check_health()
        
        # Example 1: Text summarization
        print("\n" + "=" * 60)
        print("Example 1: Text Summarization")
        print("=" * 60)
        summarize_text()
        
        # Example 2: Question answering
        print("\n" + "=" * 60)
        print("Example 2: Question Answering")
        print("=" * 60)
        analyze_report()
        
        # Example 3: Document upload
        print("\n" + "=" * 60)
        print("Example 3: Document Upload")
        print("=" * 60)
        upload_document()
        
        # Example 4: RAG summarization
        print("\n" + "=" * 60)
        print("Example 4: RAG Summarization")
        print("=" * 60)
        rag_summarize()
        
        # Example 5: RAG question answering
        print("\n" + "=" * 60)
        print("Example 5: RAG Question Answering")
        print("=" * 60)
        rag_question()
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API. Make sure the server is running.")
        print("Start the server with: python run.py")
    except Exception as e:
        print(f"\nError: {e}")

