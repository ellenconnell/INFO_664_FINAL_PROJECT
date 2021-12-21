import glob
import csv
import re

path_to_project = "PATH TO PROJECT FROM ROOT"

# dictionary to map of course subject to deptartment and division
course_code_dictionary = {
'ACCT': {'dept': 'Accounting', 'div': 'Social Sciences'},
 'ACE': {'dept': 'Adult Collegiate Education',
         'div': 'Academic Support Center'},
 'AFST': {'dept': 'Africana Studies', 'div': 'Social Sciences'},
 'AMST': {'dept': 'American Studies', 'div': 'Arts and Humanities '},
 'ANTH': {'dept': 'Anthropology', 'div': 'Social Sciences'},
 'ARAB': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
          'div': 'Arts and Humanities '},
 'ARTH': {'dept': 'Art', 'div': 'Arts and Humanities '},
 'ARTS': {'dept': 'Art', 'div': 'Arts and Humanities '},
 'ASTR': {'dept': 'Physics', 'div': 'Mathematics and the Natural Sciences'},
 'BALA': {'dept': 'Business & Liberal Arts', 'div': 'Social Sciences'},
 'BASS': {'dept': 'Sociology', 'div': 'Social Sciences'},
 'BIOCH': {'dept': 'Chemistry & Biochemistry',
           'div': 'Mathematics and the Natural Sciences'},
 'BIOL': {'dept': 'Biology', 'div': 'Mathematics and the Natural Sciences'},
 'BUS': {'dept': 'Business & Liberal Arts', 'div': 'Social Science'},
 'CESL': {'dept': 'College English as a Second Language',
          'div': 'Academic Support Center'},
 'CHEM': {'dept': 'Chemistry & Biochemistry',
          'div': 'Mathematics and the Natural Sciences'},
 'CHIN': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
          'div': 'Arts and Humanities '},
 'CLAS': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
          'div': 'Arts and Humanities '},
 'CMLIT': {'dept': 'Comparative Literature', 'div': 'Arts and Humanities '},
 'CO-OP': {'dept': 'Cooperative Education', 'div': 'Student Support Services'},
 'CSCI': {'dept': 'Computer Science',
          'div': 'Mathematics and the Natural Sciences'},
 'Code': {'dept': 'Department', 'div': 'Division'},
 'DANCE': {'dept': 'Drama, Theatre & Dance', 'div': 'Arts and Humanities '},
 'DRAM': {'dept': 'Drama, Theatre & Dance', 'div': 'Arts and Humanities '},
 'EAST': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
          'div': 'Arts and Humanities '},
 'ECON': {'dept': 'Economics', 'div': 'Social Sciences'},
 'ECP': {'dept': 'Educational & Community Programs', 'div': 'Education '},
 'ECPCE': {'dept': 'Elementary & Early Childhood Education',
           'div': 'Education '},
 'ECPEL': {'dept': 'Educational & Community Programs', 'div': 'Education '},
 'ECPSE': {'dept': 'Elementary & Early Childhood Education',
           'div': 'Education '},
 'ECPSP': {'dept': 'Educational & Community Programs', 'div': 'Education '},
 'EECE': {'dept': 'Elementary & Early Childhood Education',
          'div': 'Education '},
 'ENGL': {'dept': 'English', 'div': 'Arts and Humanities '},
 'ENSCI': {'dept': 'School of Earth & Environmental Sciences',
           'div': 'Mathematics and the Natural Sciences'},
 'EURO': {'dept': 'European Languages & Literatures',
          'div': 'Arts and Humanities '},
 'FNES': {'dept': 'Family, Nutrition & Exercise Sciences',
          'div': 'Mathematics and the Natural Sciences'},
 'FREN': {'dept': 'European Languages & Literatures',
          'div': 'Arts and Humanities '},
 'GEOL': {'dept': 'School of Earth & Environmental Sciences',
          'div': 'Mathematics and the Natural Sciences'},
 'GERM': {'dept': 'European Languages & Literatures',
          'div': 'Arts and Humanities '},
 'GRKMD': {'dept': 'Byzantine & Modern Greek Studies',
           'div': 'Arts and Humanities '},
 'GRKST': {'dept': 'Byzantine & Modern Greek Studies',
           'div': 'Arts and Humanities '},
 'HEBRW': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
           'div': 'Arts and Humanities '},
 'HIST': {'dept': 'History', 'div': 'Social Sciences'},
 'HMNS': {'dept': 'Honors in the Mathematical & Natural Sciences',
          'div': 'Mathematics and the Natural Sciences'},
 'HNRS': {'dept': 'Honors (Macaulay)', 'div': 'Macaulay Honors College'},
 'HSS': {'dept': 'Honors in the Social Sciences', 'div': 'Social Sciences'},
 'HTH': {'dept': 'Honors in the Humanities', 'div': 'Arts and Humanities '},
 'IRST': {'dept': 'Irish Studies', 'div': 'Social Sciences'},
 'ITAL': {'dept': 'European Languages & Literatures',
          'div': 'Arts and Humanities '},
 'ITAST': {'dept': 'Italian-American Studies', 'div': 'Social Sciences'},
 'JOURN': {'dept': 'Journalism', 'div': 'Arts and Humanities '},
 'JPNS': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
          'div': 'Arts and Humanities '},
 'KOR': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
         'div': 'Arts and Humanities '},
 'LABST': {'dept': 'Labor Studies', 'div': 'Social Sciences'},
 'LALS' : {'dept': 'Latin American and Latino Studies', 'div': 'Social Sciences'},
 'LATIN': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
           'div': 'Arts and Humanities '},
 'LBLST': {'dept': 'Liberal Studies', 'div': 'Social Sciences'},
 'LBSCI': {'dept': 'Graduate School of Library & Information Studies',
           'div': 'Social Sciences'},
 'LCD': {'dept': 'Linguistics & Communication Disorders', 'div': 'Education '},
 'LIBR': {'dept': 'Library', 'div': 'Social Sciences'},
 'MATH': {'dept': 'Mathematics', 'div': 'Mathematics and the Natural Sciences'},
 'MEDST': {'dept': 'Media Studies', 'div': 'Arts and Humanities '},
 'MES': {'dept': 'Classical, Middle Eastern & Asian Languages & Cultures',
         'div': 'Arts and Humanities '},
 'MUSIC': {'dept': 'Music',
           'div': 'Arts and Humanities '},
 'PHIL': {'dept': 'Philosophy', 'div': 'Social Sciences'},
 'PHYS': {'dept': 'Physics', 'div': 'Mathematics and the Natural Sciences'},
 'PORT': {'dept': 'Hispanic Languages and Literatures Department',
          'div': 'Arts and Humanities '},
 'PSCI': {'dept': 'Political Science', 'div': 'Social Sciences'},
 'PSYCH': {'dept': 'Psychology', 'div': 'Mathematics and the Natural Sciences'},
 'RLGST': {'dept': 'Religious Studies', 'div': 'Arts and Humanities '},
 'RM': {'dept': 'Risk Management', 'div': 'Social Sciences'},
 'RUSS': {'dept': 'European Languages & Literatures',
          'div': 'Arts and Humanities '},
 'SEEK': {'dept': 'Search for Education, Elevation & Knowledge', 'div': 'Student Support Services'},
 'SEYS': {'dept': 'Secondary Education & Youth Services', 'div': 'Education '},
 'SEYSL': {'dept': 'Secondary Education & Youth Services', 'div': 'Education '},
 'SOC': {'dept': 'Sociology', 'div': 'Social Sciences'},
 'SPAN': {'dept': 'Hispanic Languages and Literatures',
          'div': 'Arts and Humanities '},
 'SPST': {'dept': 'Special Studies', 'div': 'Social Sciences'},
 'STPER': {'dept': 'Student Personnel Department',
           'div': 'Counseling, Health, & Wellness Center'},
 'URBST': {'dept': 'Urban Studies', 'div': 'Social Sciences'},
 'WLDST': {'dept': 'World Studies', 'div': 'Arts and Humanities '},
 'WOMST': {'dept': "Women's Studies", 'div': 'Social Sciences'},
 'YIDD': {'dept': "Classical, Middle Eastern & Asian Languages & Cultures", 'div': 'Arts and Humanities'},
 'CMAL': {'dept': "Classical, Middle Eastern & Asian Languages & Cultures", 'div': 'Arts and Humanities'},
 'MNSCI': {'dept': "Mathematics", 'div': 'Mathematics and the Natural Sciences'},
 'AACS': {'dept': "Classical, Middle Eastern & Asian Languages & Cultures", 'div': 'Arts and Humanities'},
 'GREEK': {'dept': "Byzantine & Modern Greek Studies", 'div': 'Arts and Humanities'},
 'JAZZ': {'dept': "Aaron Copland School of Music", 'div': 'Arts and Humanities'},
 'EDUCN': {'dept': "Educational & Community Programs", 'div': 'Education'},
 'WGS': {'dept': "Women and Gender Studies", 'div': 'Social Sciences'},
 'JEWST': {'dept': "Jewish Studies", 'div': 'Social Sciences'},
 'DATA': {'dept': "Sociology", 'div': 'Social Sciences'},
 'QNS': {'dept': "Sociology", 'div': 'Social Sciences'},
 'PHOTO': {'dept': "Art", 'div': 'Arts and Humanities'},
 'ELI': {'dept': "English Language Institute", 'div': 'Admin'},
 'MAM': {'dept': "Mathematics", 'div': 'Mathematics and the Natural Sciences'},
 'PERM': {'dept': "ADMIN", 'div': 'ADMIN'},
 'CERT': {'dept': "ADMIN", 'div': 'ADMIN'},
 'CUNBA': {'dept': "ADMIN", 'div': 'ADMIN'}}

