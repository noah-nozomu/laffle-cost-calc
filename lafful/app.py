import streamlit as st

st.set_page_config(
    page_title="Laffle Management System",
    page_icon="🧇",
    layout="wide"
)

st.title("Laffle 経営管理システムへようこそ 🧇")

st.markdown("""
### このシステムについて
このアプリは、米粉ワッフル店「Laffle」の業務を効率化するために開発されました。
左側のサイドバーから機能を選択してください。

---

#### 👈 機能一覧
* **🧾 原価計算**: レシピの原価をシミュレーションします。材料マスタの管理も可能です。
* **📊 経営分析**: 売上や経費のデータを可視化し、経営状態を分析します。

---
""")

# ちょっとした遊び心：ログインしている気分になる画像
st.image("https://images.unsplash.com/photo-1481434771092-d698c567a57a?q=80&w=2070&auto=format&fit=crop", caption="Make people happy with Waffles!")