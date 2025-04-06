import pandas as pd

# 从上两级目录读取数据
data_1 = pd.read_csv('../../data/test_prompts.csv')
data_2 = pd.read_csv('../../data/valid_data.csv')

# 将 'problem' 列重命名为 'question'
data_2.rename(columns={'problem': 'question'}, inplace=True)
# 将 'answer' 列重命名为 'numeric_answer'
data_2.rename(columns={'answer': 'numeric_answer'}, inplace=True)
# 填充缺失列
data_2['CoT_anot1'] = ''
data_2['CoT_anot2'] = ''
data_2['CoT_paths'] = ''
data_2['CoT_directions'] = ''
data_2['answer'] = ''
# 合并两个数据集
df_1 = pd.concat([data_1, data_2], ignore_index=True)
# 存为 csv 文件
df_1.to_csv('../../data/df_1.csv', index=False)

