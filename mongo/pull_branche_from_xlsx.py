from module.BranchenDeteilsExtern import rmBranchenDetailsExtern
import pandas as pd
from module.BranchenDeteilsExtern import rmBranchenDetailsExtern


def get_column_of_xlsx(path: str, column_name: str) -> set[str]:
    file = pd.read_excel(path, index_col=1)
    frame: pd.DataFrame = (file).fillna("xxxxx")
    column = frame[column_name]
    return set(column)


if __name__ == "__main__":
    zfids = get_column_of_xlsx(
        "/home/user199/Desktop/20210315_fehlende_Städte_größer_20000.xlsx",
        "ZFID",
    )
    branche = dict(Name="staedte", Herkunft="1", WZCode=248411103)
    rmBranchenDetailsExtern(zfids=list(zfids), branche=branche)
