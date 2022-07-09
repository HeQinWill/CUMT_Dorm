from pathlib import Path
import pandas as pd
import plotly.express as px

# 列出所有采集的电量信息
file_list = list(Path('dorm_elec').rglob('*.csv'))
file_list.sort()

# 拼接所有的表
d_list = []
for f in file_list[:]:
    df = pd.read_csv(f, header=None)
    d_list.append(df)
df_all = pd.concat(d_list)

# 如需备份数据
# df_all.to_csv(f'dorm_elec/until_{df_all.iloc[-1, 3]}.csv', header=None, index=None)

# 设置时间列索引
df_all[3] = pd.to_datetime(df_all[3])
df_all.set_index(df_all[3], inplace=True)

# 获取最近一个时刻的状态
now = df_all.iloc[-1]
now_elec = now[1] - now[2]

# 按时间重采样为逐小时数据，并计算差值
df_all = df_all.resample('1H', axis=0).mean()
df_all = df_all.diff(-1).dropna()
df_all.columns = ['charging', 'using']

# 用 plotly 显示图表
fig = px.bar(df_all, title=f'截至 {now[3]}，还剩 {now_elec} 度电')
fig.write_html('fig.html')