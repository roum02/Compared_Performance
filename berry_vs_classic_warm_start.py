import json
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# JSON 데이터 로드
berry_warm_start_file = "berry_warm_start.json"
classic_warm_start_file = "warm_start.json"

with open(berry_warm_start_file, "r") as f:
    berry_warm_start_json = json.load(f)

with open(classic_warm_start_file, "r") as f:
    classic_warm_start_json = json.load(f)

# 실행 시간 데이터 추출
berry_warm_times = berry_warm_start_json["results"][0]["times"]  # 5회 실행
classic_warm_times = classic_warm_start_json["results"][0]["times"]  # 10회 실행

# 실행 횟수 차이를 보정하기 위해 Classic의 10개 샘플에서 5개를 무작위 선택
np.random.seed(42)  # 랜덤 시드 고정 (재현 가능성 유지)
classic_warm_sampled_times = np.random.choice(classic_warm_times, size=5, replace=False)

# 성능 비교 테이블 생성
comparison_results = {
    "Metric": ["Mean (s)", "Std Dev (s)", "Min (s)", "Max (s)", "Median (s)"],
    "Berry Warm Start": [
        np.mean(berry_warm_times),
        np.std(berry_warm_times, ddof=1),
        np.min(berry_warm_times),
        np.max(berry_warm_times),
        np.median(berry_warm_times),
    ],
    "Classic Warm Start (Sampled)": [
        np.mean(classic_warm_sampled_times),
        np.std(classic_warm_sampled_times, ddof=1),
        np.min(classic_warm_sampled_times),
        np.max(classic_warm_sampled_times),
        np.median(classic_warm_sampled_times),
    ]
}

# T-test 수행 (통계적 유의미한 차이 확인)
t_stat, p_value = stats.ttest_ind(berry_warm_times, classic_warm_sampled_times, equal_var=False)

# 결과 데이터프레임 생성
comparison_df = pd.DataFrame(comparison_results)

# 결과 출력
print(comparison_df)
print(f"\nT-statistic: {t_stat:.3f}")
print(f"P-value: {p_value:.3e}")

# 실행 시간 분포 시각화
plt.figure(figsize=(8, 5))
plt.hist(berry_warm_times, alpha=0.5, label="Berry Warm Start", bins=5, color='blue')
plt.hist(classic_warm_sampled_times, alpha=0.5, label="Classic Warm Start (Sampled)", bins=5, color='red')
plt.legend()
plt.xlabel("Execution Time (s)")
plt.ylabel("Frequency")
plt.title("Yarn Berry vs Classic Warm Start Execution Time Distribution")
plt.show()
