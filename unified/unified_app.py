import streamlit as st
import requests
from flask import Flask, request, jsonify
import threading

# --- Flask API ---
app = Flask(__name__)

@app.route('/add', methods=['GET'])
def add():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    return jsonify({'result': a + b})

@app.route('/subtract', methods=['GET'])
def subtract():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    return jsonify({'result': a - b})

@app.route('/multiply', methods=['GET'])
def multiply():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    return jsonify({'result': a * b})

@app.route('/divide', methods=['GET'])
def divide():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 1))
    if b == 0:
        return jsonify({'error': 'Division by zero'}), 400
    return jsonify({'result': a / b})

# --- 啟動 Flask 於背景執行 ---
def run_flask():
    app.run(host='0.0.0.0', port=5000)

threading.Thread(target=run_flask, daemon=True).start()

# --- Streamlit 前端 ---
st.set_page_config(page_title="簡易計算機", page_icon="🧮")
st.title("簡易計算機 (Flask+Streamlit)")

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("數字 A", value=0.0, format="%f")
with col2:
    b = st.number_input("數字 B", value=0.0, format="%f")

op = st.selectbox("運算", ["加法", "減法", "乘法", "除法"])

if st.button("計算"):
    op_map = {"加法": "add", "減法": "subtract", "乘法": "multiply", "除法": "divide"}
    url = f"http://localhost:5000/{op_map[op]}?a={a}&b={b}"
    try:
        resp = requests.get(url, timeout=3)
        data = resp.json()
        if "result" in data:
            st.success(f"結果：{data['result']}")
        elif "error" in data:
            st.error(f"錯誤：{data['error']}")
        else:
            st.warning("未知錯誤")
    except Exception as e:
        st.error(f"API 請求失敗: {e}")
