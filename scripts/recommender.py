import pandas as pd
from pathlib import Path
BASE_DIR = Path.cwd().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
df = pd.read_csv(PROCESSED_DIR/"scheme_performance_clean.csv")

def recommend_funds(risk_appetite):

    funds = df[df["risk_grade"].str.lower() == risk_appetite.lower()]

    funds = funds.sort_values("sharpe_ratio", ascending=False)

    top_funds = funds.head(3)

    return top_funds[["amfi_code", "sharpe_ratio", "risk_grade"]]

risk = input("enter risk appetite (low/moderate/high): ")

recommendations = recommend_funds(risk)

print("top 3 recommended funds",end='\n')
print(recommendations)