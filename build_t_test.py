import json
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# JSON 파일이 현재 스크립트와 같은 폴더에 있다고 가정
cold_build_file = "cold_build.json"
warm_build_file = "warm_build.json"

# JSON 파일 로드
with open(cold_build_file, "r") as f:
    cold_build_json = json.load(f)

with open(warm_build_file, "r") as f:
    warm_build_json = json.load(f)

# 실행 시간 데이터 추출
cold_times = cold_build_json["results"][0]["times"]
warm_times = warm_build_json["results"][0]["times"]

# 평균 및 표준편차 비교 테이블 생성
comparison_results = {
    "Metric": ["Mean (s)", "Std Dev (s)", "Min (s)", "Max (s)", "Median (s)"],
    "Cold Build": [
        cold_build_json["results"][0]["mean"],
        cold_build_json["results"][0]["stddev"],
        cold_build_json["results"][0]["min"],
        cold_build_json["results"][0]["max"],
        cold_build_json["results"][0]["median"],
    ],
    "Warm Build": [
        warm_build_json["results"][0]["mean"],
        warm_build_json["results"][0]["stddev"],
        warm_build_json["results"][0]["min"],
        warm_build_json["results"][0]["max"],
        warm_build_json["results"][0]["median"],
    ]
}

# T-test 수행
t_stat, p_value = stats.ttest_ind(cold_times, warm_times, equal_var=False)

# 데이터프레임 변환 및 출력
comparison_df = pd.DataFrame(comparison_results)
print(comparison_df)

# T-test 결과 출력
print(f"\nT-statistic: {t_stat:.3f}")
print(f"P-value: {p_value:.3e}")

# 실행 시간 분포 시각화
plt.figure(figsize=(8, 5))
plt.hist(cold_times, alpha=0.5, label="Cold Build", bins=5, color='red')
plt.hist(warm_times, alpha=0.5, label="Warm Build", bins=5, color='blue')
plt.legend()
plt.xlabel("Execution Time (s)")
plt.ylabel("Frequency")
plt.title("Cold vs Warm Build Execution Time Distribution")
plt.show()
