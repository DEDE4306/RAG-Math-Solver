from datasets import load_dataset
import pandas as pd
import csv
import os

# 加载数据集
ds = load_dataset("AI-MO/NuminaMath-CoT", split="train")  # 也可以改成 "test"

# 分块大小
chunk_size = 500

# 输出文件夹
output_dir = "numina_chunks"
os.makedirs(output_dir, exist_ok=True)

# 分块导出为多个 CSV 文件
for i in range(0, len(ds), chunk_size):
    chunk = ds[i:i + chunk_size]
    df = pd.DataFrame(chunk)
    df.to_csv(os.path.join(output_dir, f"train_chunk_{i}_{i + len(df) - 1}.csv"),
              index=False,
              encoding='utf-8-sig',
              quoting=csv.QUOTE_ALL,
              escapechar='\\')

print("✅ 所有分块CSV导出完成！")
