from random import randint as rand
import re
from bs4 import BeautifulSoup

APPS = [('Steam', 'gaming'),('Blackboard LMS','productive'),('Tetr.io','procrastination')]
def get_form_log():
    data_list = []
    data_valid = {'productive':0,'gaming':0,'procrastination':0}
    for i in range(5):
        r_int = rand(1,3)
        app_name, app_category = APPS[r_int-1]
        hours = rand(1,5)
        minutes = rand(1,59)
        data_list.append(
            {'app_name':app_name,
             'category':app_category,
             'hours': hours,
             'minutes': minutes,
             'mood':'🔁'}
        )
        data_valid[app_category] += hours
    return data_list, data_valid

def extract_hours(soup):
    val_prod = soup.find('div', class_='productive-hours-value').text.strip()[:-1]
    val_g = soup.find('div', class_='gaming-hours-value').text.strip()[:-1]
    val_proc = soup.find('div', class_='proc-hours-value').text.strip()[:-1]
    if not val_prod or not val_g or not val_proc:
        return 0,0,0
    else:
        return int(val_proc),int(val_g),int(val_prod)
    

def test_logging_with_validation(client_1):
    d_list, d_valid = get_form_log()
    for form in d_list:
        log_r = client_1.post('/log-activity', data=form)
        assert log_r.status_code == 200, f'Expected response 200, got {log_r.status_code}'
    
    
    analytics = client_1.get('/analytics-home')
    assert b'recent-list' in analytics.data
    
    share_r = client_1.get('/share')
    parser = BeautifulSoup(share_r.data,'html.parser')
    hours_proc,hours_g,hours_prod = extract_hours(parser)
    total = d_valid['productive']+d_valid['procrastination']+d_valid['gaming']
    ratio_prod = int(d_valid['productive']/total*100)
    ratio_g = int(d_valid['gaming']/total*100)
    ratio_proc = int(d_valid['procrastination']/total*100)

    assert ratio_prod == hours_prod
    assert ratio_proc == hours_proc
    assert ratio_g == hours_g

    download = client_1.get('/download-receipt')
    assert download.status_code == 200
    assert download.headers['Content-Type'] == 'application/pdf'

def test_sharing_request(client_1,client_2):
    client_1.get('share')




