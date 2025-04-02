import http.server
import socketserver
import urllib.parse
import sqlite3
import os

PORT = int(os.environ.get("PORT", 5000))
DATABASE = 'bank_data.db'

tutorials = {
    1: {
        'title': 'SELECT Komutu',
        'description': 'Bu bölümde SELECT komutunun temel kullanımını öğreneceğiz.',
        'question': 'customers tablosundaki tüm verileri listeleyin.',
        'answer_sql': 'SELECT * FROM customers;',
        'answer_explanation': 'SELECT * ifadesi, tablodaki tüm sütunları ve satırları getirir.'
    }
}

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

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        content = tutorials[1]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.build_page(content, '', None).encode("utf-8"))

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        fields = urllib.parse.parse_qs(post_data.decode('utf-8'))
        user_sql = fields.get('sql', [''])[0]
        result = execute_sql(user_sql)
        content = tutorials[1]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.build_page(content, user_sql, result).encode("utf-8"))

    def build_page(self, content, user_sql, result):
        html = f"""
        <html>
        <head>
            <title>SQL Öğren - Soru 1</title>
        </head>
        <body>
            <h1>{content['title']}</h1>
            <p>{content['description']}</p>
            <h3>Soru:</h3>
            <p>{content['question']}</p>
            <form method="POST">
                <textarea name="sql" rows="5" cols="80">{user_sql}</textarea><br>
                <input type="submit" value="Çalıştır">
            </form>
        """
        if result:
            if result['error']:
                html += f"<p style='color:red'>Hata: {result['error']}</p>"
            else:
                html += "<h3>Sonuç:</h3><table border='1'><tr>"
                html += ''.join([f"<th>{col}</th>" for col in result['columns']])
                html += "</tr>"
                for row in result['rows']:
                    html += "<tr>" + ''.join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
                html += "</table>"

        html += f"""
            <hr>
            <h3>Doğru Cevap:</h3>
            <pre>{content['answer_sql']}</pre>
            <p>{content['answer_explanation']}</p>
        </body>
        </html>
        """
        return html

with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
