import csv
import re

processed_schedule = {}
dept_to_division = {}
path_to_project = "PATH TO PROJECT FROM ROOT"
path = f"{path_to_project}/Output/total_merged_QC_schedule.csv"
with open(path, 'r') as merged_schedule:
    csv_reader = csv.reader(merged_schedule)
    next(csv_reader)
    for row in csv_reader:
        # "Academic Year","Year","Term","Level","Division","Department","Code","Title","Status","Query Code","Credits"
        academic_year = row[0]
        year = row[1]
        term = row[2]
        level = row[3]
        division = row[4]
        dept = row[5]
        dept_to_division[dept] = division
        section_code = row[6]
        title = row[7]
        status = row[8]
        query_code = row[9]
        credit_hours = float(row[10])
        if not bool(processed_schedule.get(query_code)):
            processed_schedule[query_code] = {}
            processed_schedule[query_code]["term"] = set()
            processed_schedule[query_code]["title"] = title
            processed_schedule[query_code]["status"] = status
            processed_schedule[query_code]["level"] = {"most_credits": level}
            processed_schedule[query_code]["dept"] = {"most_credits": dept}
        processed_schedule[query_code]["term"].add(term + " " + year)
        if not bool(processed_schedule[query_code]["level"].get(level)):
            processed_schedule[query_code]["level"][level] = 0
        processed_schedule[query_code]["level"][level] += credit_hours
        data = processed_schedule[query_code]["level"]
        if data[data["most_credits"]] < data[level]:
            processed_schedule[query_code]["level"]["most_credits"] = level
        if not bool(processed_schedule[query_code]["dept"].get(dept)):
            processed_schedule[query_code]["dept"][dept] = 0
        processed_schedule[query_code]["dept"][dept] += credit_hours
        data = processed_schedule[query_code]["dept"]
        if data[data["most_credits"]] < data[dept]:
            processed_schedule[query_code]["dept"]["most_credits"] = dept

output = []
header_row = ["Academic Year","Title","Employment Status","Level","Department","Division","Semester","Year","Query Code"]
output.append(header_row)
for query_code, data in processed_schedule.items():
    for term in data["term"]:
        semester, year = term.split(" ")
        dept = data["dept"]["most_credits"]
        level = data["level"]["most_credits"]
        row = [query_code[0:6],data["title"],data["status"],level,dept,dept_to_division[dept],semester,year,query_code]
        output.append(row)


file_name = f'{path_to_project}/Output/faculty_roster.csv'
with open(file_name, 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(output)





