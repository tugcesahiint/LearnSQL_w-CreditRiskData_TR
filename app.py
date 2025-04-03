from flask import Flask, send_from_directory, request, jsonify
import openai
import os

app = Flask(__name__, static_folder='static')

# Ana sayfa
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# GPT ile SQL cevabı kontrol eden endpoint
@app.route('/api/check-sql', methods=['POST'])
def check_sql():
    data = request.json
    user_sql = data.get("user_sql", "")
    correct_sql = data.get("correct_sql", "")

    prompt = f"""
Sen bir SQL eğitmenisin. Aşağıdaki iki sorgunun **aynı sonucu üretip üretmediğini** kontrol et. 
Yazım farklarına değil, anlam farkına dikkat et. 
Sadece "DOĞRU" veya "YANLIŞ" yaz.

Doğru SQL: {correct_sql}
Kullanıcının SQL'i: {user_sql}
"""

    openai.api_key = os.getenv("OPENAI_API_KEY")  # API anahtarını güvenli tut
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        result = response["choices"][0]["message"]["content"].strip()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Uygulama sunucusu
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
