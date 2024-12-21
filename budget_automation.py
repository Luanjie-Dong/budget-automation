
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
    
    
    output_list = {} 
    output_list2 =[]
    for months in month:
        if months != "" and months.upper() == monthh:
            difference = month[months][1] - month[months][0]
            output_list2.append(("","","","",""))
            output_list2.append(("",months.upper(),"Total Earned","Total Spent","Difference"))
            output_list2.append(("","",round(month[months][1],2),round(month[months][0],2),round(difference,2)))
            
            for individuals in month[months][2]:
                output_list[("",individuals[0][:2],individuals[0][2:].upper(),round(individuals[1][0],2),round(individuals[1][1],2))] = []
                for ss in individuals[1][2]:
                    sentence = ""
                    for ss2 in ss[4:]:
                        if ss2 != "":
                            sentence += ss2
                            sentence += " "
                    datee = ss[0]
                    details = sentence
                    if "." in ss[2]:
                        amount = float(ss[2][1:])
                        output_list[("",individuals[0][:2],individuals[0][2:].upper(),round(individuals[1][0],2),round(individuals[1][1],2))] +=[("","",datee,amount,"","","","",details)]
                    else:
                        amount = float(ss[3][1:])
                        output_list[("",individuals[0][:2],individuals[0][2:].upper(),round(individuals[1][0],2),round(individuals[1][1],2))] += [("","",datee,"",amount,"","","",details)]
                    
    
    sort_output = {} #sort ascending 
    for i in range(32):
        if i < 10:
            for output in output_list:
                if output[1] == "0"+str(i):
                    sort_output[output] = output_list[output]
        else:
            for output in output_list:
                if output[1] == str(i):
                    sort_output[output] = output_list[output]

    compare = start_date #configure which date to add(inclusive_). If I want to add dates after 7 Dec, compare = 7
    final_output = []
    
    for outputs in sort_output:
        if outputs[1][0] == "0":
            if int(outputs[1][1]) >= compare:
                dating = outputs[1]+" "+outputs[2]
                final_output.append(("",dating,outputs[3],outputs[4]))
                for outputs2 in sort_output[outputs]:
                    final_output.append(outputs2)
        else:
            if int(outputs[1]) >= compare:
                dating = outputs[1]+" "+outputs[2]
                final_output.append(("",dating,outputs[3],outputs[4]))
                for outputs2 in sort_output[outputs]:
                    final_output.append(outputs2)
    final_output += output_list2
    return final_output[::-1]


#parameters to edit!!!!!!!
month_to_add = "JUN"                    #edit the intended month
csv_file = "2024/june.csv"                    #edit the intended downloaded csv database
google_sheet = "2024 Monthly Tracker "  #edit the intended google spreadsheet
google_worksheet = "Jun 2024"               #edit the intended google spreadsheet's worksheet
start_row = 47                         #edit the intended start row
year = "2024"
start_date = 0

def test(csv_file,month_to_add,start_date,year):
    test = budgeting(csv_file,month_to_add,start_date,year) #to test the programme 
    for test1 in test:
        print(test1)


def importing(google_sheet,google_worksheet,csv_file,month_to_add,start_date,year):
    sa = gspread.service_account(filename="/Users/luanjiechen/Desktop/Personal Projects/Budget_python/ss.json/service_account.json")
    sh = sa.open(google_sheet)
    wks = sh.worksheet(google_worksheet) 
    rows = budgeting(csv_file,month_to_add,start_date,year) 

    for row in rows:
        wks.insert_row(row,start_row) 
        time.sleep(2)
    
test(csv_file,month_to_add,start_date,year)
importing(google_sheet,google_worksheet,csv_file,month_to_add,start_date,year)


