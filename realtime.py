import streamlit as st
import pandas as pd
from datetime import datetime

# === ชื่อไฟล์ Excel สำหรับเก็บข้อมูล ===
FILE_NAME = "account_realtime.xlsx"

# === โหลดหรือสร้างไฟล์ใหม่ ===
def load_data():
    try:
        df = pd.read_excel(FILE_NAME)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["วันที่/เวลา", "ประเภท", "รายละเอียด", "รายรับ", "รายจ่าย", "ยอดคงเหลือ"])
        df.to_excel(FILE_NAME, index=False)
    return df

# === บันทึกข้อมูลกลับไปที่ไฟล์ ===
def save_data(df):
    df.to_excel(FILE_NAME, index=False)

# === เริ่มต้นหน้าหลัก ===
st.set_page_config(page_title="บัญชีรายรับรายจ่ายเรียลไทม์ 💰", layout="wide")

st.title("💼 บัญชีรายรับรายจ่ายแบบเรียลไทม์")
st.caption("อัปเดตได้ตลอดเวลา ดูได้ทุกที่ทุกเวลา")

df = load_data()

# --- ส่วนเพิ่มข้อมูลใหม่ ---
with st.form("add_transaction"):
    st.subheader("➕ เพิ่มรายการใหม่")
    t_type = st.selectbox("ประเภท", ["รายรับ", "รายจ่าย"])
    desc = st.text_input("รายละเอียด")
    amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, step=1.0)
    submitted = st.form_submit_button("บันทึกข้อมูล")

    if submitted and amount > 0 and desc:
        last_balance = df["ยอดคงเหลือ"].iloc[-1] if not df.empty else 0
        if t_type == "รายรับ":
            income, expense = amount, 0
            new_balance = last_balance + amount
        else:
            income, expense = 0, amount
            new_balance = last_balance - amount

        new_row = {
            "วันที่/เวลา": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ประเภท": t_type,
            "รายละเอียด": desc,
            "รายรับ": income,
            "รายจ่าย": expense,
            "ยอดคงเหลือ": new_balance
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("✅ บันทึกเรียบร้อย!")

# --- สรุปยอด ---
st.subheader("📊 สรุปยอดรวม")
total_income = df["รายรับ"].sum()
total_expense = df["รายจ่าย"].sum()
balance = df["ยอดคงเหลือ"].iloc[-1] if not df.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("รายรับรวม", f"{total_income:,.2f} บาท")
col2.metric("รายจ่ายรวม", f"{total_expense:,.2f} บาท")
col3.metric("ยอดคงเหลือ", f"{balance:,.2f} บาท")

# --- ตารางรายการทั้งหมด ---
st.subheader("📒 รายการทั้งหมด")
st.dataframe(df, use_container_width=True)
