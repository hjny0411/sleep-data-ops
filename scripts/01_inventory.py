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

# 함수 시험: 형식이 틀린 이름을 넣으면?
print(parse_name("sc4001e0=-psg.edf"))