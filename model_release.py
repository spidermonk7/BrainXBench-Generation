from huggingface_hub import HfApi
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import scienceplots
# 初始化 Hugging Face API
# api = HfApi()

# # 获取最多 10,000 个模型（你可以分页拉更多）
# models = api.list_models(limit=30000)

# # 统计创建年份
# year_counter = Counter()
# for id, model in enumerate(models):
#     print(f"Model {id}: {model.modelId}, Created At: {model.created_at}")
#     if model.created_at:
#         year_counter[model.created_at.year] += 1

# # 转换为 DataFrame 并排序
# df = pd.DataFrame(sorted(year_counter.items()), columns=["Year", "Model Count"])
# print(df)

# # save the data df
# df.to_csv("huggingface_model_release.csv", index=False)


import matplotlib.pyplot as plt

# 假设你已经准备好 df，包含两列：df["Year"], df["Model Count"]
df = pd.read_csv("huggingface_model_release.csv")
plt.style.use('seaborn-v0_8-paper')

fig, ax = plt.subplots(figsize=(6, 6))

bars = ax.bar(df["Year"], df["Model Count"], color="skyblue")

# 添加每个柱子顶部的数字
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=10)

# 去除 Y 轴
ax.spines['left'].set_visible(False)
ax.get_yaxis().set_visible(False)

# 去除上右边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 隐藏默认 x 轴
ax.spines['bottom'].set_visible(False)
ax.get_xaxis().set_ticks_position('none')

# 添加自定义 x 轴箭头（右向）
x_min, x_max = df["Year"].min(), df["Year"].max()
ax.annotate('', xy=(x_max + 0.5, 0), xytext=(x_min - 0.5, 0),
            arrowprops=dict(arrowstyle='->', lw=2.0, color='black'))

# 重新标注年份
ax.set_xticks(df["Year"])
ax.set_xticklabels(df["Year"], fontsize=10)

plt.tight_layout()
plt.savefig("huggingface_model_release_arrow.png", dpi=300, transparent=True)
plt.show()
