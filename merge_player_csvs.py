import csv


alphabet = ["b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o","p", "q", "r", "s", "t", "u", "v", "w", "y", "z"] 
    talbes = ["_stats_pitcher.csv", "_stats_nonpitcher.csv", "_bios.csv", "_employment.csv"]
    for name in tables:
        filename = "letter_" + letter + name
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            next(reader, None)
            with open("letter_a" + name, mode='a') as outfile:
                writer = csv.writer(outfile)
                for line in reader:
                    if len(line) >=1:
                        writer.writerow(line)
