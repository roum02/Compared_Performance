import json
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# JSON 파일이 현재 스크립트와 같은 폴더에 있다고 가정
cold_start_file = "cold_start.json"
warm_start_file = "warm_start.json"

# JSON 파일 로드
with open(cold_start_file, "r") as f:
    cold_start_json = json.load(f)

with open(warm_start_file, "r") as f:
    warm_start_json = json.load(f)

# 실행 시간 데이터 추출
cold_times = cold_start_json["results"][0]["times"]
warm_times = warm_start_json["results"][0]["times"]

# 평균 및 표준편차 계산
comparison_results = {
    "Metric": ["Mean (s)", "Std Dev (s)", "Min (s)", "Max (s)", "Median (s)"],
    "Cold Start": [
        cold_start_json["results"][0]["mean"],
        cold_start_json["results"][0]["stddev"],
        cold_start_json["results"][0]["min"],
        cold_start_json["results"][0]["max"],
        cold_start_json["results"][0]["median"],
    ],
    "Warm Start": [
        warm_start_json["results"][0]["mean"],
        warm_start_json["results"][0]["stddev"],
        warm_start_json["results"][0]["min"],
        warm_start_json["results"][0]["max"],
        warm_start_json["results"][0]["median"],
    ]
}

# T-test 수행
t_stat, p_value = stats.ttest_ind(cold_times, warm_times, equal_var=False)

# 결과 출력
comparison_df = pd.DataFrame(comparison_results)
print(comparison_df)
print(f"T-statistic: {t_stat:.3f}, P-value: {p_value:.3e}")

# 실행 시간 분포 시각화
plt.hist(cold_times, alpha=0.5, label="Cold Start", bins=10)
plt.hist(warm_times, alpha=0.5, label="Warm Start", bins=10)
plt.legend()
plt.xlabel("Execution Time (s)")
plt.ylabel("Frequency")
plt.title("Cold vs Warm Start Execution Time Distribution")
plt.show()
