"""Craft Cans 数据集 EDA 脚本（Step 3 支持）。
运行后会输出数据概览与关键分布，用于决定仪表盘展示内容。
"""
import pandas as pd

beers = pd.read_csv("data/beers.csv", index_col=0)
breweries = pd.read_csv("data/breweries.csv", index_col=0)

print("=" * 60)
print("1. 数据规模与格式")
print("=" * 60)
print(f"beers.csv:      {beers.shape[0]} 行 x {beers.shape[1]} 列")
print(f"breweries.csv:  {breweries.shape[0]} 行 x {breweries.shape[1]} 列")
print("\nbeers 列类型:")
print(beers.dtypes)
print("\nbreweries 列类型:")
print(breweries.dtypes)

print("\n" + "=" * 60)
print("2. 缺失值")
print("=" * 60)
print("beers:")
print(beers.isna().sum())
print("\nbreweries:")
print(breweries.isna().sum())

print("\n" + "=" * 60)
print("3. 关键分布")
print("=" * 60)
print("\n酒精度 abv 描述统计:")
print(beers["abv"].describe())
print("\n苦度 ibu 描述统计:")
print(beers["ibu"].describe())
print("\n罐装容量 ounces 取值:")
print(beers["ounces"].value_counts())

print("\n啤酒风格 Top 15:")
print(beers["style"].value_counts().head(15))

print("\n酿酒厂所在州 Top 15:")
print(breweries["state"].value_counts().head(15))

print("\n" + "=" * 60)
print("4. 关联关系（按 brewery_id 合并）")
print("=" * 60)
merged = beers.merge(
    breweries, left_on="brewery_id", right_index=True, suffixes=("", "_brewery")
)
print(f"合并后: {merged.shape[0]} 行（beers 中 {beers.shape[0]} 行，"
      f"{merged.shape[0] - beers.shape[0]} 行 brewery_id 无法匹配）")

print("\n各州平均酒精度 (abv) Top 10:")
state_abv = merged.groupby("state")["abv"].mean().sort_values(ascending=False)
print(state_abv.head(10).round(3))

print("\n各州啤酒数量 Top 10:")
print(merged.groupby("state")["name"].count().sort_values(ascending=False).head(10))

print("\n风格数量（合并后）:", merged["style"].nunique())
print("酒厂数量（breweries）:", breweries.shape[0])
