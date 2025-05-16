from random import randint as rand
import re
from bs4 import BeautifulSoup

APPS = [
        ('chrome', 'productive'),
        ('steam', 'gaming'),
        ('tiktok', 'social_media')
    ]
def get_form_log():
    data_list = []
    data_valid = {'productive':0,'gaming':0,'social_media':0}
    for i in range(5):
        r_int = rand(1,3)
        app_name, app_category = APPS[r_int-1]
        hours = rand(1,5)
        minutes = rand(1,1)
        form = {'application':app_name,
             'category':app_category,
             'hours': hours,
             'minutes': minutes,
             'mood':'😊'}
        data_list.append(form)
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
    

def get_ratio(valid:dict):
    total = valid['productive']+valid['social_media']+valid['gaming']
    return int(valid['productive']/total*100),int(valid['gaming']/total*100),int(valid['social_media']/total*100)

def test_logging_with_validation(client_1):
    d_list, d_valid = get_form_log()
    for form in d_list:
        log_load_r = client_1.get('/log-activity')
        log_r = client_1.post('/log-activity', data=form, follow_redirects=True)
        assert log_r.status_code == 200, f'Expected response 200, got {log_r.status_code}'
    
    
    analytics = client_1.get('/analytics-home')
    assert b'recent-list' in analytics.data
    
    share_r = client_1.get('/share')
    parser = BeautifulSoup(share_r.data,'html.parser')
    hours_proc,hours_g,hours_prod = extract_hours(parser)
    ratio_prod,ratio_g,ratio_proc = get_ratio(d_valid)

    tolerance = 2
    assert abs(ratio_prod - hours_prod) <= tolerance, f"Expected {ratio_prod}% (±{tolerance}), got {hours_prod}%"
    assert abs(ratio_proc - hours_proc) <= tolerance, f"Expected {ratio_proc}% (±{tolerance}), got {hours_proc}%"
    assert abs(ratio_g - hours_g) <= tolerance, f"Expected {ratio_g}% (±{tolerance}), got {hours_g}%"

    #this needs an API call to validate, which requires implementation of the API.
    #download = client_1.post('/download-receipt')
    #assert download.status_code == 200
    #assert download.headers['Content-Type'] == 'application/pdf'

def find_receipt_id(soup):
    receipt_id = None
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string and "receiptId" in script.string:
            match = re.search(r'receiptId\s*=\s*[\'"](\d+)[\'"]', script.string)
            if match:
                receipt_id =  match.group(1)
    return receipt_id
            

def test_sharing_request(client_1,client_2):
    #Its complicated but it works.
    first_forms, first_valid = get_form_log()
    second_forms, second_valid = get_form_log()
    for form in first_forms:
        client_1.post('/log-activity',data=form)
    for form in second_forms:
        client_2.post('/log-activity',data=form)

    c1_share = client_1.get('/share')   
    c2_share = client_2.get('/share')

    c1_soup = BeautifulSoup(c1_share.data, 'html.parser')
    c2_soup = BeautifulSoup(c2_share.data, 'html.parser')

    c1_receipt = find_receipt_id(c1_soup)
    c2_receipt = find_receipt_id(c2_soup)

    share_1 = client_1.post(f'/share/send/{c1_receipt}/2')
    share_2 = client_2.post(f'/share/send/{c2_receipt}/1')

    assert share_1.status_code == 302
    assert share_2.status_code == 302

    req_1 = BeautifulSoup(client_1.get('/share/requests').data,'html.parser')
    req_2 = BeautifulSoup(client_2.get('/share/requests').data,'html.parser')

    acc_1 = req_1.find('form', action=re.compile(r'/share/requests/accept/\d+')).get('action')
    acc_2 = req_2.find('form', action=re.compile(r'/share/requests/accept/\d+')).get('action')

    res_acc_1 = client_1.post(acc_1)
    res_acc_2 = client_2.post(acc_2)

    assert res_acc_1.status_code == 302
    assert res_acc_2.status_code == 302






    




