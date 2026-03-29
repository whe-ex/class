import pandas as pd
import re
from io import StringIO

data_str = """Authors,Title,Publication,Volume,Number,Pages,Year,Publisher
"Alves, Luciano FS; Gomes, Ruan CM; Lefranc, Pierre; Pegado, Raoni De A; Jeannin, Pierre-Olivier; Luciano, Benedito A; Rocha, Filipe V; ",SIC power devices in power electronics: An overview,2017 Brazilian Power Electronics Conference (COBEP),,,1-8,2017,IEEE
"Gajewski, Donald A; Hull, Brett; Lichtenwalner, Daniel J; Ryu, Sei-Hyung; Bonelli, Eric; Mustain, Habib; Wang, Gangyao; Allen, Scott T; Palmour, John W; ",SiC power device reliability,2016 IEEE International Integrated Reliability Workshop (IIRW),,,29-34,2016,IEEE
"Buffolo, M; Favero, D; Marcuzzi, A; De Santi, C; Meneghesso, G; Zanoni, E; Meneghini, M; ","Review and outlook on GaN and SiC power devices: Industrial state-of-the-art, applications, and perspectives",IEEE Transactions on Electron Devices,71,3,1344-1355,2024,IEEE
"Kimoto, Tsunenobu; ",High-voltage SiC power devices for improved energy efficiency,"Proceedings of the Japan academy, series B",98,4,161-189,2022,The Japan Academy
"Chen, Zibo; Huang, Alex Q; ",Extreme high efficiency enabled by silicon carbide (SiC) power devices,Materials Science in Semiconductor Processing,172,,108052,2024,Elsevier
"Baliga, B Jayant; ",Silicon carbide power devices: Progress and future outlook,IEEE Journal of Emerging and Selected Topics in Power Electronics,11,3,2400-2411,2023,IEEE
"Kimoto, T; Yonezawa, Y; ",Current status and perspectives of ultrahigh-voltage SiC power devices,Materials Science in Semiconductor Processing,78,,43-56,2018,Elsevier
"Xun, Qian; Xun, Boyang; Li, Zuxin; Wang, Peiliang; Cai, Zhiduan; ",Application of SiC power electronic devices in secondary power source for aircraft,Renewable and Sustainable Energy Reviews,70,,1336-1342,2017,Elsevier
"Yuan, Xibo; Laird, Ian; Walder, Sam; ","Opportunities, challenges, and potential solutions in the application of fast-switching SiC power devices and converters",IEEE Transactions on Power Electronics,36,4,3925-3945,2020,IEEE
"Kimoto, T; Iijima, A; Tsuchida, H; Miyazawa, T; Tawara, T; Otsuki, A; Kato, T; Yonezawa, Y; ",Understanding and reduction of degradation phenomena in SiC power devices,2017 IEEE International Reliability Physics Symposium (IRPS),,,2A-1.1-2A-1.7,2017,IEEE
"Lauenstein, Jean-Marie; Casey, Megan C; Ladbury, Ray L; Kim, Hak S; Phan, Anthony M; Topper, Alyson D; ",Space radiation effects on SiC power device reliability,2021 IEEE International Reliability Physics Symposium (IRPS),,,1-8,2021,IEEE
"Hu, Borong; Gonzalez, Jose Ortiz; Ran, Li; Ren, Hai; Zeng, Zheng; Lai, Wei; Gao, Bing; Alatise, Olayiwola; Lu, Hua; Bailey, Christopher; ",Failure and reliability analysis of a SiC power module based on stress comparison to a Si device,IEEE Transactions on device and materials reliability,17,4,727-737,2017,IEEE
"La Via, Francesco; Alquier, Daniel; Giannazzo, Filippo; Kimoto, Tsunenobu; Neudeck, Philip; Ou, Haiyan; Roncaglia, Alberto; Saddow, Stephen E; Tudisco, Salvatore; ",Emerging SiC applications beyond power electronic devices,Micromachines,14,6,1200,2023,MDPI
"Baliga, B Jayant; ",Gallium nitride and silicon carbide power devices,,,,,2016,world scientific publishing company
"Castellazzi, Alberto; Fayyaz, Asad; Romano, Gianpaolo; Yang, Li; Riccio, Michele; Irace, Andrea; ","SiC power MOSFETs performance, robustness and technology maturity",Microelectronics Reliability,58,,164-176,2016,Elsevier
"Langpoklakpam, Catherine; Liu, An-Chen; Chu, Kuo-Hsiung; Hsu, Lung-Hsing; Lee, Wen-Chung; Chen, Shih-Chen; Sun, Chia-Wei; Shih, Min-Hsiung; Lee, Kung-Yen; Kuo, Hao-Chung; ",Review of silicon carbide processing for power MOSFET,Crystals,12,2,245,2022,MDPI
"Gonzalez, Jose Ortiz; Wu, Ruizhu; Jahdi, Saeed; Alatise, Olayiwola; ","Performance and reliability review of 650 V and 900 V silicon and SiC devices: MOSFETs, cascode JFETs and IGBTs",IEEE Transactions on Industrial Electronics,67,9,7375-7385,2019,IEEE
"Roccaforte, Fabrizio; Fiorenza, Patrick; Greco, Giuseppe; Nigro, Raffaella Lo; Giannazzo, Filippo; Iucolano, Ferdinando; Saggio, Mario; ",Emerging trends in wide band gap semiconductors (SiC and GaN) technology for power devices,Microelectronic Engineering,187,,66-77,2018,Elsevier
"Baierhofer, Daniel; ","Current SiC power device development, material defect measurements and characterization at bosch",ESSDERC 2019-49th European Solid-State Device Research Conference (ESSDERC),,,31-34,2019,IEEE"""

