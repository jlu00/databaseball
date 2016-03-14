import csv

def do_conversion_pitcher():
    '''
    Convets certain pitcher statistics to the form they need to be in
    '''
    with open("all_stats_pitcher.csv") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        with open("ints_all_stats_pitcher.csv", mode='a') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                for line in reader:
                    line_list = []
                    for value_index in range(len(line)):
                        if value_index == 0 or value_index == 1:
                            line_list.append(line[value_index])
                        elif value_index == 2 or value_index == 8:
                            values_list = line[value_index].split("|")
                            if is_non_empty(values_list):
                                three_highest = find_three_highest(values_list)
                                avg_three_highest = find_avg(three_highest)
                                line_list.append(avg_three_highest)
                            else:
                                line_list.append("")
                        elif value_index == 3 or value_index == 6 or value_index == 9:
                            values_list = line[value_index].split("|")
                            if is_non_empty(values_list):
                                three_lowest_list = find_three_lowest(values_list)
                                avg = find_avg(three_lowest_list)
                                line_list.append(avg)
                            else:
                                line_list.append("")
                        elif value_index == 4 or value_index == 5:
                            values_list = line[value_index].split("|")
                            if is_non_empty(values_list):
                                for val in values_list:
                                    total += float(val)
                                line_list.append(total)
                            else:
                                line_list.append("")
                        elif value_index == 7:
                            values_list = line[value_index].split("|")
                            if is_non_empty(values_list):
                                avg_total = find_avg(values_list)
                                line_list.append(avg_total)
                            else:
                                line_list.append("")   
                    writer.writerow(line_list)

def do_conversion_nonpitcher():
    '''
    Converts certain nonpitcher statistics to the form they need to be in
    '''
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


def is_non_empty(values_list):
    '''
    Checks if a list of values is non_empty
    '''
    values_list = line[value_index].split("|")
    non_empty = False
    for val in values_list:
        if val != "":
            non_empty = True
            return non_empty
    return non_empty
                    
def find_three_highest(value_list):
    '''
    Finds the three hightest values in a list and returns them
    '''
    three_highest = [0, 0, 0]
    max_val1 = None
    max_val2 = None
    max_val3 = None
    if len(value_list) >= 3: 
        max_val1 = find_max(value_list)
        if is_non_empty(value_list):
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
                if is_non_empty(value_list):
                    max_val2 = find_max(value_list)
                    if len(value_list) >= 1:
                        if is_non_empty(values_list):
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
                            if is_non_empty(value_list):
                                max_val3 = find_min(value_list)
    three_highest[0] = max_val1
    three_highest[1] = max_val2
    three_highest[2] = max_val3 
    return three_highest

def find_max(value_list):
    '''
    Finds the maximum value in a list and returns it 
    '''
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
    '''
    Finds the three lowest values in a list and returns them
    '''
    three_lowest = [0, 0, 0]
    min_val1 = None
    min_val2 = None
    min_val3 = None
    if len(value_list) >= 3: 
        min_val1 = find_min(value_list)
        if is_non_empty(value_list):
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
                if is_non_empty(value_list):
                    min_val2 = find_min(value_list)
                    if len(value_list) >= 1:
                        if is_non_empty(values_list):
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
                            if is_non_empty(value_list):
                                min_val3 = find_min(value_list)

    three_lowest[0] = min_val1
    three_lowest[1] = min_val2
    three_lowest[2] = min_val3
    return three_lowest

def find_min(value_list):
    '''
    Finds the minimum value in a list and returns it 
    '''
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
    '''
    Finds the average of a list of values and returns it 
    '''
    total = 0
    for val in values_list:
        if val:
            total += float(val)
    avg = total/len(values_list)
    return avg