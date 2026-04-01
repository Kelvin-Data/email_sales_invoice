import pygsheets
import dotenv
import os

dotenv.load_dotenv()

def get_gsheet_data():
  path = os.getenv("GSHEET_PATH")
  gc = pygsheets.authorize(service_account_file = path)
  sh = gc.open('Invoice_form')
  wk = sh.worksheet_by_title('Form_responses')
  content = wk.get_all_values(include_tailing_empty=False)
  data_rows = content[1:]  
  processed_data = []
  
  for row in data_rows:
    if any(cell.strip() for cell in row):
      customer_name = row[1]  
      customer_email = row[3]  
      processed_data.append({
          "customer_name": customer_name,
          "customer_email": customer_email,
          "full_row": row  
            })
  return processed_data
