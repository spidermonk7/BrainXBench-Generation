import os
import shutil

# ==== 年份 ====
years = [17, 18, 19, 20, 21, 22, 24]

# ==== 工作目录结构 ====
workspace_root = "workspaces"
csvs_subdir = "bench/forward/csvs"

# ==== 原始文件名 -> tag 映射 ====
rename_rules = {
    "Factor_Misattribution.csv": "Factor_Misattribution",
    "Opposite_Outcome.csv": "Opposite_Outcome",
    "Incorrect_Causal_Relationship.csv": "Incorrect_Causal_Relationship"
}

# ==== 最终输出目录 ====
output_dir = "/Users/cuishaoyang/Desktop/PKU/KaiTeam/BrainX-NeuroBench/BenchData/BXB/forward/csvs"
os.makedirs(output_dir, exist_ok=True)

# ==== 重命名 + 复制 ====
for year in years:
    folder_name = f"BrainX-{year}JFM"
    target_dir = os.path.join(workspace_root, folder_name, csvs_subdir)

    for original_filename, tag in rename_rules.items():
        original_path = os.path.join(target_dir, original_filename)
        new_filename = f"{year}_{tag}-V0.6.csv"
        new_path = os.path.join(target_dir, new_filename)
        final_output_path = os.path.join(output_dir, new_filename)

        if os.path.exists(original_path):
            os.rename(original_path, new_path)
            shutil.copy(new_path, final_output_path)
            print(f"✅ Renamed and copied: {original_path} → {final_output_path}")
        else:
            print(f"⚠️  Skipped (not found): {original_path}")
