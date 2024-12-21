import gspread
import time


def budgeting(filename,monthh,start_date,year):
    items ={} #filter the CSV data 
    with open(filename,'r') as input_file:
        for lines in input_file:
            lines = lines.rstrip("\n")
            columns = lines.split(",")
            if year in columns[0]:
                date = ""
                for check in columns:
                    if 'SI NG' in check:
                        check = check.split("SI NG")
                        date = check[1][1:].lower()
                
                if date == "" or date == ' ':
                    date2 = columns[0].split(" ")
                    new_date = (date2[0]+date2[1]).lower()
                    if new_date not in items:
                        if '.' in columns[2]:
                            items[new_date] = [float(columns[2]),0,[columns]]
                        elif "." in columns[3]:
                            items[new_date] = [0,float(columns[3]),[columns]]

                    else:
                        if '.' in columns[2]:
                            items[new_date][0] += float(columns[2])
                            items[new_date][2] += [columns]
                        elif "." in columns[3]:
                            items[new_date][1] += float(columns[3])
                            items[new_date][2] += [columns]
                else:
                    if date not in items:
                        if '.' in columns[2]:
                            items[date] = [float(columns[2]),0,[columns]]
                        elif "." in columns[3]:
                            items[date] = [0,float(columns[3]),[columns]]
                    else:
                        if '.' in columns[2]:
                            items[date][0] += float(columns[2])
                            items[date][2] += [columns]
                        elif "." in columns[3]:
                            items[date][1] += float(columns[3])
                            items[date][2] += [columns]
    
    month = {} #categorise based on the month
    for dates1 in items:
        if dates1[2:] not in month:
            month[dates1[2:]] = [items[dates1][0],items[dates1][1],[(dates1,items[dates1])]]
        else:
            month[dates1[2:]][0] += items[dates1][0]
            month[dates1[2:]][1] += items[dates1][1]
            month[dates1[2:]][2] += [(dates1,items[dates1])]
    
    overall_month = []

    for months2 in month:
        difference = month[months2][1] - month[months2][0]
        overall_month.append((months2.upper(),round(month[months2][0],2),round(month[months2][1],2),round(difference,2)))
    
    for each in overall_month:
        print(each)


    #parameters to edit!!!!!!!
month_to_add = "JUL"                    #edit the intended month
csv_file = "overall1.csv"                    #edit the intended downloaded csv database
google_sheet = "2023 Monthly Tracker "  #edit the intended google spreadsheet
google_worksheet = "Test"   #edit the intended google spreadsheet's worksheet
start_row = 2                          #edit the intended start row
year = "2023"
start_date = 0

budgeting(csv_file,month_to_add,start_date,year)