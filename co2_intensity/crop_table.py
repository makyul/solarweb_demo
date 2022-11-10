"""
Crop table to reduce previous years.

"""

import csv

WORLD_CO2_INTENSITY = 425.23486328125
first_row = ["Afghanistan", "AFG", "2000", "255.3191375732422"]
last_row = ["Zimbabwe", "279.02789306640625"]

prev_row = first_row


with open("carbon-intensity-electricity.csv", "r") as f_r:
    with open("carbon-intensity-electricity-01-09-2022_cropped.csv", "w", newline="") as f_w:

        csv_orig = csv.reader(f_r)
        csv_cropped = csv.writer(f_w, delimiter=",")

        for row in csv_orig:
            if row[0] != prev_row[0]:
                if float(prev_row[3]) == 0.0:
                    cropped_row = [prev_row[0], WORLD_CO2_INTENSITY]
                else:
                    cropped_row = [prev_row[0], float(prev_row[3])]
                csv_cropped.writerow(cropped_row)

            prev_row = row

        csv_cropped.writerow(last_row)
