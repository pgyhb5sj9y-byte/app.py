import streamlit as st
import pandas as pd

st.set_page_config(page_title="TCST Reefer Risk Control", layout="wide")
st.title("🚢 HỆ THỐNG KIỂM SOÁT RỦI RO CONTAINER LẠNH - TCST")

# Dữ liệu Master Data giả lập từ Hãng tàu
master_data = {
    "TCNU1234567": {"Booking": "BK001", "Temp": -18.0, "Vent": 0},
    "MSKU9876543": {"Booking": "BK002", "Temp": -5.0, "Vent": 15},
}

st.sidebar.header("DANH MỤC QUẢN LÝ")
menu = st.sidebar.radio("Chọn chức năng:", ["1. Kiểm tra Cổng (Smart Gate)", "2. Giám sát Bãi Lạnh (Yard)", "3. Thống kê Sự cố"])

if menu == "1. Kiểm tra Cổng (Smart Gate)":
    st.subheader("📋 Kiểm tra & Đối chiếu Thông tin tại Cổng")
    
    col1, col2 = st.columns(2)
    with col1:
        cont_no = st.text_input("Nhập Số Container:", "TCNU1234567").upper()
        driver_temp = st.number_input("Nhiệt độ Tài xế Khai báo (°C):", value=-18.0, step=0.5)
        driver_vent = st.number_input("Thông gió Khai báo (CBM/h):", value=0)

    if st.button("XÁC NHẬN CHỨNG TỪ GATE"):
        if cont_no in master_data:
            target = master_data[cont_no]
            st.write(f"**Dữ liệu Master Data Hãng tàu:** Nhiệt độ {target['Temp']}°C | Vent {target['Vent']}")
            
            # Kiểm tra thuật toán
            if driver_temp == target['Temp'] and driver_vent == target['Vent']:
                st.success("✅ THÔNG TIN TRÙNG KHỚP! Cho phép xe vào bãi hạ container.")
            else:
                st.error("🚨 CẢNH BÁO SAI LỆCH! Khai báo không khớp với Booking Hãng tàu.")
                st.warning("⚠️ Hệ thống tự động chuyển thông báo rủi ro đến Trưởng ca Bãi Lạnh.")
        else:
            st.error("❌ Không tìm thấy thông tin Container trên hệ thống TOS!")