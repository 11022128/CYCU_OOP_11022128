import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv('20250520/midterm_scores.csv')

# 定義科目名稱
subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']

# 計算每位學生不及格科目的數量 (成績 < 60)
df['FailCount'] = (df[subjects] < 60).sum(axis=1)

# 找出不及格科目超過一半的學生 (超過 7 科目的一半為 4 科)
students_with_many_fails = df[df['FailCount'] > len(subjects) / 2]

# 顯示結果
if not students_with_many_fails.empty:
    print("超過一半科目成績不及格的學生：")
    print(students_with_many_fails[['Name', 'FailCount']])
else:
    print("沒有學生超過一半科目成績不及格。")

# 將結果輸出為 CSV 檔案
students_with_many_fails.to_csv('20250520/students_with_many_fails.csv', index=False)