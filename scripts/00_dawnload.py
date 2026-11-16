
# 목록 파일 읽어보기
from pathlib import Path
sum_path = Path("data/reference/SHA256SUMS.txt")
lines = sum_path.read_text().splitlines()

print("전체 줄 수:, len(lines)")
for line in lines[:5]:
    print(line)
    
# 필요한 파일만 골라내기 
targets = []
for line in lines:
    hash_value, rel_path = line.split()
    if not rel_path.startswith("sleep-cassette/"):
        continue
    name = rel_path.split("/")[-1]
    subject = int(name[3:5])
    if subject <= 14:
        targets.append(rel_path)
print("골라낸 파일 수:", len(targets))
for t in sorted(targets)[:6]:
    print(t)

# 한 개만 시험 다운로드 
import urllib.request

BASE_URL = "https://physionet.org/files/sleep-edfx/1.0.0/"
RAW_DIR = Path("data/raw")

# test = sorted(targets)[1]
# url = BASE_URL + test
# dest = RAW_DIR / test.split("/")[-1]

# print("받는 중:", url)
# urllib.request.urlretrieve(url, dest)
# print("완료:", dest, dest.stat().st_size, "bytes")

# 전체 다운로드 

downloaded, skipped = 0, 0

for rel_path in sorted(targets):
    dest = RAW_DIR / rel_path.split("/")[-1]
    
    if dest.exists():
        skipped += 1
        continue
    tmp = dest.with_suffix(".part")
    print("받는 중:", dest.name)
    urllib.request.urlretrieve(BASE_URL + rel_path, tmp)
    tmp.rename(dest)
    downloaded += 1
    
print(f"새로받음 {downloaded}개, 건너뜀 {skipped}개")
print("data/raw 파일 수:", len(list(RAW_DIR.glob("*.edf"))))


