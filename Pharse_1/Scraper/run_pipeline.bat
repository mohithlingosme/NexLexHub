@echo off
REM NexLexHub Pharse_1 Master Runner + Report Generator

cd /d "%~dp0Script"
echo === Installing Dependencies ===
pip install -r requirements.txt

echo === Testing Pipeline ===
pytest tests/ -v

echo === Running Full Pipeline ===
python Ai_pipelines.py

echo === Generating Report ===
python -c "
import sqlite3
conn = sqlite3.connect('../database/nexlexhub.db')
print('=== PIPELINE REPORT ===')
print('Tables:', conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\";').fetchall())
print('Legal Docs:', conn.execute('SELECT COUNT(*) FROM legal_documents;').fetchone()[0])
print('Sources:', conn.execute('SELECT COUNT(*) FROM source_registry;').fetchone()[0])
print('Sample:', conn.execute('SELECT title, confidence_score FROM legal_documents LIMIT 3;').fetchall())
conn.close()
"

echo === MySQL Dump Ready: Data/Output/nexlexhub_mysql_dump.sql ===
echo Pipeline Complete!
pause

