import streamlit as st
import pandas as pd
import base64  # 👈 これが必要です！画像変換用のライブラリ

st.set_page_config(layout="wide")
# ==========================================
# 👇 背景画像を自由に切り替える機能（完成版）
# ==========================================

# 1. 画像をCSSで使える形式(Base64)に変換する関数
def get_base64_of_bin_file(bin_file):
    data = bin_file.read()
    return base64.b64encode(data).decode()

# 2. CSSを適用する関数
def set_bg(bg_image_file):
    bin_str = get_base64_of_bin_file(bg_image_file)
    # アップロードされた画像の形式(jpg/png)に合わせておまじないを変える
    ext = "png" if bg_image_file.name.endswith(".png") else "jpg"
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/{ext};base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* 文字を見やすくする設定（前回と同じ） */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label {{
            color: #ffffff !important;
            font-weight: 600 !important;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.8);
        }}
        [data-testid="stMetricValue"] {{
            color: #ffff00 !important;
            font-size: 3rem !important;
            font-weight: 800 !important;
            text-shadow: 3px 3px 5px rgba(0,0,0,1);
        }}
        [data-testid="stMetricLabel"] {{
            color: #ffffff !important;
            background-color: rgba(0,0,0,0.5);
            padding: 5px;
            border-radius: 5px;
        }}
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 3. デフォルト画像を設定する関数（アップロードがない時用）
def set_default_bg(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* 文字設定などは上と同じ（省略せず書くことで適用漏れを防ぐ） */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label {{
            color: #ffffff !important;
            font-weight: 600 !important;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.8);
        }}
        [data-testid="stMetricValue"] {{
            color: #ffff00 !important;
            font-size: 3rem !important;
            font-weight: 800 !important;
            text-shadow: 3px 3px 5px rgba(0,0,0,1);
        }}
        [data-testid="stMetricLabel"] {{
            color: #ffffff !important;
            background-color: rgba(0,0,0,0.5);
            padding: 5px;
            border-radius: 5px;
        }}
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 🎮 画面ロジック：どっちの画像を使うか決める
# ==========================================

# サイドバーにアップロードボタンを設置
uploaded_bg = st.sidebar.file_uploader("🖼️ 背景画像をアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_bg is not None:
    # A. ユーザーが画像をアップロードした場合
    set_bg(uploaded_bg)
else:
    # B. アップロードしていない場合（GitHubのデフォルト画像）
    # ↓ここにさっきのURLを入れてください
    default_url = "https://github.com/noah-nozomu/laffle-cost-calc/blob/main/pg.jpg.jpg?raw=true"
    set_default_bg(default_url)

# ==========================================
# 👆 ここまで
# =========================================

st.set_page_config(layout="wide")
st.title('原価計算システム')

# -------------------------------------------
# 1. データの準備（セッションステートで保存）
# -------------------------------------------
# 初回起動時のみ、初期データを読み込む
if "master_df" not in st.session_state:
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
    st.session_state.master_df = pd.DataFrame(default_data)

# -------------------------------------------
# 2. 仕入れ値の変更エリア（画面上部に配置）
# -------------------------------------------
with st.expander("🛠️ 【マスタ管理】仕入れ値を変える・新しい材料を登録する", expanded=False):
    st.caption("下の一覧を直接書き換えてください。行を追加すると新しい材料になります。")
    # 編集可能なデータフレーム
    edited_master = st.data_editor(
        st.session_state.master_df,
        num_rows="dynamic", # 行の追加・削除を許可
        key="editor"
    )
    # 変更を保存
    st.session_state.master_df = edited_master

# 計算用に辞書形式に変換（プログラムで扱いやすくする）
MASTER_DICT = {}
for index, row in st.session_state.master_df.iterrows():
    if row["材料名"]: # 空行対策
        MASTER_DICT[row["材料名"]] = {
            "price": row["仕入れ値"],
            "unit": row["単位量"]
        }

# -------------------------------------------
# 3. レシピの構成エリア
# -------------------------------------------
st.divider()
st.header("📝 レシピ・シミュレーション")

col_setup, col_calc = st.columns([1, 1])

with col_setup:
    st.subheader("① 使う材料を選ぶ")
    # ベースとなるレシピ（ここも本当はDB化できますが、一旦コードに書きます）
    base_recipes = {
        "プレーンワッフル": ["米粉", "コーンスターチ", "片栗粉", "三温糖", "ベーキングパウダー", "牛乳", "無糖ヨーグルト", "卵", "米油"],
        "チョコワッフル": ["米粉", "ココアパウダー", "コーンスターチ", "片栗粉", "三温糖", "ベーキングパウダー", "牛乳", "無糖ヨーグルト", "卵", "米油"],
        "カスタム（白紙）": []
    }
    
    # テンプレート選択
    selected_template = st.selectbox("ベースにするレシピを選択", list(base_recipes.keys()))
    
    # ★ここがポイント！使う材料を自由に抜き差しできる機能★
    # マスタにある全材料を選択肢にする
    all_ingredients = list(MASTER_DICT.keys())
    # テンプレートの材料を初期値にする
    default_ingredients = [img for img in base_recipes[selected_template] if img in all_ingredients]
    
    # マルチセレクト（タグ選択）で材料を自由に追加・削除
    selected_ingredients = st.multiselect(
        "このレシピに使う材料（追加・削除できます）",
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
        # 選ばれた材料の分量入力欄をズラッと並べる
        for ing_name in selected_ingredients:
            data = MASTER_DICT[ing_name]
            
            # 1行に「入力欄」と「計算結果」を並べる
            c1, c2 = st.columns([2, 1])
            
            with c1:
                # 分量入力
                amount = st.number_input(
                    f"{ing_name} (g または 個)", 
                    value=0.0, 
                    step=10.0, 
                    key=f"amount_{ing_name}"
                )
            
            with c2:
                # 原価計算
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

# -------------------------------------------
# 4. 結果発表エリア
# -------------------------------------------
st.divider()
st.header(f"💰 合計原価: {int(total_cost):,} 円")

# 30個で作った場合の1個あたり
st.metric("1個あたりの原価 (30個製造時)", f"{int(total_cost / 30):,} 円")

# おまけ：詳細テーブル表示
with st.expander("詳細な内訳を見る"):
    st.dataframe(pd.DataFrame(details))
    