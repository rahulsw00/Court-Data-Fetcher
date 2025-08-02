import time
from django.shortcuts import render
from django.http import JsonResponse
from .models import CourtQuery, CourtResponse
from django.contrib.auth.decorators import login_required  # optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import json


# @login_required  # uncomment if you want to protect the view
def fetch_case_data(request):
    if request.method == 'POST':
        # Get form data
        case_type = request.POST.get('case_type')
        case_number = request.POST.get('case_number')
        year = request.POST.get('filing_year')

        #for testing
        # case_type = request.GET.get('case_type', 'CS(OS)')
        # case_number = request.GET.get('case_number', '1000')
        # year = request.GET.get('year', '2024')
        
        # Log the query
        court_query = CourtQuery.objects.create(
            case_type=case_type,
            case_number=case_number,
            filing_year=year,
            user_ip=get_client_ip(request) 
        )
        
        try:
            url = "https://delhihighcourt.nic.in/app/get-case-type-status"
            options = Options()
            # options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(url)

            # Input search criteria
            driver.find_element(By.ID, "case_number").send_keys(case_number)
            Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)
            Select(driver.find_element(By.ID, "case_year")).select_by_visible_text(year)

            # Handle captcha
            captcha = driver.find_element(By.ID, "captcha-code").text
            driver.find_element(By.ID, "captchaInput").send_keys(captcha)

            # Click search
            driver.find_element(By.ID, "search").click()

            # Wait for results to load
            time.sleep(3) 

            allCases = {}

            try:
                tbody = driver.find_element(By.XPATH, '//*[@id="caseTable"]/tbody')
                rows = tbody.find_elements(By.TAG_NAME, "tr")
                
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    
                    # Skip rows that don't have enough columns
                    if len(cols) < 4:  # Ensure we have at least 4 columns
                        continue
                        
                    try:
                        caseNo = cols[0].text
                        petitionerVsRespondent = cols[2].text.splitlines()
                        
                        # Check if we have enough elements in petitionerVsRespondent
                        if len(petitionerVsRespondent) < 3:
                            petitioner = "N/A"
                            respondent = "N/A"
                        else:
                            petitioner = petitionerVsRespondent[0]
                            respondent = petitionerVsRespondent[2]
                            
                        date_parts = cols[3].text.splitlines()
                        if date_parts: 
                            next_date = date_parts[0].split(":")[1].strip() 
                            last_date = date_parts[1].split(":")[1].strip() 
                            court_no = date_parts[2].split(":")[1].strip()
                        else:
                            next_date = last_date = court_no = "N/A"
                            
                        # Handle order links
                        order_links = cols[1].find_elements(By.TAG_NAME, "a")
                        orderUrl = order_links[1].get_attribute("href") if len(order_links) > 1 else None
                        
                        allOrders = {}
                        if orderUrl:
                            driver.get(orderUrl)
                            time.sleep(1) 
                            try:
                                orderTbody = driver.find_element(By.XPATH, '//*[@id="caseTable"]/tbody')
                                orderRows = orderTbody.find_elements(By.TAG_NAME, "tr")
                                
                                for order_row in orderRows:
                                    orderTableCols = order_row.find_elements(By.TAG_NAME, "td")
                                    if len(orderTableCols) >= 3:
                                        orderNo = orderTableCols[0].text
                                        link_element = orderTableCols[1].find_element(By.TAG_NAME, "a")
                                        allOrders[orderNo] = {
                                            'orderNo': orderNo,
                                            'linkText': link_element.text,
                                            'link': link_element.get_attribute("href"),
                                            'dataOfOrder': orderTableCols[2].text
                                        }
                            except Exception as e:
                                print(f"Error processing orders: {e}")
                            finally:
                                driver.back()
                                time.sleep(1) 
                        
                        allCases[caseNo] = {
                            'status': cols[1].find_element(By.TAG_NAME, "font").text if cols[1].find_elements(By.TAG_NAME, "font") else "N/A",
                            'petitioner': petitioner,
                            'respondent': respondent,
                            'nextDate': next_date,
                            'lastDate': last_date,
                            'courtNo': court_no,
                            'orders': allOrders
                        }
                        
                    except Exception as e:
                        print(f"Error processing row: {e}")
                        continue
                        
            except Exception as e:
                print(f"Major error occurred: {e}")
            finally:
                pass
                driver.quit()

            response_data = {
                'status': 'success',
                'case_type': case_type,
                'case_number': case_number,
                'year': year,
                'data': allCases 
            }
            CourtResponse.objects.create(
                query=court_query,
                is_success=True,
                raw_response=json.dumps(response_data), 
                http_status=200
            )
            
            return JsonResponse(response_data)
        except Exception as e:
            # Log failed response
            CourtResponse.objects.create(
                query=court_query,
                raw_response=str(e),
                http_status=500,
                is_success=False
            )
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def case_search_view(request):
    return render(request, 'myapp/index.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip