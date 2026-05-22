# 第⑦组 Homework
## 1.成员分工内容
| 姓名   | 学号   | 分工内容   |
|-------|-------|-------|
| 林能行 | 202416010211 | 项目统筹与进度管理 |
| 潘儒凤 | 202416010321 | 检索策略设计 |
| 毛俊钦 | 202416010118 | 文献收集与筛选 |
| 李炫浒 | 202416010206 | 数据整理与预处理 |
| 张博 | 202416010314 | 计量与可视化分析 |
| 刘硕 | 202416010130 | 结果撰写与展示 |


## 2.研究方向
- SiC功率器件研究热点与演进趋势
### 备选方向
- GaN射频器件研究热点与演进趋势计量分析
- AI加速芯片研究热点与演进趋势计量分析

## 3.项目结构

```
├── config/                      # 配置文件目录
│   ├── query.yaml
│   └── synonyms.yaml
├── data/                        # 数据目录
│   ├── processed/               # 已处理数据
│   │   ├── RAW3_cleaned.csv
│   │   ├── citations (1)_cleaned.csv
│   │   ├── raw2_cleaned.csv
│   │   └── README.md
│   ├── raw/                     # 原始数据
│   │   ├── RAW3.csv
│   │   ├── citations (1).csv
│   │   ├── raw2.csv
│   │   ├── text1.txt
│   │   ├── text2.txt
│   │   ├── text3.txt
│   │   ├── text4.txt
│   │   └── text5.txt
│   └── data_clean2.py           # 数据清洗脚本
├── docs/
│   └── direction_candidates.md
├── output/                  # 分析结果与可视化
│   ├── 作者合作.png
│   ├── 共被引网络分析报告.md
│   ├── 文献引用特征分析表.xlsx
│   ├── 时间线.png
│   └── 聚类图.png
├── paper/                       # 论文相关内容
├── reports/                     # 分析报告与过程
│   └── data_quality.md
├── src/                         # 源代码
├── README.md                    # 项目说明文件
└── requirements.txt             # Python依赖包清单
```

## 4.工具与软件环境

本项目采用以下工具与编程环境完成核心分析与展示工作：

- CiteSpace：用于科学计量与知识图谱生成
- VOSviewer：关键词共现与网络结构可视化
- Python（pandas、numpy、matplotlib）：数据处理和绘图

---
  
## 5.操作流程概述

1. 数据采集  
   将检索获得的文献数据（CSV 格式）放置于 `data/` 目录下。

2. 数据预处理  
   使用 `src/` 路径下的 Python 脚本进行数据清理与统计。

3. 网络与趋势分析  
   结合 CiteSpace 或 VOSviewer，对处理后数据进行主题提取与网络关系构建，并生成相关图表。

4. 结果输出  
   所有分析产品（如趋势图、共现网络图等）汇总于 `outputs/` 目录。

---

## 6.已完成内容

- 数据目录、配置文件、文档结构初步搭建
- 数据清洗脚本：`data/data_clean2.py`
- 配置文件：`config/query.yaml`、`config/synonyms.yaml`
- 方向候选文档：`docs/direction_candidates.md`
- 数据质量分析报告：`reports/data_quality.md`
- requirements.txt 依赖清单初始化
- 主要分析结果（见 output 文件夹）：
    - 聚类分析图（`output/聚类图.png`）
    - 主题演化时间线图（`output/时间线.png`）
    - 作者合作网络图（`output/作者合作.png`）
    - 共被引网络分析报告（`output/共被引网络分析报告.md`）
    - 文献引用特征分析表（`output/文献引用特征分析表.xlsx`）

## 7.复现性说明

- 检索关键词统一，确保分析一致性
- 原始数据文件与所用脚本全部保留
- 处理与分析每一环节均有明确文档和源码可查
- 仓库维护完整输出，方便溯源和二次分析

---

**项目说明**  
本项目为课程小组作业，旨在通过文献计量分析方法，掌握学术研究的基本流程，并实现研究结果的可复现性。
