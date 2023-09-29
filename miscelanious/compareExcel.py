import pandas as pd


# viessman 10.
file1 = pd.read_excel(
    "/home/user199/Desktop/gesungheitswesen/ObjektScout KW46.2022_cron.xlsx"
)

# viessman 17 original
file2 = pd.read_excel(
    "/home/user199/Desktop/gesungheitswesen/ObjektScout KW47.2022_cron.xlsx"
)

# viessman 17. mit beteiligte
file3 = pd.read_excel("/home/user199/Downloads/odinExport - 2022-11-22T083725.570.xlsx")

# viessman 17. ohne beteiligte (aktuell)
file4 = pd.read_excel("/home/user199/Downloads/odinExport - 2022-11-22T083930.006.xlsx")

neue_datei_945 = pd.read_excel(
    "/home/user199/Downloads/odinExport - 2022-11-24T161231.425.xlsx"
)

frame1: pd.DataFrame = (file1).fillna("xxxxx")
frame2: pd.DataFrame = (file2).fillna("xxxxx")
frame3: pd.DataFrame = (file3).fillna("xxxxx")
frame4: pd.DataFrame = (file4).fillna("xxxxx")
frame_945: pd.DataFrame = (neue_datei_945).fillna("xxxxx")

zoids1 = frame1["ZOID"].to_list()
zoids2 = frame2["ZOID"].to_list()
zoids3 = frame3["ZOID"].to_list()
zoids4 = frame4["ZOID"].to_list()
zoids5 = frame_945["ZOID"].to_list()

zoids1 = set(zoids1)
print(len(zoids1))
zoids2 = set(zoids2)
print(len(zoids2))
zoids3 = set(zoids3)
print(len(zoids3))
zoids4 = set(zoids4)
print(len(zoids4))


# print(zoids1.difference(zoids3))

df = pd.DataFrame(list(zoids4.difference(zoids5)))
print(df)
# df.to_csv(f"./comparison.csv")


# im access nur die mit beteiligeten
