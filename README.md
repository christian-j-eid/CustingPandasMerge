# CustomPandasMerge
Merging three excel spreadsheet files using Pandas &amp; numpy + openpyxl. Requires custom merging functions to retain a Master Format. Freelance project used by compnay. 

Set EXPLAIN variable to understand results

# Process
Master Spreadsheet (A) has dimension -- (7330, 29)

First merge (B) dimension (281, 20) --> (n, 29) fn Merge1() 


Final, merge (12417, 9) into --> (n, 29) fn Merge2()

# GOAL: Merge B Data into A, carrying A titles
If FirstName,LastName is in both A & B then Pull B, else use A format and create new row

There are 58 rows.
The length of the final spreadsheet should increase by 58
Number of rows in Master: 7330
Number of rows to be added from Brochure: 58
Merge should have 7388 rows.
I now remove the columns that are not in master, and add using only master titles. 

A_b has 7388 rows, so (7388, 29)

2560 rows x 7 columns

