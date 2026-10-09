import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cấu hình trang web
st.set_page_config(page_title="Quản lý điểm sinh viên", layout="wide")
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. Tạo dữ liệu & tính toán điểm
data = {
    "Ho_ten": ["An", "Bình", "Chi", "Dũng", "Hà", "Lan", "Minh", "Nam", "Phúc", "Trang"],
    "Chuyen_can": [9.0, 8.5, 7.0, 9.5, 8.0, 6.5, 9.0, 7.5, 8.0, 10.0],
    "Giua_ky": [8.0, 8.0, 6.0, 9.0, 7.0, 5.5, 8.5, 6.5, 7.0, 9.0],
    "Cuoi_ky": [7.5, 8.5, 6.5, 9.0, 7.5, 5.5, 8.0, 7.0, 7.5, 9.0]
}
df = pd.DataFrame(data)

# Công thức tính điểm tổng kết: 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
df["Tong_ket"] = (df["Chuyen_can"] * 0.2 + df["Giua_ky"] * 0.3 + df["Cuoi_ky"] * 0.5).round(2)

def xep_loai(diem):
    if diem >= 8.5: return "Giỏi"
    elif diem >= 7.0: return "Khá"
    elif diem >= 5.0: return "Trung bình"
    else: return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 3. Hiển thị bảng điểm
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

# 4. Hiển thị thông tin thống kê
st.subheader("📊 Thống kê chung")
col1, col2, col3, col4 = st.columns(4)

dtb_lop = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()

col1.metric("Điểm TB cả lớp", f"{dtb_lop:.2f}")
col2.metric("Điểm cao nhất", f"{sv_max['Ho_ten']} ({sv_max['Tong_ket']})")
col3.metric("Điểm thấp nhất", f"{sv_min['Ho_ten']} ({sv_min['Tong_ket']})")
col4.metric("Số SV đạt (>=5)", f"{so_sv_dat}/{len(df)}")

st.markdown("---")

# 5. Danh sách chọn sinh viên (Selectbox)
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_sv = st.selectbox("Chọn sinh viên cần xem:", df["Ho_ten"])

sv_info = df[df["Ho_ten"] == selected_sv].iloc[0]
c1, c2, c3, c4, c5 = st.columns(5)
c1.write(f"**Chuyên cần:** {sv_info['Chuyen_can']}")
c2.write(f"**Giữa kỳ:** {sv_info['Giua_ky']}")
c3.write(f"**Cuối kỳ:** {sv_info['Cuoi_ky']}")
c4.write(f"**Tổng kết:** {sv_info['Tong_ket']}")
c5.write(f"**Xếp loại:** {sv_info['Xep_loai']}")

st.markdown("---")

# 6. Biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(df["Ho_ten"], df["Tong_ket"], color='#4C72B0')
ax.set_ylabel("Điểm tổng kết")
ax.set_xlabel("Sinh viên")
ax.set_ylim(0, 10)
ax.axhline(5.0, color='red', linestyle='--', label='Điểm đạt (5.0)')
ax.legend()

st.pyplot(fig)

# 7. Thông tin sinh viên tạo ứng dụng ở cuối trang
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Họ và tên: [Tên của bạn] | MSSV: [Mã số sinh viên của bạn]</p>", unsafe_allow_html=True)
