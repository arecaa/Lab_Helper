import streamlit as st

st.set_page_config(page_title="실험용 계산기", layout="centered")

# 사이드바 메뉴 선택
menu = st.sidebar.selectbox("기능 선택", ["시딩 계산기", "WB 샘플링 계산기", "희석 계산기"])

# ─────────────────────────────
# 1. 시딩 계산기
# ─────────────────────────────
if menu == "시딩 계산기":
    st.title("🌱 시딩 계산기")

    def parse_input(value):
        value = value.strip().upper()
        if value.endswith("M"):
            return float(value[:-1]) * 1_000_000
        elif value.endswith("K"):
            return float(value[:-1]) * 1_000
        else:
            return float(value)

    cell_conc = st.text_input("1 mL당 세포 수 (예: 1M)")
    target_cells = st.text_input("시딩할 세포 수 (예: 100k)")

    if st.button("계산하기", key="seed"):
        try:
            conc = parse_input(cell_conc)
            target = parse_input(target_cells)
            volume_ul = (target / conc) * 1000
            st.success(f"💡 필요한 시딩 볼륨: **{volume_ul:.2f} µL**")
        except:
            st.error("입력을 확인하세요 (예: 1M, 100k 등)")

# ─────────────────────────────
# 2. WB 샘플링 계산기
# ─────────────────────────────
elif menu == "WB 샘플링 계산기":
    st.title("🧪 WB 샘플링 계산기")

    sample_volume = st.number_input("샘플 볼륨 (µL)", min_value=1.0, value=20.0, step=1.0)

    if st.button("계산하기", key="wb"):
        total_volume = sample_volume / 0.65
        sample_buffer = total_volume * 0.25
        reducing_agent = total_volume * 0.10

        st.markdown(f"""
        💡 **결과:**

        - Sample buffer (4×): **{sample_buffer:.2f} µL**
        - Reducing agent (10×): **{reducing_agent:.2f} µL**
        - 최종 총량: **{total_volume:.2f} µL**
        """)
# ─────────────────────────────
# 3. 희석 계산기
# ─────────────────────────────
elif menu == "희석 계산기":
    st.title("🧬 플라스미드 희석 계산기")

    
    c1 = st.number_input("📈 현재 농도 (ng/µL)", min_value=0.1, value=500.0, step=1.0)
    c2 = st.number_input("🎯 목표 농도 (ng/µL)", min_value=0.1, value=100.0, step=1.0)
    v2 = st.number_input("📦 최종 부피 (µL)", min_value=1.0, value=10.0, step=1.0)

    if st.button("계산하기", key="plasmid_dilution"):
        if c1 < c2:
            st.error("현재 농도가 목표 농도보다 낮으면 희석할 수 없습니다.")
        else:
            v1 = (c2 * v2) / c1
            dw = v2 - v1

            st.success(f"""
            💡 **결과:**

            - 플라스미드: **{v1:.2f} µL**
            - UPW (멸균수): **{dw:.2f} µL**
            - 최종 총량: **{v1 + dw:.2f} µL**
        """)
