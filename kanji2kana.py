# code written by chatgpt 3.5, with modifications
# v0.1.0
# &copy; <admin@p1m.org>, 2024
# license: refer to openai's licensing terms

# initial query:
# i have a text file as an input and need to calc the number of occurrences of a particular character by line, and output a file that contains the same number of lines as input but each line contains the number of occurrences of that char on that line. write in python

# important additional query:
# modify the script so that it used args.character to break the line into fragments, and then calculate the number of kana characters within each fragment. modify the output file to become a json file of the following format:
# 
# {
#     "kanji": [
#         {
#             readings: [
#                 NUMBER OF KANAS IN FRAGMENT 1,
#                 NUMBER OF KANAS IN FRAMENT 2,
#                 ...
#             ]
#         },
#         ...
#     ]
# }

# one more important additional query:
# also write line that will print min, max, mean, and median number of occurrences. average occurrences first within line, then across lines. e.g., if a line has three readings, average the number of kana for this line, and when you have point estimates for each line, average overall. print only the overall numbers.

import argparse
import json
import re
import statistics

def count_kana_occurrences(input_file, output_file, delimiter):
    kana_count_list = []
    min_within_line = []
    max_within_line = []
    mean_within_line = []
    median_within_line = []
    kana_counts_within_lines = 0

    with open(input_file, 'r') as f_in:
        for line in f_in:
            fragments = line.strip().split(delimiter)
            kana_counts = [len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF]', fragment)) for fragment in fragments]
            if len(kana_counts) == 1 and kana_counts[0] == 0:
                continue
            kana_count_list.append({'readings': kana_counts})
            kana_counts_within_lines += len(kana_counts)
            min_within_line.append(min(kana_counts))
            max_within_line.append(max(kana_counts))
            mean_within_line.append(statistics.mean(kana_counts))
            median_within_line.append(statistics.median(kana_counts))

    with open(output_file, 'w') as f_out:
        json.dump({'kanji': kana_count_list}, f_out, indent=4)    

    kana_counts_across_lines = len(kana_count_list)
    min_across_lines = min(min_within_line)
    max_across_lines = max(max_within_line)
    mean_across_lines = statistics.mean(mean_within_line)
    median_across_lines = statistics.median(median_within_line)

    print("Lines containing kanas:", kana_counts_across_lines)
    print("Total number of readings:", kana_counts_within_lines)
    print("Overall minimum occurrences, weighted within line:", min_across_lines)
    print("Overall maximum occurrences, weighted within line:", max_across_lines)
    print("Overall mean occurrences, weighted within line:", mean_across_lines)
    print("Overall median occurrences, weighted within line:", median_across_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count occurrences of kana characters in each fragment of a text file.')
    parser.add_argument('input_file', type=str, help='Path to the input text file')
    parser.add_argument('output_file', type=str, help='Path to the output JSON file')
    parser.add_argument('--delimiter', type=str, default='\u3001', help='Delimiter to split each line into fragments')

    args = parser.parse_args()

    count_kana_occurrences(args.input_file, args.output_file, args.delimiter)

