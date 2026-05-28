import pandas as pd
import os
import datetime

# ========== 1. 配置 ==========
RAW_DIR = './data/raw'
PROC_DIR = './data/processed'
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)
DATA_FILES = [
    'RAW3.csv',
    'citations (1).csv',
    'raw2.csv'
]

COLUMN_MAPPING = {
    'Article Title': 'TI',
    'Authors': 'AU',
    'Author Full Names': 'AF',
    'Affiliations': 'C1',
    'Publication Year': 'PY',
    'Source Title': 'SO',
    'Abstract': 'AB',
    'Author Keywords': 'DE',
    'Keywords Plus': 'ID',
    'Cited References': 'CR',
    'DOI': 'DI',
    'Document Type': 'DT',
    'Times Cited': 'TC',
    'Accession Number': 'UT',
    'ISSN': 'SN',
    'eISSN': 'EI',
    'ISBN': 'BN',
    'Volume': 'VL',
    'Issue': 'IS',
    'Start Page': 'BP',
    'End Page': 'EP',
    'PubMed ID': 'PM',
    'Language': 'LA',
    'Publication Type': 'PT',
    'Conference Title': 'CT',
    'Conference Date': 'CY',
    'Conference Location': 'CL',
    'Book Title': 'BK',
    'Editor': 'BE',
    'Publisher': 'PU',
    'Cited Reference Count': 'NR',
}

CITESPACE_REQUIRED = ['PT', 'TI', 'AU', 'PY', 'SO', 'AB', 'DE', 'UT', 'CR', 'DI', 'TC', 'DT']

# ========== 2. 基础功能 ==========
def read_csv_utf8(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")
    return pd.read_csv(path, encoding='utf-8', dtype=str, keep_default_na=False)

def export_wos_txt(df, path):
    df.to_csv(path, sep='\t', encoding='utf-8', index=False, quoting=1)

def field_missing_ratio(df, fields):
    check_fields = [f for f in fields if f in df.columns]
    return df[check_fields].replace('', pd.NA).isna().mean().round(3).to_dict()

def deduplicate(df):
    before = len(df)
    
    if 'UT' in df.columns:
        df_with_ut = df[df['UT'] != '']
        df_no_ut = df[df['UT'] == '']
        
        if len(df_with_ut) > 0:
            df_with_ut = df_with_ut.drop_duplicates(subset=['UT'], keep='first')
        
        if 'TI' in df_no_ut.columns and len(df_no_ut) > 0:
            df_no_ut = df_no_ut.drop_duplicates(subset=['TI'], keep='first')
            
        df = pd.concat([df_with_ut, df_no_ut], ignore_index=True)
    elif 'TI' in df.columns:
        df = df.drop_duplicates(subset=['TI'], keep='first')
    
    after = len(df)
    return df, before - after

def ambiguity_rate(df):
    result = {}
    if 'AU' in df.columns:
        author_amb = df['AU'].value_counts()
        result['作者同名计数'] = int((author_amb > 1).sum())
    if 'C1' in df.columns:
        org_amb = df['C1'].value_counts()
        result['机构同名计数'] = int((org_amb > 1).sum())
    return result

def filter_invalid_records(df):
    before = len(df)
    
    if 'TI' in df.columns:
        df = df[df['TI'] != '']
    else:
        key_fields = ['DI', 'UT']
        available_keys = [f for f in key_fields if f in df.columns]
        if available_keys:
            df = df[(df[available_keys] != '').any(axis=1)]
    
    after = len(df)
    return df, before - after

def ensure_citespace_format(df):
    if 'PT' not in df.columns:
        df['PT'] = 'J'
    
    if 'DT' in df.columns and 'PT' in df.columns:
        df['PT'] = df['PT'].replace('', pd.NA).fillna(df['DT'])
    
    for col in CITESPACE_REQUIRED:
        if col not in df.columns:
            df[col] = ''
    
    ordered_cols = [col for col in CITESPACE_REQUIRED if col in df.columns]
    ordered_cols += [col for col in df.columns if col not in ordered_cols]
    
    return df[ordered_cols]

# ========== 3. 主流程 ==========
stamp = datetime.datetime.now().isoformat(timespec='seconds')
quality_report = []

for fname in DATA_FILES:
    raw_path = os.path.join(RAW_DIR, fname)
    base_name = fname.replace('.csv', '').replace(' ', '_')
    proc_path = os.path.join(PROC_DIR, f'download_{base_name}.txt')

    print(f"正在处理: {fname} ...")
    
    try:
        df = read_csv_utf8(raw_path)
    except FileNotFoundError as e:
        print(f"  ⚠️ {e}")
        continue
    
    original_count = len(df)
    df = df.rename(columns=COLUMN_MAPPING)
    df, invalid_cnt = filter_invalid_records(df)
    df, dup_cnt = deduplicate(df)
    df = ensure_citespace_format(df)
    
    miss_ratio = field_missing_ratio(df, CITESPACE_REQUIRED)
    ambi = ambiguity_rate(df)
    ref_missing = (df['CR'] == '').sum() if 'CR' in df.columns else 0
    ut_missing = (df['UT'] == '').sum() if 'UT' in df.columns else len(df)
    final_count = len(df)
    
    export_wos_txt(df, proc_path)
    print(f"  ✓ 已导出: {proc_path} ({final_count}条记录)")

    quality_report.append(f"### {fname}")
    quality_report.append(f"- 原始记录数: {original_count}")
    quality_report.append(f"- 清洗后记录数: {final_count}")
    quality_report.append(f"- 过滤无效记录数: {invalid_cnt}")
    quality_report.append(f"- 去重数: {dup_cnt}")
    quality_report.append(f"- 核心字段缺失率: {miss_ratio}")
    quality_report.append(f"- UT缺失数: {ut_missing}")
    if '作者同名计数' in ambi:
        quality_report.append(f"- 作者歧义数: {ambi.get('作者同名计数', 0)}")
    if '机构同名计数' in ambi:
        quality_report.append(f"- 机构歧义数: {ambi.get('机构同名计数', 0)}")
    quality_report.append(f"- 缺参考文献条数: {ref_missing}")
    quality_report.append(f"- 输出文件: download_{base_name}.txt\n")

# ========== 4. 生成报告 ==========
with open(os.path.join(PROC_DIR, '数据质量报告.txt'), 'w', encoding='utf-8') as f:
    f.write(f"# 数据质量报告\n\n")
    f.write(f"生成时间：{stamp}\n\n")
    f.write(f"## 文件列表\n\n")
    for fname in DATA_FILES:
        base_name = fname.replace('.csv', '').replace(' ', '_')
        f.write(f"- download_{base_name}.txt\n")
    f.write(f"\n## 清洗详情\n\n")
    f.write('\n'.join(quality_report))

print("\n" + "="*60)
print("✅ 全部清洗完成！")
print("="*60)
print(f"\n📁 输出目录: {PROC_DIR}")
print(f"📄 详细报告: {os.path.join(PROC_DIR, '数据质量报告.txt')}")
