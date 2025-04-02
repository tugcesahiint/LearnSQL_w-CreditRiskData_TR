from flask import Flask, render_template_string, request
import sqlite3
import nest_asyncio
import os

# Spyder içinde Flask çalıştırmak için gerekli
nest_asyncio.apply()

app = Flask(__name__)

# Her soru için içerik burada tutulabilir veya bir JSON dosyasından yüklenebilir
tutorials = {
    1: {
        'title': 'SELECT Komutu',
        'description': 'Bu bölümde SELECT komutunun temel kullanımını öğreneceğiz.',
        'question': 'customers tablosundaki tüm verileri listeleyin.',
        'answer_sql': 'SELECT * FROM customers;',
        'answer_explanation': 'SELECT * ifadesi, tablodaki tüm sütunları ve satırları getirir.'
    }
}

# SQLite veritabanı bağlantısı
DATABASE = 'bank_data.db'

def execute_sql(sql):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        conn.close()
        return {'columns': columns, 'rows': rows, 'error': None}
    except Exception as e:
        return {'columns': [], 'rows': [], 'error': str(e)}

@app.route('/', methods=['GET', 'POST'])
@app.route('/soru/<int:id>', methods=['GET', 'POST'])
def soru(id=1):
    content = tutorials.get(id)
    result = None
    user_sql = ''

    if request.method == 'POST':
        user_sql = request.form['sql']
        result = execute_sql(user_sql)

    return render_template_string('''
        <html>
        <head>
            <title>SQL Öğren - Soru {{ id }}</title>
        </head>
        <body>
            <h1>{{ content.title }}</h1>
            <p>{{ content.description }}</p>
            <h3>Soru:</h3>
            <p>{{ content.question }}</p>

            <form method="post">
                <textarea name="sql" rows="5" cols="80">{{ user_sql }}</textarea><br>
                <input type="submit" value="Çalıştır">
            </form>

            {% if result %}
                {% if result.error %}
                    <p style="color:red">Hata: {{ result.error }}</p>
                {% else %}
                    <h3>Sonuç:</h3>
                    <table border="1">
                        <tr>
                            {% for col in result.columns %}<th>{{ col }}</th>{% endfor %}
                        </tr>
                        {% for row in result.rows %}
                            <tr>
                                {% for cell in row %}<td>{{ cell }}</td>{% endfor %}
                            </tr>
                        {% endfor %}
                    </table>
                {% endif %}
            {% endif %}

            <hr>
            <h3>Doğru Cevap:</h3>
            <pre>{{ content.answer_sql }}</pre>
            <p>{{ content.answer_explanation }}</p>
        </body>
        </html>
    ''', id=id, content=content, result=result, user_sql=user_sql)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

    app.run(host="0.0.0.0", port=10000)
