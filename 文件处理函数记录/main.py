import pandas as pd
import csv
import json
import openpyxl as oxl
import xml.etree.ElementTree as ET
import sqlalchemy as sa


# ====================================== CSV，TSV ======================================
print("====================================== CSV，TSV ======================================")
# 第一种方式：使用DataFrame加载/写入CSV,TSV
# 读出数据的文件名
r_filenameCSV = 'realEstate_trans.csv'
r_filenameTSV = 'realEstate_trans.tsv'
# 写进数据的文件名
w_filenameCSV = 'realEstate_trans.csv'
w_filenameTSV = 'realEstate_trans.tsv'
# 读取数据
csv_read = pd.read_csv(r_filenameCSV)
tsv_read = pd.read_csv(r_filenameTSV, sep='\t')
# 输出头10行记录
print(csv_read.head(10))
print(tsv_read.head(10))

# 写入文件
with open(w_filenameCSV, 'w') as write_csv:
    write_csv.write(tsv_read.to_csv(sep=',', index=False))
with open(w_filenameTSV, 'w') as write_tsv:
    write_tsv.write(csv_read.to_csv(sep='\t', index=False))
# ====================================== CSV，TSV ======================================
print("====================================== CSV，TSV ======================================")
# 第二种方式：使用CSV加载/写入CSV
# 保存数据的数据结构
csv_labels = []
tsv_labels = []
csv_data = []
tsv_data = []

# 读取数据
with open(r_filenameCSV, 'r') as csv_in:
    csv_reader = csv.reader(csv_in)
    # 读取第一行，这是列标签
    csv_labels = csv_reader.__next__()
    # 遍历记录
    for record in csv_reader:
        csv_data.append(record)
with open(r_filenameTSV, 'r') as tsv_in:
    tsv_reader = csv.reader(tsv_in, delimiter='\t')
    tsv_labels = tsv_reader.__next__()
    for record in tsv_reader:
        tsv_data.append(record)

# 打印标签
print(csv_labels, '\n')
print(tsv_labels, '\n')
# 打印头10行记录
print(csv_data[0:10], '\n')
print(tsv_data[0:10], '\n')

# ====================================== JSON ======================================
print("====================================== JSON ======================================")
# 第一种方式：使用Pandas
# 读出数据的JSON文件
r_filenameJSON = 'realEstate_trans.json'
w_filenameJSON = 'realEstate_trans.json'
# 读取数据
json_read = pd.read_json(r_filenameJSON, lines=True)
# 打印头10行记录
print(json_read.head(10))

# ====================================== JSON ======================================
print("====================================== JSON ======================================")
# 第二种方式：使用Json
with open(r_filenameJSON, 'r') as json_file:
    jsonread = json.loads(json_file.read())

print(jsonread[-10:])
with open(w_filenameJSON, 'w') as json_file:
    json_file.write(json.dumps(jsonread))

# ====================================== XLSX ======================================
print("====================================== XLSX ======================================")
# 第一种方式：使用Pandas
# 读写数据的文件名
r_filenameXLSX = 'realEstate_trans.xlsx'
w_filenameXLSX = 'realEstate_trans.xlsx'
# 打开Excel文件
xlsx_file = pd.ExcelFile(r_filenameXLSX)
# 读取内容
xlsx_read = {
    sheetName: xlsx_file.parse(sheetName) 
        for sheetName in xlsx_file.sheet_names
}
# 打印Sacramento头10份价格
print (xlsx_read['Sacramento'].head(10)['price'])
# 写入Excel文件
xlsx_read['Sacramento'].to_excel (w_filenameXLSX, 'Sacramento', index=False)

# ====================================== XLSX ======================================
print("====================================== XLSX ======================================")
# 打开Excel文件
xlsx_wb = oxl.load_workbook(filename=r_filenameXLSX)
# 工作簿中所有工作表的名字
sheets = xlsx_wb.get_sheet_names()
# 提取第一列工作表
xlsx_ws = xlsx_wb[sheets[0]]
data = [] # 保存数据的列表

row_label = list(xlsx_ws.rows)[0]
labels = [cell.value for cell in row_label]

rows_without_label = list(xlsx_ws.rows)[1:]
for row in rows_without_label:
    data.append([cell.value for cell in row])
print (
    [item[labels.index('price')] for item in data[0:10]]
)

# ====================================== XML ======================================
print("====================================== XML ======================================")

#读入XML数据，返回pd.DataFrame
def read_xml(xmlFileName):
    with open(xmlFileName, 'r') as xml_file:
        # 读取数据，以树的结构存储
        tree = ET.parse(xml_file)
        # 访问树的根节点
        root = tree.getroot()
        # 返回DataFrame
        return pd.DataFrame(list(iter_records(root)))

# 遍历所有记录的生成器
def iter_records(records):
    for record in records:
        # 保存值的临时字典
        temp_dict = {}
        # 遍历所有字段
        for var in record:
            temp_dict[var.attrib['var_name']] = var.text
        # 生成值
        yield temp_dict

# 以XML格式保存数据
def write_xml(xmlFileName, data):
    with open (xmlFileName, 'w') as xmlFile:
        # 写头部
        xmlFile.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
        )
        xmlFile.write('<records>\n')
        # 写数据
        xmlFile.write(
            '\n'.join(data.apply(xml_encode, axis=1))
        )
        # 写尾部
        xmlFile.write('\n</records>')

# 以特定的嵌套格式将每一行编码成XML 
def xml_encode(row):
    # 第一步——输出record节点
    xmlItem = ['<record>']
    # 第二步——给行中每个字段加上XML格式<field name=…>…</field>
    for field in row.index:
        xmlItem.append(
            ' <var var_name=“{0}”>{1}</var>' \
            .format (field, row[field])
        )
    # 最后一步——标记record节点的结束标签
    xmlItem.append('</record>')
    # 返回一个字符串
    return '\n'.join(xmlItem)

# 读出和写入数据的文件名
r_filenameXML = 'realEstate_trans.xml'
w_filenameXML = 'realEstate_trans_w.xml'

# 读取数据
xml_read = read_xml (r_filenameXML)
# 打印头10行记录
print (xml_read.head(10))
# 以XML格式写回到文件
write_xml(w_filenameXML, xml_read)

# ====================================== SQLITE ======================================
print("====================================== SQLITE ======================================")

r_filenameCSV = 'realEstate_trans.csv'
w_filenameSQLite = 'realEstate_trans.db'

# 创建数据库链接
engine = sa.create_engine(
    'sqlite:///{0}'.format(w_filenameSQLite)
)
# 读取CSV数据
csv_read = pd.read_csv(r_filenameCSV)
# 转换数据格式
csv_read['sale_date'] = pd.to_datetime(csv_read['sale_date'])
# 存储数据到SQLite中
csv_read.to_sql('real_estate', engine, if_exists='replace')
# 打印数据库前10行
query = 'SELECT * FROM real_estate LIMIT 10'
top10 = pd.read_sql_query(query, engine)
print(top10)