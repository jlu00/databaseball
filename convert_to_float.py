import csv

def do_conversion_pitcher():
    with open("all_stats_pitcher.csv") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        with open("ints_all_stats_pitcher.csv", mode='a') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                for line in reader:
                    line_list = []
                    for value_index in range(len(line)):
                        if value_index == 0:
                            line_list.append(line[value_index])
                        elif value_index == 1:
                            line_list.append(line[value_index])
                        elif value_index == 2:
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                three_highest = find_three_highest(values_list)
                                total_three_highest = 0
                                for val in three_highest:
                                    if val:
                                        total_three_highest += val
                                avg_three_highest = total_three_highest/3.0
                                line_list.append(avg_three_highest)
                            else:
                                line_list.append("")
                        elif value_index == 3:
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                three_lowest_list = find_three_lowest(values_list)
                                avg = find_avg(three_lowest_list)
                                line_list.append(avg)
                            else:
                                line_list.append("")
                        elif value_index == 4:
                            total = 0
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                #print("values_list", values_list)
                                for val in values_list:
                                    total += float(val)
                                line_list.append(total)
                            else:
                                line_list.append("")
                        elif value_index == 5:
                            total = 0
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                for val in values_list:
                                    total += float(val)
                                line_list.append(total)
                            else:
                                line_list.append("")
                        elif value_index == 6:
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                three_lowest = find_three_lowest(values_list)
                                total_three_lowest = 0
                                for val in three_lowest:
                                    if val:
                                        total_three_lowest += float(val)
                                avg_three_lowest = total_three_lowest/3.0
                                line_list.append(avg_three_lowest)
                            else:
                                line_list.append("")
                        elif value_index == 7:
                            total = 0
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                for val in values_list:
                                    if val != "":
                                        total += float(val) 
                                avg_total = total/len(line[value_index])
                                line_list.append(avg_total)
                            else:
                                line_list.append("")
                        elif value_index == 8:
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                three_highest = find_three_highest(values_list)
                                total_three_highest = 0
                                for val in three_highest:
                                    if val:
                                        total_three_highest += val
                                avg_three_highest = total_three_highest/3.0
                                line_list.append(avg_three_highest)
                            else:
                                line_list.append("")
                        elif value_index == 9:
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                three_lowest = find_three_lowest(values_list)
                                total_three_lowest = 0
                                for val in three_lowest:
                                    if val:
                                        total_three_lowest += float(val)
                                avg_three_lowest = total_three_lowest/3.0
                                line_list.append(avg_three_lowest)
                            else:
                                line_list.append("")
                    writer.writerow(line_list)
def do_conversion_nonpitcher():
    with open("all_stats_nonpitcher.csv") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        with open("ints_all_stats_nonpitcher.csv", mode='a') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                for line in reader:
                    line_list = []
                    for value_index in range(len(line)):
                        if value_index == 0:
                            line_list.append(line[value_index])
                        elif value_index == 1:
                            line_list.append(line[value_index])
                        elif value_index == 6:
                            line_list.append(line[value_index])
                        elif value_index == 9:
                            line_list.append(line[value_index])
                        else:
                            values_list = line[value_index].split("|")
                            non_empty = False
                            for val in values_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                three_highest = find_three_highest(values_list)
                                total_three_highest = 0
                                for val in three_highest:
                                    if val:
                                        total_three_highest += val
                                avg_three_highest = total_three_highest/3.0
                                line_list.append(avg_three_highest)
                            else:
                                line_list.append("")
                    writer.writerow(line_list)
                    
def find_three_highest(value_list):
    three_highest = [0, 0, 0]
    max_val1 = None
    max_val2 = None
    max_val3 = None
    if len(value_list) >= 3:
        non_empty = False
        for val in value_list:
            if val != "":
                non_empty = True
        if non_empty:
            max_val1 = find_max(value_list)
            try:
                value_list.remove(str(max_val1))
            except:
                pass
            try:
                value_list.remove(str(int(max_val1)))
            except:
                pass
            try:
                value_list.remove("0"+str(max_val1))
            except:
                pass
            try:
                value_list.remove(str(max_val2)+"0")
            except:
                pass
            if len(value_list) >=2:
                non_empty = False
                for val in value_list:
                    if val != "":
                        non_empty = True
                if non_empty:
                    max_val2 = find_max(value_list)
                    if len(value_list) >= 1:
                        non_empty = False
                        for val in value_list:
                            if val != "":
                                non_empty = True
                        if non_empty:
                            try:
                                value_list.remove(str(max_val2))
                            except:
                                pass
                            try:
                                value_list.remove(str(int(max_val2)))
                            except:
                                pass
                            try:
                                value_list.remove("0"+str(max_val2))
                            except:
                                pass
                            try:
                                value_list.remove(str(max_val2)+"0")
                            except:
                                pass
                            non_empty = False
                            for val in value_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                max_val3 = find_max(value_list)
    three_highest[0] = max_val1
    three_highest[1] = max_val2
    three_highest[2] = max_val3
        
    return three_highest

def find_max(value_list):
    for val in value_list:
        if val != "":
            max_value = float(value_list[value_list.index(val)])
            break
    for v in value_list:
        if v != "":
            if float(v) > max_value:
                max_value = float(v)
    return max_value


def find_three_lowest(value_list):
    three_lowest = [0, 0, 0]
    min_val1 = None
    min_val2 = None
    min_val3 = None
    if len(value_list) >= 3:
        non_empty = False
        for val in value_list:
            if val != "":
                non_empty = True
        if non_empty:
            min_val1 = find_min(value_list)
            try:
                value_list.remove(str(min_val1))
            except:
                pass
            try:
                value_list.remove(str(int(min_val1)))
            except:
                pass
            try:
                value_list.remove("0"+str(min_val1))
            except:
                pass
            try:
                value_list.remove(str(min_val2)+"0")
            except:
                pass
            if len(value_list) >=2:
                non_empty = False
                for val in value_list:
                    if val != "":
                        non_empty = True
                if non_empty:
                    min_val2 = find_min(value_list)
                    if len(value_list) >= 1:
                        non_empty = False
                        for val in value_list:
                            if val != "":
                                non_empty = True
                        if non_empty:
                            try:
                                value_list.remove(str(min_val2))
                            except:
                                pass
                            try:
                                value_list.remove(str(int(min_val2)))
                            except:
                                pass
                            try:
                                value_list.remove("0"+str(min_val2))
                            except:
                                pass
                            try:
                                value_list.remove(str(min_val2)+"0")
                            except:
                                pass
                            non_empty = False
                            for val in value_list:
                                if val != "":
                                    non_empty = True
                            if non_empty:
                                min_val3 = find_min(value_list)
    three_lowest[0] = min_val1
    three_lowest[1] = min_val2
    three_lowest[2] = min_val3

    return three_lowest

def find_min(value_list):
    for val in value_list:
        if val != "":
            min_val_float = float(value_list[value_list.index(val)])
            min_val_str = value_list[value_list.index(val)]
            break
    for v in value_list:
        if v != "":
            if float(v) < min_val_float:
                min_val_float = float(v)
                min_val_str = v
    return min_val_str

def find_avg(values_list):
    total = 0
    for val in values_list:
        if val:
            total += float(val)
    avg = total/len(values_list)
    return avg