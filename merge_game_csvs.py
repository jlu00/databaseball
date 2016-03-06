import csv


alphabet = ["b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o","p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]
#spaced_csv_letters = ["h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "z"]
for letter in alphabet:
    #if letter not in spaced_csv_letters:
        #filename = "letter_" + letter + ".csv"
    #else: 
    filename = "letter_" + letter + "_stats_pitcher.csv"
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader, None)
        with open("letter_a_stats_pitcher.csv", mode='a') as outfile:
            writer = csv.writer(outfile)
            for line in reader:
                if len(line) >=1:
                    writer.writerow(line)
