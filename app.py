import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="TCST Reefer Risk Control", page_icon="🚢", layout="wide")

# Tiêu đề ứng dụng
st.title("🚢 HỆ THỐNG QUẢN LÝ VÀ KIỂM SOÁT RỦI RO CONTAINER LẠNH (TCST-RRM)")
st.markdown("---")

# Menu điều hướng bên thanh sidebar
st.sidebar.header("DANH MỤC CHỨC NĂNG")
menu = st.sidebar.radio(
    "Chọn Module:", 
    [
        "1. Kiểm tra Cổng (Smart Gate)", 
        "2. Giám sát Bãi Lạnh (Reefer Yard)", 
        "3. Thống kê Sự cố & Phân tích"
    ]
)

# ----------------- TAB 1: KIỂM TRA CỔNG -----------------
if menu == "1. Kiểm tra Cổng (Smart Gate)":
    st.subheader("📋 Phân hệ Kiểm soát Cổng: Đối chiếu Thông tin Hàng lạnh")
    
    # Dữ liệu Master Data giả lập nhiều container
    master_data = {
        "TCNU1234567": {"Booking": "BK-2026-01", "Temp": -18.0, "Vent": 0, "Line": "ONE", "Cargo": "Thủy hải sản đông lạnh"},
        "MSKU9876543": {"Booking": "BK-2026-02", "Temp": -5.0, "Vent": 15, "Line": "Maersk", "Cargo": "Thực phẩm tươi sống"},
        "CMAU4561238": {"Booking": "BK-2026-03", "Temp": -20.0, "Vent": 0, "Line": "CMA CGM", "Cargo": "Thịt đông lạnh"},
        "HLBU7894561": {"Booking": "BK-2026-04", "Temp": 2.0, "Vent": 25, "Line": "Hapag-Lloyd", "Cargo": "Trái cây tươi"}
    }

    col1, col2 = st.columns(2)
    with col1:
        cont_no = st.selectbox("Chọn hoặc Nhập Số Container đến Cổng:", list(master_data.keys()))
        driver_temp = st.number_input("Nhiệt độ Tài xế Khai báo (°C):", value=-18.0, step=0.5)
        driver_vent = st.number_input("Thông gió Tài xế Khai báo (CBM/h):", value=0, step=5)

    with col2:
        st.info("💡 **Quy tắc kiểm tra tự động (Smart Gate):**\nHệ thống sẽ tự động đối chiếu thông số thực tế từ tài xế với Master Data của Hãng tàu nhằm chặn lỗi sai lệch nhiệt độ trước khi cho xe hạ bãi.")

    if st.button("🔍 XÁC THỰC THÔNG TIN & CẤP GATE PASS", type="primary"):
        target = master_data[cont_no]
        st.markdown("---")
        st.write(f"**📦 Thông tin Hàng hóa:** {target['Cargo']} | **Hãng tàu:** {target['Line']} | **Booking:** {target['Booking']}")
        st.write(f"**🎯 Yêu cầu chuẩn từ Hãng tàu:** Nhiệt độ: `{target['Temp']}°C` | Thông gió: `{target['Vent']} CBM/h`")
        
        # Kiểm tra điều kiện
        if driver_temp == target['Temp'] and driver_vent == target['Vent']:
            st.success("✅ THÔNG TIN TRÙNG KHỚP HOÀN TOÀN! Trạng thái: AN TOÀN. Cho phép xe vào bãi hạ container.")
            st.metric(label="Mã định danh Gate Pass", value="GP-2026-8891", delta="Hợp lệ")
        else:
            st.error("🚨 CẢNH BÁO SAI LỆCH (RED ALERT)! Thông tin khai báo không khớp với Booking hãng tàu.")
            st.warning("⚠️ **Hành động tự động:** Hệ thống đã khóa mã Gate Pass, gửi thông báo khẩn đến Trưởng ca bãi lạnh và yêu cầu kiểm tra thực tế (PTI lại) tại cổng.")