#dictionary to match title scraped from SeeThroughNY to a faculty status
faculty_title_to_employment_status = {
  "Instructor":"Title,Status",
  "Lecturer":"Full-time",
  "Adjunct Asst Professo":"Part-time",
  "Adjunct Lecturer":"Part-time",
  "Lect/Doctoral Sch":"Full-time",
  "Assistant Professor":"Full-time",
  "Professor":"Full-time",
  "Asst Professor":"Full-time",
  "Assoc Professor":"Full-time",
  "Instructor":"Full-time",
  "Adjunct Assoc Profess":"Part-time",
  "Distinguished Lecturer":"Full-time",
  "College Asst":"Part-time",
  "Administrative Staff Analyst":"Part-time",
  "Sr Coll Lab Tech":"Part-time",
  "Adj Lect Hry":"Part-time",
  "Higher Educ Officer":"Part-time",
  "Continuing Ed Teacher":"Part-time",
  "He Assoc":"Part-time",
  "Graduate Asst D":"Part-time",
  "Dist Prof":"Full-time",
  "Doc Nta-1":"Part-time",
  "Adjunct Professor":"Part-time",
  "Visiting Asst Profess":"Part-time",
  "Higher Educ Asst":"Part-time",
  "Adj Asst Prof Hry":"Part-time",
  "Visiting Assoc Profes":"Part-time",
  "Adj Assoc Prof Hry":"Part-time",
  "Adjuncy Lecturer":"Part-time",
  "Vice President":"Part-time",
  "Adjunct Assistant Professor":"Part-time",
  "Doc Nta-2":"Part-time",
  "Adj Lecdoc":"Part-time",
  "Custodial Supervisor (Cuny)":"Part-time",
  "Adj Inst Hry":"Part-time",
  "Visiting Prof":"Part-time",
  "Dean":"Part-time",
  "Adj Prof Hry":"Part-time",
  "Athletic Director":"Part-time",
  "Graduate Asst C":"Part-time",
  "Associate Professor":"Full-time",
  "Non-Teaching Adjunct I":"Part-time",
  "Asst Vice President":"Part-time",
  "Coll Lab Tech":"Part-time",
  "Chief College Lab Tec":"Part-time",
  "Cuny Custodial Asst":"Part-time",
  "Assnt Professor-10 Mo":"Full-time",
  "Asst To Heo":"Part-time",
  "Research Support Specialist":"Part-time",
  "Clinical Professor":"Part-time",
  "College Assistant":"Part-time",
  "Cuny Office Assnt":"Part-time",
  "Project Manager":"Part-time",
  "Visiting Lecturer":"Part-time",
  "Adjunct Instructors":"Part-time",
  "Adjunct Coll Lab Tech":"Part-time",
  "It Associate":"Part-time",
  "Adjunct Sr Col Lab Tc":"Part-time",
  "Adjunct Instructor":"Part-time",
  "Adjuct Lecturer":"Part-time",
  "Clinical Assnt In Hs":"Part-time",
  "Doc Nitra 1":"Part-time",
  "Adjunct Associate":"Part-time",
  "It Senior Associate":"Part-time",
  "Program Coordinator":"Part-time",
  "Athletics Director":"Part-time",
  "Cuny Admnv Assnt":"Part-time",
  "Clinical Assnt Pr Hs":"Part-time",
  "Adjunct Intructor":"Part-time",
  "Graduate Assistant":"Part-time",
  "Adjunt Professor":"Part-time",
  "Research Asst":"Part-time",
  "Campus Public Safety Sergeant":"Part-time",
  "Graduate Asst":"Part-time"
}
# dictionary pulled from SeeThrough NY
faculty_year_to_title_dictionary = {}
path = f"{path_to_project}/Titles/seethroughny_QueensCollege_titles.csv"
with open(path, 'r') as schedule_csv:
    csv_reader = csv.reader(schedule_csv)
    for row in csv_reader:
        code = row[-1]
        faculty_year_to_title_dictionary[code] = row[5]
