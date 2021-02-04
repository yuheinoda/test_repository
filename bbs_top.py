#!/usr/bin/env python3
import sys
import io 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import cgi
form_data = cgi.FieldStorage(keep_blank_values = True)
import MySQLdb
con = None
cur = None
import os
from pathlib import Path
env_path = Path('.') / '.env'
from dotenv import load_dotenv
load_dotenv( dotenv_path = env_path, verbose = True )

def print_html():
    print('<!DOCTYPE html>')
    print('<html>')
    print('<head>')
    print('<meta charset="UTF-8">')
    print('</head>')
    print('<body>')
    print('<p>ひとこと掲示板</p>')
    print('<form action="" method="POST">')
    print('<input type="hidden" name="method_type" value="tweet">')
    print('<input type="text" name="poster_name" value="" placeholder="なまえ">')
    print('<br>')
    print('<textarea name="body_text" value="" placeholder="本文"></textarea>')
    print('<input type="submit" value="投稿">')
    print('</form>')
    print('<hr>')
    sql = "select * from posts"
    cur.execute(sql)
    rows=cur.fetchall()
    for row in rows:
      print('<div class="meta>')
      print('<span class="id">'+ str(row['id'])+ '</span>')
      print('<span class="name">'+str(row ['name'])+ '</span>')
      print('<span class="date">'+str(row ['created_at'])+ '</span>') 
      print('<div>')
      print('<div class="message"><span>'+str(row['body'])+'</span></div>')
    print('</body>')
    print('</html>')

def proceed_methods():
    method = form_data['method_type'].value
    if  (method == 'tweet'):
      poster_name = form_data['poster_name'].value
      body_text  = form_data['body_text'].value
      sql = 'insert into posts (name,body) values (%s,%s)'
      cur.execute(sql,(poster_name,body_text))
      con.commit()
    print('<!DOCTYPE html>')
    print('<html>')
    print('   <head>') 
    print('       <meta http-equiv="refresh" content="5; url=./bbs_top.py">')
    print('   </head>')
    print('   <body>')
    print('       処理が成功しました。5秒後に元のページに戻ります。')    
    print('   </body>')
    print('</html>')






def main():
    print('Content-Type: text/html; charset=utf-8')
    print('')
    global con, cur
    try:
      con = MySQLdb.connect(
       user=str(os.environ.get('bbs_db_user')),
       passwd=str(os.environ.get('bbs_db_passwd')),
       host=os.environ.get('bbs_db_host'),
       db=str(os.environ.get('bbs_db_name')),
       use_unicode = True,
       charset = 'utf8'
       )

    except MySQLdb.Error as e:
      print('データベース接続に失敗しました。')
      print(e)
      exit()

    cur = con.cursor(MySQLdb.cursors.DictCursor)
    if('method_type' in form_data):
      proceed_methods()
    else:
      print_html()

    cur.close
    con.close

if __name__  =="__main__":
    main()     
