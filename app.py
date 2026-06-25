import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import folium
import streamlit.components.v1 as components 

from data_process import generate_data, preprocess_data
from model import cluster_locations

st.set_page_config(page_title="数说商圈 - 商业活力分析", layout="wide")
st.title("🌍 数说商圈：城市商业活力与选址可视化平台")

@st.cache_data
def load_and_process():
    raw_df = generate_data()      
    clean_df = preprocess_data(raw_df) 
    final_df = cluster_locations(clean_df) 
    return final_df

df = load_and_process()

st.sidebar.header("🔍 筛选条件")
selected_cities = st.sidebar.multiselect(
    "选择城市", options=df['city'].unique(), default=['北京', '上海', '广州', '深圳']
)
selected_zones = st.sidebar.multiselect(
    "选择商圈类型", options=df['zone_type'].unique(), default=df['zone_type'].unique()
)
min_rating = st.sidebar.slider("最低评分", 0.0, 5.0, 3.0)

filtered_df = df[
    (df['city'].isin(selected_cities)) & 
    (df['zone_type'].isin(selected_zones)) & 
    (df['rating'] >= min_rating)
]


st.subheader("📊 商业活力关键指标")
col1, col2, col3, col4 = st.columns(4)
col1.metric("总商业网点", len(filtered_df))
col2.metric("平均用户评分", f"{filtered_df['rating'].mean():.2f} 分")
col3.metric("平均情感得分", f"{filtered_df['sentiment_score'].mean():.2f}")
col4.metric("活跃商圈数", filtered_df['zone_type'].nunique())
st.divider()


st.subheader("📍 城市商业地理分布图")

m = folium.Map(location=[35.0, 105.0], zoom_start=4, tiles='cartodbpositron')


try:
    with open('data/china.json', 'r', encoding='utf-8') as f:
        china_data = json.load(f)
    folium.GeoJson(china_data, name='china', style_function=lambda x: {
        'fillColor': '#f0f0f0', 'color': '#d0d0d0', 'weight': 1
    }).add_to(m)
except FileNotFoundError:
    st.warning(" 提示：data文件夹缺少 china.json 文件，地图仅显示圆点，不显示省份轮廓。")

city_colors = {
    '北京': 'red', '上海': 'blue', '广州': 'purple', '深圳': 'orange',
    '杭州': 'green', '成都': 'lightred', '武汉': 'darkblue', '南京': 'darkgreen'
}

for _, row in filtered_df.iterrows():
    city = row['city']
    color = city_colors.get(city, 'gray')
    
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,               
        popup=row['name'],
        tooltip=f"{row['name']} ({row['rating']}分)",
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.7
    ).add_to(m)

m_html = m._repr_html_()
components.html(m_html, width=700, height=500)

st.divider()

st.subheader("📈 数据建模与洞察")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig_box = px.box(
        filtered_df,
        x='city',
        y='sentiment_score',
        color='zone_type',
        points="all",
        title="不同城市店铺情感得分分布对比"
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col_chart2:
    cat_counts = filtered_df.groupby(['city', 'category']).size().reset_index(name='count')
    fig_bar = px.bar(
        cat_counts,
        x='city',
        y='count',
        color='category',
        barmode='group',
        title="不同城市各商业业态数量对比"
    )
    st.plotly_chart(fig_bar, use_container_width=True)


with st.expander("📋 查看筛选后的原始数据"):
    st.dataframe(filtered_df, use_container_width=True)