df = pd.read_csv(StringIO(data_str))

df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

for col in ["Volume", "Number", "Pages", "Publication", "Publisher"]:
    df[col] = df[col].fillna("N/A")

def extract_author_list(author_str):
    if pd.isna(author_str):
        return []
    authors = re.split(r';\s*', author_str.strip('" ;'))
    return [a.strip() for a in authors if a.strip()]

df["Author_List"] = df["Authors"].apply(extract_author_list)
df["First_Author"] = df["Author_List"].str[0].fillna("Unknown")

def get_document_type(pub):
    if not isinstance(pub, str) or pub.strip() == "N/A":
        return "Book/Other"
    pub = pub.lower()
    conf_words = ["conference", "symposium", "workshop", "cobep", "irps", "essderc"]
    jour_words = ["transactions", "journal", "materials", "microelectronics", "crystals", "micromachines"]
    
    if any(word in pub for word in conf_words):
        return "Conference"
    elif any(word in pub for word in jour_words):
        return "Journal"
    else:
        return "Book/Other"

df["Document_Type"] = df["Publication"].apply(get_document_type)

def get_keywords(title):
    if not isinstance(title, str):
        return "General"
    title = title.lower()
    keywords = []
    if "sic" in title or "silicon carbide" in title:
        keywords.append("SiC")
    if "gan" in title or "gallium nitride" in title:
        keywords.append("GaN")
    if "reliability" in title or "failure" in title or "degradation" in title:
        keywords.append("Reliability")
    if "mosfet" in title:
        keywords.append("MOSFET")
    if "high voltage" in title or "high-voltage" in title:
        keywords.append("High-Voltage")
    return "; ".join(keywords) if keywords else "General"

df["Keywords"] = df["Title"].apply(get_keywords)

df["Publisher_Clean"] = df["Publisher"].str.title()

clean_df = df[[
    "First_Author", "Authors", "Author_List",
    "Title", "Keywords",
    "Publication", "Document_Type",
    "Volume", "Number", "Pages",
    "Year", "Publisher_Clean"
]].copy()

print("="*60)
print("✅ 数据清洗完成！")
print("="*60)
print(f"📊 总文献数：{len(clean_df)} 篇")
print(f"📅 年份范围：{int(clean_df['Year'].min())} – {int(clean_df['Year'].max())}")
print("\n📌 文献类型统计：")
print(clean_df["Document_Type"].value_counts())
print("\n📌 研究主题统计：")
print(clean_df["Keywords"].value_counts().head(10))