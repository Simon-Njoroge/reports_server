import requests
import json
from datetime import datetime

# Sample payment data from your CSV
payments = [
    {
        "id": "784b51b8-1355-4ada-89a3-5b5ccd3b3f16",
        "reference": "ws_CO_19062026211235287713479387",
        "customerName": "DANCAN MURIMI Mwangi",
        "customerEmail": "farmernjuki@gmail.com",
        "customerPhone": "254713479387",
        "eventTitle": "Dad Chella",
        "amount": 2000.00,
        "currency": "KES",
        "status": "successful",
        "provider": "mpesa",
        "paidAt": "2026-06-19T18:12:47.402Z",
        "createdAt": "2026-06-19T18:12:29.353Z"
    },
    {
        "id": "344bbbde-4f21-467b-8b27-a28b0a35aa53",
        "reference": "ws_CO_20062026091325825718869040",
        "customerName": "victor kariuki",
        "customerEmail": "kikimwangi@gmail.com",
        "customerPhone": "254718869040",
        "eventTitle": "Dad Chella",
        "amount": 2000.00,
        "currency": "KES",
        "status": "successful",
        "provider": "mpesa",
        "paidAt": "2026-06-20T06:13:39.996Z",
        "createdAt": "2026-06-20T06:13:24.442Z"
    },
    {
        "id": "9b607d9b-f459-4a4e-a0c0-a9e20052c0fe",
        "reference": "ws_CO_19062026182649413721921052",
        "customerName": "peter lopee",
        "customerEmail": "peterlopee@gmail.com",
        "customerPhone": "254721921052",
        "eventTitle": "Dad Chella",
        "amount": 4000.00,
        "currency": "KES",
        "status": "successful",
        "provider": "mpesa",
        "paidAt": "2026-06-19T15:27:01.561Z",
        "createdAt": "2026-06-19T15:26:48.102Z"
    },
    {
        "id": "89e1afea-f80c-43b5-8ac8-96cb6e157549",
        "reference": "ws_CO_19062026213015753716285915",
        "customerName": "Mercy Wanja",
        "customerEmail": "rechykahugu@gmail.com",
        "customerPhone": "254716285915",
        "eventTitle": "Dad Chella",
        "amount": 3000.00,
        "currency": "KES",
        "status": "successful",
        "provider": "mpesa",
        "paidAt": "2026-06-19T18:30:29.181Z",
        "createdAt": "2026-06-19T18:30:14.810Z"
    }
]

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5001/health")
        print(f"✅ Health: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_generate_report():
    """Test report generation"""
    print("\n📄 Testing report generation...")
    try:
        url = "http://localhost:5001/api/generate-report"
        
        payload = {
            "payments": payments,
            "eventTitle": "Dad Chella",
            "reportTitle": "Payment Summary Report",
            "includeSummary": True
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            filename = f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Report generated successfully!")
            print(f"📁 Saved as: {filename}")
            print(f"📊 Contains: {len(payments)} payments")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Testing Report Server")
    print("=" * 60)
    test_health()
    test_generate_report()
    print("\n✨ Done!")