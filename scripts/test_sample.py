import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Health Check
print("=" * 50)
print("TEST 1: Health Check")
print("=" * 50)
response = requests.get(f"{BASE_URL}/api/v1/health")
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}\n")

# Test 2: Summarize Medical Report
print("=" * 50)
print("TEST 2: Summarize Medical Report")
print("=" * 50)
medical_report = """
Patient: Sarah Johnson, Age: 62
Chief Complaint: Persistent headache and dizziness for 3 days
Vital Signs: BP 160/100 mmHg, HR 88 bpm, Temp 98.4°F
Physical Exam: Alert and oriented, no focal neurological deficits
Labs: Blood glucose 180 mg/dL, HbA1c 8.2%
Assessment: Hypertension, poorly controlled Type 2 Diabetes
Plan: Started on Lisinopril 10mg daily, adjusted Metformin to 1000mg BID
Follow-up in 2 weeks
"""

payload = {
    "text": medical_report.strip(),
    "temperature": 0.7,
    "max_length": 150
}

response = requests.post(f"{BASE_URL}/api/v1/summarize", json=payload)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Summary: {result['summary']}")
    print(f"Input Length: {result['input_length']}")
    print(f"Summary Length: {result['summary_length']}\n")
else:
    print(f"Error: {response.text}\n")

# Test 3: Analyze with Question
print("=" * 50)
print("TEST 3: Question Answering")
print("=" * 50)
payload = {
    "text": medical_report.strip(),
    "question": "What medications were prescribed to the patient?"
}

response = requests.post(f"{BASE_URL}/api/v1/analyze", json=payload)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}\n")
else:
    print(f"Error: {response.text}\n")