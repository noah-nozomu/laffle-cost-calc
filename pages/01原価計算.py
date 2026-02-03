import streamlit as st
import pandas as pd

st.set_page_config(page_title="原価計算", page_icon="🧾", layout="wide")
st.title('🧾 原価計算システム')

# -------------------------------------------
# 1. データの準備（セッションステート）
# -------------------------------------------
# 初期データ（デフォルトのマスタ）
default_data = [
    {"材料名": "米粉", "仕入れ値": 540, "単位量": 1000},
    {"材料名": "コーンスターチ", "仕入れ値": 400, "単位量": 1000},
    {"材料名": "片栗粉", "仕入れ値": 200, "単位量": 250},
    {"材料名": "三温糖", "仕入れ値": 300, "単位量": 1000},
    {"材料名": "ベーキングパウダー", "仕入れ値": 380, "単位量": 100},
    {"材料名": "牛乳", "仕入れ値": 240, "単位量": 1000},
    {"材料名": "無糖ヨーグルト", "仕入れ値": 350, "単位量": 400},
    {"材料名": "卵", "仕入れ値": 300, "単位量": 10},
    {"材料名": "米油", "仕入れ値": 750, "単位量": 1300},
    {"材料名": "ココアパウダー", "仕入れ値": 800, "単位量": 200},
    {"材料名": "バニラエッセンス", "仕入れ値": 500, "単位量": 30},
    {"材料名": "抹茶パウダー", "仕入れ値": 1200, "単位量": 100},
]

# まだデータがない場合のみ初期化
if "master_df" not in st.session_state:
    st.session_state.master_df = pd.DataFrame(default_data)

# -------------------------------------------
# 2. 【新機能】データの保存と読み込み
# -------------------------------------------
with st.expander("💾 データの保存・読み込み（続きからやる時はここ！）", expanded=True):
    col_load, col_save = st.columns(2)
    
    # A. 読み込み（ロード）
    with col_load:
        st.subheader("📂 続きから始める")
        uploaded_file = st.file_uploader("保存したCSVファイルをアップロード", type=["csv"])
        if uploaded_file is not None:
            try:
                # アップロードされたファイルを読み込んでマスタを更新
                df_loaded = pd.read_csv(uploaded_file)
                st.session_state.master_df = df_loaded
                st.success("データを復元しました！")
            except Exception as e:
                st.error("ファイルの読み込みに失敗しました。")

    # B. 保存（セーブ）
    with col_save:
        st.subheader("💾 今の状態を保存")
        # データフレームをCSVに変換
        csv = st.session_state.master_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="CSVファイルをダウンロード",
            data=csv,
            file_name='my_ingredients_master.csv',
            mime='text/csv',
            type="primary" # ボタンを目立たせる
        )

# -------------------------------------------
# 3. マスタ編集エリア
# -------------------------------------------
st.divider()
st.subheader("🛠️ 材料マスタの編集")
st.caption("ここで追加・変更した内容は、上のボタンで「CSVダウンロード」して保存してください。")

# 編集可能なデータフレーム
edited_master = st.data_editor(
    st.session_state.master_df,
    num_rows="dynamic",
    key="editor"
)
# 変更を即座に反映
st.session_state.master_df = edited_master

# 計算用に辞書形式に変換
MASTER_DICT = {}
for index, row in st.session_state.master_df.iterrows():
    if row["材料名"]:
        MASTER_DICT[row["材料名"]] = {
            "price": row["仕入れ値"],
            "unit": row["単位量"]
        }

# -------------------------------------------
# 4. レシピ計算エリア（以下、前と同じロジック）
# -------------------------------------------
st.divider()
st.header("📝 レシピ・シミュレーション")

col_setup, col_calc = st.columns([1, 1])

with col_setup:
    st.subheader("① 使う材料を選ぶ")
    base_recipes = {
        "プレーンワッフル": ["米粉", "コーンスターチ", "片栗粉", "三温糖", "ベーキングパウダー", "牛乳", "無糖ヨーグルト", "卵", "米油"],
        "チョコワッフル": ["米粉", "ココアパウダー", "コーンスターチ", "片栗粉", "三温糖", "ベーキングパウダー", "牛乳", "無糖ヨーグルト", "卵", "米油"],
        "カスタム（白紙）": []
    }
    
    selected_template = st.selectbox("ベースにするレシピを選択", list(base_recipes.keys()))
    
    all_ingredients = list(MASTER_DICT.keys())
    default_ingredients = [img for img in base_recipes[selected_template] if img in all_ingredients]
    
    selected_ingredients = st.multiselect(
        "このレシピに使う材料",
        options=all_ingredients,
        default=default_ingredients
    )

with col_calc:
    st.subheader("② 分量を決める")
    total_cost = 0
    details = []

    if not selected_ingredients:
        st.info("👈 左側で材料を選んでください")
    else:
        for ing_name in selected_ingredients:
            data = MASTER_DICT[ing_name]
            c1, c2 = st.columns([2, 1])
            with c1:
                amount = st.number_input(
                    f"{ing_name} (g/個)", 
                    value=0.0, 
                    step=10.0, 
                    key=f"amount_{ing_name}"
                )
            with c2:
                unit_price = data["price"] / data["unit"]
                cost = unit_price * amount
                total_cost += cost
                st.write(f"¥ {int(cost)}")
                
            details.append({
                "材料": ing_name,
                "使用量": amount,
                "単価": f"{data['price']}円/{data['unit']}",
                "原価": int(cost)
            })

st.divider()
st.header(f"💰 合計原価: {int(total_cost):,} 円")
st.metric("1個あたりの原価 (30個製造時)", f"{int(total_cost / 30):,} 円")

with st.expander("詳細な内訳を見る"):
    st.dataframe(pd.DataFrame(details))