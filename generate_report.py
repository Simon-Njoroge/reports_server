import json
import os
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


REPORT_SERVER_URL = "http://localhost:5001"

def find_excel_file():
    current_dir = os.getcwd()
    print(f"Looking in: {current_dir}")
    
    files = os.listdir(current_dir)
    excel_files = [f for f in files if f.endswith(('.xlsx', '.xls'))]
    
    if excel_files:
        print(f"Found Excel file: {excel_files[0]}")
        return excel_files[0]
    
    parent_dir = os.path.dirname(current_dir)
    if os.path.exists(parent_dir):
        parent_files = os.listdir(parent_dir)
        parent_excel = [f for f in parent_files if f.endswith(('.xlsx', '.xls'))]
        if parent_excel:
            print(f"Found Excel file in parent directory: {parent_excel[0]}")
            return os.path.join(parent_dir, parent_excel[0])
    
    return None

FILE_PATH = find_excel_file()
if FILE_PATH is None:
    FILE_PATH = "09 Employee HR Records.xlsx"
    print(f"Using fallback filename: {FILE_PATH}")

def check_server():
    try:
        req = Request(f"{REPORT_SERVER_URL}/health", method='GET')
        with urlopen(req, timeout=5) as response:
            if response.status == 200:
                return True
            return False
    except (URLError, HTTPError, ConnectionError):
        return False

