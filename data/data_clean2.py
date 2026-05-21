import pandas as pd
import os
import datetime

# ========== 1. 配置 ==========
RAW_DIR = '.'
PROC_DIR = './processed'
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)
DATA_FILES = [
    'RAW3.csv',
    'citations (1).csv',
    'raw2.csv'
]
REQUIRED_FIELDS = [
    '标题', '作者', '机构', '年份', '期刊', '摘要', '关键词', '参考文献', 'DOI'
]

# ========== 2. 基础功能 ==========
def read_csv_utf8(path):
    return pd.read_csv(path, encoding='utf-8', dtype=str, keep_default_na=False)

def export_csv_utf8(df, path):
    df.to_csv(path, encoding='utf-8', index=False, quoting=1)

def field_missing_ratio(df):
    return df[REQUIRED_FIELDS].replace('', pd.NA).isna().mean().round(3).to_dict()

def deduplicate(df):
    before = len(df)
    if 'DOI' in df.columns and df['DOI'].nunique() > 1:
        df = df.drop_duplicates(subset=['DOI'])
    else:
        df = df.drop_duplicates(subset=['标题'])
    after = len(df)
    return df, before - after

def ambiguity_rate(df):
    author_amb = df['作者'].value_counts()
    org_amb = df['机构'].value_counts()
    author_amb_cnt = (author_amb > 1).sum()
    org_amb_cnt = (org_amb > 1).sum()
    return {'作者同名计数': int(author_amb_cnt), '机构同名计数': int(org_amb_cnt)}

# ========== 3. 主流程 ==========
stamp = datetime.datetime.now().isoformat(timespec='seconds')
quality_report = []
for fname in DATA_FILES:
    raw_path = os.path.join(RAW_DIR, fname)
    proc_path = os.path.join(PROC_DIR, fname.replace('.csv', '_cleaned.csv'))

    df = read_csv_utf8(raw_path)

    # 补全字段，按规范顺序
    for col in REQUIRED_FIELDS:
        if col not in df.columns:
            df[col] = ''
    df = df[REQUIRED_FIELDS]

    miss_ratio = field_missing_ratio(df)
    df, dup_cnt = deduplicate(df)
    ambi = ambiguity_rate(df)
    ref_missing = (df['参考文献'] == '').sum()

    export_csv_utf8(df, proc_path)

    # 质量报告
    quality_report.append(f"### {fname}")
    quality_report.append(f"- 总记录数: {len(df)}")
    quality_report.append(f"- 缺失率: {miss_ratio}")
    quality_report.append(f"- 去重数: {dup_cnt}")
    quality_report.append(f"- 作者歧义数: {ambi['作者同名计数']}；机构歧义数: {ambi['机构同名计数']}")
    quality_report.append(f"- 缺参考文献条数: {ref_missing}\n")

# ========== 4. 生成报告 ==========
with open(os.path.join(PROC_DIR, 'data_quality.md'), 'w', encoding='utf-8') as f:
    f.write(f"# 数据质量报告\n\n自动生成时间：{stamp}\n\n")
    f.write('\n'.join(quality_report))

with open(os.path.join(PROC_DIR, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(f"# 数据处理说明\n\n")
    f.write(f"本目录下数据已按课件标准清洗。原始数据在 raw/，清理结果在 processed/。\n")
    f.write(f"- 导出时间戳：{stamp}\n\n")
    f.write(f"## 字段字典\n")
    for col in REQUIRED_FIELDS:
        f.write(f"- {col}\n")
    f.write("\n## 质量报告见 data_quality.md\n")

print("全部清洗完成。质量报告与说明已在 processed/ 目录生成。")
