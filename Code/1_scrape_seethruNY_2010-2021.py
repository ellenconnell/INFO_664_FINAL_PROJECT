import requests
import json
import csv
import requests
from bs4 import BeautifulSoup

total_page_count = 180
page_range = range(total_page_count)
path_to_project = "PATH TO PROJECT FROM ROOT"

#dictionary developed to match pay year to the academic year
ay_dictionary = {
        '2010': 'AY0910',
        '2011': 'AY1011',
        '2012': 'AY1112',
        '2013': 'AY1213',
        '2014': 'AY1314',
        '2015': 'AY1415',
        '2016': 'AY1516',
        '2017': 'AY1617',
        '2018': 'AY1718',
        '2019': 'AY1819',
        '2020': 'AY1920',
        '2021': 'AY2021'
}

# the headers are taken from network requests made to SeeThrough NY webpage.
# headers are accessed from the Network of Chrome dev tools and expire after 24 hrs.
# the dictionary below has expired 

headers = {
        'User-Agent': 'Mozilla/5.0',
        'authority' : 'www.seethroughny.net',
        'accept' : 'application/json',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-platform': 'macOS',
        'origin': 'https://www.seethroughny.net',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.seethroughny.net/payrolls',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'cookie': '_ga=GA1.2.423450844.1636910173; __ss_tk=202111%7C6191445d610e7c33a4017cf3; CONCRETE5=8ef3eec346be5aab17eb25222b6eaa62; __ss=1638321244541; __ss_referrer=https%3A//www.seethroughny.net/payrolls; _gid=GA1.2.2106698636.1638321245'
}

url = 'https://www.seethroughny.net/tools/required/reports/payroll?action=get'
csv_rows = []
for page_number in page_range:
    # these are the url encoded parameters taken from the Network tab relevant to the SeeThroughNY endpoint
    payload = f'PayYear%5B%5D=2020&PayYear%5B%5D=2010&PayYear%5B%5D=2011&PayYear%5B%5D=2012&PayYear%5B%5D=2013&PayYear%5B%5D=2014&PayYear%5B%5D=2015&PayYear%5B%5D=2016&PayYear%5B%5D=2017&PayYear%5B%5D=2018&PayYear%5B%5D=2019&PayYear%5B%5D=2021&SubAgencyName%5B%5D=Queens+College&SubAgencyName%5B%5D=Queens+College+(Adjunct)&SortBy=YTDPay+DESC&current_page={page_number}&result_id=0&url=%2Ftools%2Frequired%2Freports%2Fpayroll%3Faction%3Dget&nav_request=0'
    r_results = requests.post(url,data=payload, headers=headers)
    print("Request to page number ",page_number,"/",total_page_count," had an HTTP response code ", r_results.status_code)
    data = r_results.text
    split_response = data.split('<br />\n')
    response_json = split_response[-1]
    html = json.loads(response_json)['html']
    soup = BeautifulSoup(html, features="html.parser")
    rows = soup.findAll("tr")
    parsed_data = {}
    for row in rows:
        if "resultRow" in row.get("id"):
            id = row.get("id").replace("resultRow","")
            parsed_data[id] = row.text.strip().split("\n")
        elif "expandRow" in row.get("id"):
            id = row.get("id").replace("expandRow","")
            values = row.findAll("div",{"class":"col-xs-6"})
            data = map(lambda val: val.text,values)
            parsed_data[id] += list(data)
            prof_name = re.sub(r'[\'.\-\s]','',parsed_data[id][0])
            professor_name_first_initial_search = re.search(r'^(.*,[A-Za-z]{3}?)',prof_name)
            if professor_name_first_initial_search == None:
                professor_name_first_initial = prof_name
            else:
                professor_name_first_initial = professor_name_first_initial_search.group(0)
            name_year_code = ay_dictionary[parsed_data[id][7]] + professor_name_first_initial
            parsed_data[id].append(name_year_code)
    csv_rows += parsed_data.values()

keys = []
dupes = []
# checked for duplicate faculty listings in the case that professors appear on the adjunct payroll (for summer instruction)
for row in csv_rows:
    if row[-1] not in keys:
        keys.append(row[-1])
    else:
        dupes.append(row[-1])
# selects the entry that corresponds to the higher salary value if faculty is paid from more than one source with assumption that the higher salary reflects primary position
output = []
dup_rows ={}
for row in csv_rows:
        code = row[-1]
        if code in dupes:
            if dup_rows.get(code) == None:
                dup_rows[code] = row
            else:
                saved_row = dup_rows[code]
                saved_salary = int(re.sub(r'[$,]','',saved_row[2]))
                current_salary = int(re.sub(r'[$,]','',row[2]))
                if saved_salary < current_salary:
                    dup_rows[code] = current_salary
        else:
            output.append(row)

output += list(dup_rows.values())

file_name = f'{path_to_project}/Titles/seethroughny_QueensCollege_titles.csv'
with open(file_name, 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(output)






