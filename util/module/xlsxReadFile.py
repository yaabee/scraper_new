import pandas as pd

def xlsxReadFile(path: str) -> pd.DataFrame:
    file = pd.read_excel(path)
    return (file).fillna("xxxxx")

if __name__ == '__main__':
    df = xlsxReadFile('/home/user199/Desktop/ausf_hkls,1.xlsx')
