import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="経営分析", page_icon="📊", layout="wide")

st.title("📊 利益シミュレーション (損益分岐点分析)")

# -------------------------------------------
# 1. パラメータ入力（サイドバー）
# -------------------------------------------
with st.sidebar:
    st.header("🔢 経営条件の設定")
    
    # 販売単価
    sales_price = st.number_input("ワッフル1個の販売価格 (円)", value=300, step=10)
    
    # 原価（原価計算アプリの結果を参考に入力）
    cost_price = st.number_input("ワッフル1個の原価 (円)", value=80, step=5)
    
    # 固定費（家賃や人件費など、売れなくてもかかるお金）
    fixed_cost = st.number_input("月間の固定費 (円)", value=150000, step=10000, help="家賃、光熱費、システム利用料など")
    
    st.divider()
    
    # シミュレーション範囲
    max_sales_num = st.slider("シミュレーションする販売数 (個/月)", 0, 3000, 1000)

# -------------------------------------------
# 2. 計算ロジック
# -------------------------------------------
# 1個売るごとの利益（限界利益）
profit_per_unit = sales_price - cost_price

if profit_per_unit <= 0:
    st.error("⚠️ 販売価格が原価より安いです！これでは赤字になります。")
    break_even_point = 0
else:
    # 損益分岐点（何個売ればトントンになるか）
    break_even_point = fixed_cost / profit_per_unit

# グラフ用データの作成
sales_nums = list(range(0, max_sales_num + 1, 50)) # 0個から50個刻みで計算
data = []

for num in sales_nums:
    sales_total = sales_price * num       # 売上
    cost_total = fixed_cost + (cost_price * num) # 総費用（固定費＋変動費）
    profit = sales_total - cost_total     # 利益
    
    data.append({
        "販売数": num,
        "金額": sales_total,
        "種類": "売上"
    })
    data.append({
        "販売数": num,
        "金額": cost_total,
        "種類": "総費用"
    })

df = pd.DataFrame(data)

# -------------------------------------------
# 3. 画面表示
# -------------------------------------------

# 重要指標（KPI）の表示
col1, col2, col3 = st.columns(3)
col1.metric("販売単価", f"{sales_price:,} 円")
col2.metric("1個あたりの利益", f"{profit_per_unit:,} 円")
col3.metric("目標販売数 (損益分岐点)", f"{int(break_even_point):,} 個", delta_color="inverse")

st.divider()

# グラフの描画
st.subheader("📈 売上と費用のシミュレーション")

# Plotlyを使ったインタラクティブなグラフ
fig = px.line(df, x="販売数", y="金額", color="種類", 
              title="どこから黒字になる？（線が交わるところが分岐点）",
              color_discrete_map={"売上": "blue", "総費用": "red"})

# 損益分岐点のラインを追加
fig.add_vline(x=break_even_point, line_dash="dash", line_color="green", annotation_text="ここから黒字！")

st.plotly_chart(fig, use_container_width=True)

# アドバイス機能
st.subheader("💡 経営アドバイス")
if break_even_point > max_sales_num:
    st.warning(f"設定した範囲内では黒字になりません。固定費を下げるか、単価を上げる必要があります。")
else:
    st.success(f"月に **{int(break_even_point):,} 個** 以上売れば黒字になります！1日あたり約 **{int(break_even_point/25):,} 個** (25日営業) です。")