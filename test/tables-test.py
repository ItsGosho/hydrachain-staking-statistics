from prettytable import PrettyTable as pt

tb = pt(title="Hydra Staking Statistics")


#Add headers
tb.field_names = ["Month","Total", "Transactions","Block Min", "Block Max", "USD End Month", "BGN End Month", "USD Equivalent Today", "BGN Equivalent Today"]
#tb.align["Major"] = "l"

#Add rows
tb.add_row(["1/2023", 127.47683867, 22, 5.74761925, 5.84260831, 258.24052716878856, 464.83294890381944, 298.2958024878, 536.93244447804])
tb.add_row(["2/2023", 127.47683867, 22, 5.74761925, 5.84260831, 258.24052716878856, 464.83294890381944, 298.2958024878, 536.93244447804])
tb.add_row(["3/2023", 127.47683867, 22, 5.74761925, 5.84260831, 258.24052716878856, 464.83294890381944, 298.2958024878, 536.93244447804])

print(tb)