#dictionary created from instructors with no match to the SeeThroughNY scrape due to differences in punctuation, middlie initial
#generated through consulting SeeThrough scrape in Excel
missing_title_hash = {}
path = f"{path_to_project}/Titles/seethroughNY_QueensCollege_missing_titles.csv"
with open(path, 'r') as missing_titles:
    csv_reader = csv.reader(missing_titles)
    for row in csv_reader:
        missing_title_hash[row[0]] = row[1]  

#cleaning and restructuring the course schedule data from one row per section meeting time to summary by section code
#splitting cells to generate new columns for credits and subject code to be mapped to dept and div
#using regex to generate a unique ID to match instructor name with titles dictionaries
path = f"{path_to_project}/Schedule/*.csv"
total_output = []
header_row = ["Academic Year","Year","Term","Level","Division","Department","Section Code","Title","Status","Query Code","Credits"]
total_output.append(header_row)
# iterating over a directory of schedule csv files to be merged and summarized by unique course section code
for fname in glob.glob(path):
    courses_data = {}
    year = re.findall(r"(.{4})\.csv$", fname)[0]
    term = re.findall(r"AllPrograms_(.*)20[0-9]{2}.csv", str(fname))[0]
    if term == "Fall":
        next_year = str(int(year) + 1)
        academic_year = f"AY{year[2:]}{next_year[2:]}"
    elif term == "Spring":
        last_year = str(int(year) - 1)
        academic_year = f"AY{last_year[2:]}{year[2:]}"
    # Iterate over rows of schedule csv
    with open(fname, 'r') as schedule_csv:
        csv_reader = csv.reader(schedule_csv)
        for row in csv_reader:
            # create a unique instructor identifier
            instructor_cleaned = re.sub(r'[\'.\-\s]','',row[6])
            instructor_code = re.search(r'^(.*,[A-Za-z]{3}?)',instructor_cleaned)
            section_code = row[1]
            if instructor_code == None:
                instructor_code = instructor_cleaned
            else:
                instructor_code = instructor_code.group(0)
            if row[0] != "Sec" and instructor_cleaned != ",":
                # breaks out course number, level and credits from single schedule cell
                split_column = re.sub('[(),]','',row[2]).split(" ")
                split_column[1] = " ".join(split_column[0:2])
                course_number = re.findall(r"([0-9]+)",split_column[1])[0]
                course_level = int(course_number[0])
                credits = split_column[-1]
                if course_level in [0,1,2,3,4]:
                    course_level = "Undergraduate"
                elif course_level in [5,6,7,8,9]:
                    course_level = "Graduate"
                # pull department and devision from the department code
                dept_code = split_column[0]
                dept = course_code_dictionary[dept_code]['dept']
                division = course_code_dictionary[dept_code]['div']
                # use title dictionaries to match title to instructor
                query_code = academic_year + instructor_code
                title = faculty_year_to_title_dictionary.get(query_code)
                if title == None:
                    title = missing_title_hash.get(query_code)
                status = faculty_title_to_employment_status.get(title)
                modified_row = [academic_year,year,term,course_level,division,dept,section_code,title,status,query_code]
                if not courses_data.get(section_code):
                  courses_data[section_code] = {}
                courses_data[section_code]["credits"] = credits
                courses_data[section_code][instructor_code] = modified_row
    output = []
    # iterate over dictionary of csv rows to output grouped by section code per term per year
    for key in courses_data.keys():
      instructors = courses_data[key].keys() - ["credits"]
      credits_per_instructor = float(courses_data[key]["credits"])/len(instructors)
      for prof in instructors:
        single_row = courses_data[key][prof]
        single_row.append(credits_per_instructor)
        output.append(single_row)
    total_output += output

file_name = f'{path_to_project}/Output/master_merged_schedule.csv'
with open(file_name, 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(total_output)