def generate_report():
    if not os.path.exists(FILE_PATH):
        print(f"Error: File '{FILE_PATH}' not found")
        print(f"Current directory: {os.getcwd()}")
        print("\nFiles in current directory:")
        for file in os.listdir('.'):
            print(f"  - {file}")
        
        excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
        if excel_files:
            print(f"\nFound Excel files: {', '.join(excel_files)}")
        return
    
    if not check_server():
        print("Report server is not running. Please start it first:")
        print("   python app.py")
        return
    
    print("Report server is running")
    
    abs_path = os.path.abspath(FILE_PATH)
    print(f"Using file: {abs_path}")
    
    payload = {
        "filePath": abs_path,
        "eventTitle": "Employee HR Report",
        "reportTitle": "Employee HR Records",
        "includeSummary": True
    }
    
    json_data = json.dumps(payload).encode('utf-8')
    
    print(f"Generating HR report from: {FILE_PATH}")
    
    try:
        req = Request(
            f"{REPORT_SERVER_URL}/api/generate-report-from-file",
            data=json_data,
            method='POST'
        )
        req.add_header('Content-Type', 'application/json')
        req.add_header('Content-Length', str(len(json_data)))
        
        with urlopen(req, timeout=60) as response:
            pdf_data = response.read()
            
            filename = f"hr_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, 'wb') as f:
                f.write(pdf_data)
            
            file_size = len(pdf_data) / 1024
            print(f"Report generated successfully!")
            print(f"Saved as: {filename}")
            print(f"File size: {file_size:.2f} KB")
            
            try:
                if sys.platform == 'win32':
                    os.startfile(filename)
                elif sys.platform == 'darwin':
                    os.system(f'open "{filename}"')
                else:
                    os.system(f'xdg-open "{filename}"')
            except:
                pass
                
    except HTTPError as e:
        print(f"HTTP Error: {e.code}")
        try:
            error_data = json.loads(e.read().decode('utf-8'))
            print(f"   Message: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"   Response: {e.read().decode('utf-8')[:200]}")
    except URLError as e:
        print(f"Connection Error: {e.reason}")
        print("   Make sure the server is running on http://localhost:5001")
    except Exception as e:
        print(f"Error: {e}")

def generate_test_report():
    employees = [
        {
            "employee_id": "EMP-1001",
            "full_name": "Richard Hernandez",
            "gender": "Male",
            "department": "Sales",
            "job_title": "Sales Representative",
            "hire_date": "2023-02-12",
            "annual_salary": 85100,
            "performance_rating": "2",
            "satisfaction_score": "3",
            "employment_status": "Active"
        },
        {
            "employee_id": "EMP-1002",
            "full_name": "Richard Harris",
            "gender": "Male",
            "department": "Operations",
            "job_title": "Warehouse Supervisor",
            "hire_date": "2020-11-04",
            "annual_salary": 54900,
            "performance_rating": "5",
            "satisfaction_score": "6",
            "employment_status": "Active"
        },
        {
            "employee_id": "EMP-1003",
            "full_name": "Timothy Rodriguez",
            "gender": "Male",
            "department": "Sales",
            "job_title": "Sales Representative",
            "hire_date": "2017-10-06",
            "annual_salary": 80200,
            "performance_rating": "4",
            "satisfaction_score": "5",
            "employment_status": "Active"
        },
        {
            "employee_id": "EMP-1004",
            "full_name": "Amanda Young",
            "gender": "Female",
            "department": "Marketing",
            "job_title": "Marketing Coordinator",
            "hire_date": "2018-03-09",
            "annual_salary": 63300,
            "performance_rating": "4",
            "satisfaction_score": "6",
            "employment_status": "Active"
        }
    ]
    
    if not check_server():
        print("Report server is not running. Please start it first:")
        print("   python app.py")
        return
    
    payload = {
        "employees": employees,
        "eventTitle": "Employee HR Report",
        "reportTitle": "Employee HR Records (Test)",
        "includeSummary": True
    }
    
    json_data = json.dumps(payload).encode('utf-8')
    
    print("Generating test HR report from JSON data...")
    
    try:
        req = Request(
            f"{REPORT_SERVER_URL}/api/generate-report",
            data=json_data,
            method='POST'
        )
        req.add_header('Content-Type', 'application/json')
        req.add_header('Content-Length', str(len(json_data)))
        
        with urlopen(req, timeout=30) as response:
            pdf_data = response.read()
            
            filename = f"test_hr_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, 'wb') as f:
                f.write(pdf_data)
            
            file_size = len(pdf_data) / 1024
            print(f"Test report generated: {filename}")
            print(f"File size: {file_size:.2f} KB")
            
    except HTTPError as e:
        print(f"HTTP Error: {e.code}")
        try:
            error_data = json.loads(e.read().decode('utf-8'))
            print(f"   Message: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"   Response: {e.read().decode('utf-8')[:200]}")
    except Exception as e:
        print(f"Error: {e}")

def preview_file():
    try:
        if not os.path.exists(FILE_PATH):
            excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
            if excel_files:
                file_to_preview = excel_files[0]
                print(f"\nPreviewing Excel file: {file_to_preview}")
            else:
                print(f"\nNo Excel files found in current directory")
                return
        else:
            file_to_preview = FILE_PATH
        
        print(f"\nFile: {file_to_preview}")
        print("-" * 80)
        print("Fields: Employee ID, Full Name, Gender, Department, Job Title, Hire Date, Annual Salary, Performance Rating, Satisfaction Score, Employment Status")
        print("-" * 80)
        
    except Exception as e:
        print(f"Could not preview file: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Employee HR Report Generator")
    print("=" * 60)
    
    print(f"\nWorking directory: {os.getcwd()}")
    
    preview_file()
    
    if FILE_PATH and os.path.exists(FILE_PATH):
        print(f"\nUsing Excel file: {FILE_PATH}")
    else:
        print(f"\nExcel file '{FILE_PATH}' not found")
        excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
        if excel_files:
            print(f"Found these Excel files: {', '.join(excel_files)}")
            print("The script will use the first one found")
    
    print("\nChoose an option:")
    print("1. Generate HR report from Excel file")
    print("2. Generate test HR report from JSON (4 sample employees)")
    print("3. Both")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        generate_report()
    elif choice == "2":
        generate_test_report()
    elif choice == "3":
        generate_test_report()
        print("\n" + "=" * 60)
        generate_report()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Running default (Excel)...")
        generate_report()