# ----------------- TAB 2: GIÁM SÁT BÃI LẠNH -----------------
elif menu == "2. Giám sát Bãi Lạnh (Reefer Yard)":
    st.subheader("⚡ Phân hệ Giám sát Trạng thái Điện & Nhiệt độ Bãi Lạnh (Reefer Yard)")
    st.write("Dưới đây là danh sách các container lạnh đang hạ bãi và trạng thái cấp nguồn thời gian thực (Real-time Dashboard):")

    # Tạo bảng dữ liệu giả lập nhiều container trong bãi
    yard_data = pd.DataFrame({
        "Container No": ["TCNU1234567", "MSKU9876543", "CMAU4561238", "HLBU7894561", "OOLU5544332"],
        "Vị trí Bãi": ["RF-01-04-2", "RF-02-12-1", "RF-01-05-3", "RF-03-08-2", "RF-02-01-4"],
        "Cài đặt (°C)": [-18.0, -5.0, -20.0, 2.0, -15.0],
        "Thực tế (°C)": [-17.8, -4.9, -20.0, 3.5, -15.0],
        "Trạng thái Cắm điện": ["Đã cắm ổn định", "Đã cắm ổn định", "Đã cắm ổn định", "⚠️ Lệch nhiệt độ", "Đã cắm ổn định"],
        "Thời gian từ khi hạ (phút)": [25, 40, 15, 65, 10]
    })

    # Hiển thị bảng dạng interactive
    st.dataframe(yard_data, use_container_width=True)

    st.markdown("---")
    st.subheader("🛠️ Cập nhật Kiểm tra Thực địa (Dành cho Công nhân bãi)")
    selected_cont = st.selectbox("Chọn Container cần ghi nhận sự cố:", yard_data["Container No"])
    check_status = st.selectbox("Đánh giá tình trạng phích cắm & đồng hồ:", ["Bình thường, hoạt động tốt", "Phích cắm lỏng/hư hỏng", "Nhiệt độ vượt ngưỡng cho phép", "Mất nguồn điện cấp"])
    
    if st.button("GHI NHẬN VÀO HỆ THỐNG TOS"):
        st.success(f"Đã cập nhật trạng thái mới cho container **{selected_cont}** vào cơ sở dữ liệu trung tâm thành công!")

# ----------------- TAB 3: THỐNG KÊ SỰ CỐ & PHÂN TÍCH -----------------
elif menu == "3. Thống kê Sự cố & Phân tích":
    st.subheader("📊 Phân hệ Thống kê Sự cố & Phân tích Rủi ro (Incident Analytics)")
    st.write("Báo cáo tỷ lệ các nguyên nhân gây sai sót trong quy trình nhận container hàng lạnh tại TCST:")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tổng số Container lạnh xử lý tháng qua", value="1,245", delta="+12% so với tháng trước")
        st.metric(label="Tỷ lệ sự cố/sai sót ghi nhận", value="2.4%", delta="-0.8% (Cải thiện)", delta_color="inverse")
    
    with col2:
        st.metric(label="Thời gian xử lý trung bình mỗi xe", value="8.5 phút", delta="-2 phút")
        st.metric(label="Chỉ số Rủi ro Tổng hợp (RRS)", value="0.18 / 1.00", delta="Mức an toàn")

    st.markdown("---")
    st.subheader("📈 Biểu đồ Tỷ lệ các loại Sự cố thường gặp")
    
    # Dữ liệu vẽ biểu đồ thống kê nguyên nhân sự cố
    chart_data = pd.DataFrame(
        {
            "Tỷ lệ (%)": [45, 30, 15, 10],
        },
        index=["Sai lệch nhiệt độ/thông gió khai báo", "Chậm trễ cắm điện sau khi hạ bãi", "Lỗi chứng từ/Booking hãng tàu", "Hư hỏng phích cắm/vỏ container (PTI)"]
    )
    
    st.bar_chart(chart_data)
    st.info("📌 **Gợi ý đưa vào báo cáo Word:** Biểu đồ này chứng minh lý do tại sao Chương 2 và Chương 3 của nhóm phải tập trung vào 2 hạn chế lớn nhất là *Lỗi thông tin khai báo tại cổng* và *Lỗi thao tác/độ trễ hiện trường*.")
