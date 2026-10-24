"""Craft Cans 选品仪表盘 —— Streamlit 应用。

面向精酿啤酒选品经理的决策仪表盘：
- 快速掌握在售啤酒货架概况（数量、酒精度、苦度）
- 按风格查看供应布局是否均衡
- 按州查看区域酒厂集中度

数据：Craft Cans Dataset (Kaggle: nickhould/craft-cans)
数据期：2017 年 1 月快照（Kaggle）
"""
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Craft Cans 选品仪表盘", layout="wide")

# ---------------------------------------------------------------------------
# 数据加载（缓存）
# ---------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    beers = pd.read_csv("data/beers.csv", index_col=0)
    breweries = pd.read_csv("data/breweries.csv", index_col=0)
    # 按 brewery_id 关联，得到每款啤酒的州/城市信息
    df = beers.merge(
        breweries[["name", "city", "state"]],
        left_on="brewery_id",
        right_index=True,
        suffixes=("", "_brewery"),
    )
    return df


df = load_data()

# ---------------------------------------------------------------------------
# 标题与说明（Step 5 要求 1 & 2）
# ---------------------------------------------------------------------------
st.title("精酿啤酒选品仪表盘")
st.caption(
    "面向精酿啤酒选品经理 —— 支持「该进哪些风格/区域的啤酒」的选品决策。"
    "如果选品经理看到某风格或区域供应过剩/空白，就会调整采购清单。"
)

# ---------------------------------------------------------------------------
# 数据期与刷新频率说明（Step 4 要求）
# ---------------------------------------------------------------------------
st.info(
    "**数据期**：2017 年 1 月，Kaggle 快照（craft-cans）。"
    "**建议刷新频率**：按月刷新（精酿新品多为季度/月度上新，选品决策每月评审一次）。"
)

# ---------------------------------------------------------------------------
# 侧边栏筛选器（Step 5 要求 5）
# ---------------------------------------------------------------------------
st.sidebar.header("筛选条件")

# 风格筛选（多选，默认全选）
all_styles = sorted(df["style"].dropna().unique())
selected_styles = st.sidebar.multiselect(
    "啤酒风格", options=all_styles, default=all_styles
)

# 酒精度范围滑块（abv 是比例值，乘以 100 转为百分数显示）
abv_min = float(df["abv"].min()) * 100
abv_max = float(df["abv"].max()) * 100
abv_range = st.sidebar.slider(
    "酒精度 (abv, %)",
    min_value=round(abv_min, 1),
    max_value=round(abv_max, 1),
    value=(round(abv_min, 1), round(abv_max, 1)),
)

# 应用筛选（把百分数还原为比例值）
filtered = df[
    (df["style"].isin(selected_styles))
    & (df["abv"].between(abv_range[0] / 100, abv_range[1] / 100))
]

# ---------------------------------------------------------------------------
# 核心指标（Step 5 要求 3，Step 3：最多 3 个）
# ---------------------------------------------------------------------------
st.subheader("货架概况")
c1, c2, c3 = st.columns(3)
c1.metric("在售啤酒数", f"{len(filtered):,}")
c2.metric("平均酒精度 (abv)", f"{filtered['abv'].mean() * 100:.1f}%")
c3.metric("平均苦度 (ibu)", f"{filtered['ibu'].mean():.0f}")

# ---------------------------------------------------------------------------
# 支撑图表（Step 5 要求 4）
# ---------------------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("各风格啤酒数量 (Top 15)")
    style_counts = filtered["style"].value_counts().head(15)
    st.bar_chart(style_counts)

with right:
    st.subheader("各州酿酒厂数量 (Top 15)")
    # 每个州有多少家不同酒厂
    state_brewery_counts = (
        filtered.groupby("state")["name_brewery"]
        .nunique()
        .sort_values(ascending=False)
        .head(15)
    )
    st.bar_chart(state_brewery_counts)

# ---------------------------------------------------------------------------
# 底部明细表（Step 3：为想深挖的人准备，可折叠）
# ---------------------------------------------------------------------------
with st.expander("查看明细数据（前 200 条）"):
    st.dataframe(
        filtered[
            ["name", "style", "abv", "ibu", "ounces", "name_brewery", "city", "state"]
        ].head(200),
        use_container_width=True,
    )
