with open('D2.txt', 'r') as fs, open('D2_processed.txt', 'w') as ft:
    for line in fs:
        line = line.replace("\t", "")
        line=line.replace(" ", ",")
        ft.write(line)
with open('D2 (1).txt', 'r') as fs, open('D2_1_processed.txt', 'w') as ft:
    for line in fs:
        line = line.replace("\t", "")
        line=line.replace(" ", ",")
        ft.write(line)

with open('A.txt', 'r') as fs1, open('D2_processed.txt', 'r') as fs2, open('D2_1_processed.txt', 'r') as fs3, open('features.txt', 'w') as ft:
    for line in fs1:
        ft.write(line)
    for line in fs2:
        ft.write(line)
    for line in fs3:
        ft.write(line)