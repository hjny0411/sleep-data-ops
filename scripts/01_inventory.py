# 폴더 훑기
from pathlib import Path
from datetime import datetime
import pandas as pd
import re

RAW_DIR = Path("data/raw")
PATTERN = re.compile(r"^SC4(\d{2})([12])E.-(PSG|Hypnogram)\.edf$")

def parse_name(name):
    m = PATTERN.match(name)
    if m is None:
        return{"subject": None, "night": None, "file_type": None, "record_key": None, "name_valid": False}
    subject = int(m.group(1))
    night = int(m.group(2))
    return {
        "subject": subject,
        "night": night,
        "file_type": m.group(3),
        "record_key": f"S{subject:02d}_N{night}",
        "name_valid": True        
    }

rows = []
for f in sorted(RAW_DIR.rglob("*")):
    if not f. is_file():
        continue
    st = f.stat()
    row= {
        "file_name": f.name,
        "ext": f.suffix,
        "size_bytes": st.st_size,
        "size_mb": round(st.st_size / 1024**2, 2),
        "midified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M") 
    }
    row.update(parse_name(f.name))
    rows.append(row)
df = pd.DataFrame(rows)
print("파일 수:", len(df))
print(df[["file_name", "subject", "night", "file_type", "record_key","name_valid"]].head())
print(df["file_type"].value_counts())
print(df["name_valid"].value_counts())

valid = df[df["name_valid"]]

pair = valid.pivot_table(index="record_key", columns="file_type", aggfunc="size", fill_value=0)
pair = pair.reindex(columns=["PSG", "Hypnogram"], fill_value=0)

def judge(r):
    if r["PSG"] > 1 or r["Hypnogram"] > 1:
        return "중복 의심"
    if r["PSG"] == 1 and r["Hypnogram"] ==  1:
        return "정상"
    if r["PSG"] == 1:
        return "판독본 없음"
    return "PSG 없음"

pair["status"] = pair.apply(judge, axis=1)

print("기록 수:", len(pair))
print(pair["status"].value_counts())
print(pair.head())

test = pd.DataFrame(
    {"PSG": [1, 1, 0, 2], "Hypnogram":[1, 0, 1, 1]},
    index = ["정상이어야 함", "판독본 없음이어야 함", "PSG 없음이어야 함", "중복 의심이어야 함"],
)
test["status"] = test.apply(judge, axis =1)
print(test)

OUT_DIR =Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

df.to_csv(OUT_DIR / "invevtory.csv", index=False, encoding="utf-8-sig")
pair.to_csv(OUT_DIR / "pair_summary.csv", encoding="utf-8-sig")
bad_pair = (pair["status"]!="정상").sum()

bad_name = (~df["name_valid"]).sum()
bad_pair = (pair["status"] !="정상").sum()
print(f"[요약] 파일 {len(df)}개 / 기록 {len(pair)}건 / 형식 오류 {bad_name}개 / 짝 이상 {bad_pair}건")