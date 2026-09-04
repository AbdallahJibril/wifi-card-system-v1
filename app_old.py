from flask import Flask ,render_template, request , session,url_for,redirect ,flash
from admin import Admin
from db import DB , DB_code_usage , DB_logs 
import time
from flask_jwt_extended import (create_access_token,jwt_manager,create_refresh_token)
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_super_secret_key' # غير ده لمفتاح قوي
#1. بوابة الدخول: بتشيك على المستخدم قبل أي حاجة
@app.before_request
def check_user_login():
    # بنسمح بصفحة اللوجين والملفات الثابتة (CSS/Images)
    allowed_routes = ['index', 'static',"to_login_admin","to_code_user","to_admin","code_user","Create_accunt","add_accunt"]
    
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('index'))
# 2. بوابة الخروج: بتمسح الكاش من المتصفح بعد ما الرد يجهز
@app.after_request
def add_header(response):
    if response.mimetype == 'text/html':
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response
admin_Choose =["عرض كل الاكواد","عرض الاكواد المستخدمه","عرض الاكواد الغير مستخدمخ","عرض سجل النظام"]
settings_Choose =["تغير الاسم","تغير الباسورد"]
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/to_admin", methods=["POST"])
def to_admin():
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          username= request.form.get("username")
          password= request.form.get("password")
          data= admin_db.get_admin()
          for i in data:
                    if i["name"] == username and check_password_hash( i["password"],password):
                         session["username"] =username
                         session["ID"] =i["ID"]
                         detals_text=" تم تسجيل الدخول ادمن "
                         admin_db.add_logs(username,"True",detals_text)
                         #    session["password"] =password
                         return redirect(url_for("adnim_panel"))#
          flash("خطا اسم المستخدم او كلمه السر غير صحيحه")
          detals_text=" عمليه تسجيل دخول فاشله "
          admin_db.add_logs(username,"False",detals_text)
     return redirect(request.referrer)
@app.route("/adnim_panel")
def adnim_panel():
     if 'username' not in session:
          return redirect(url_for("to_login_admin"))
     return render_template("admin.html",Choose=admin_Choose)
@app.route("/to_login_admin")
def to_login_admin():
     return render_template("login_admin.html")
@app.route("/Create_accunt")
def Create_accunt():
     return render_template("Create_accunt.html")
@app.route("/add_accunt", methods=["POST"])
def add_accunt(): 
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          username = request.form.get("uesrname")
          password = request.form.get("password")
          admin_name = [a["name"] for a in admin_db.get_admin()]
          if username in admin_name:
                flash("هذا الاسم مستخدم بالفعل ")
                return redirect(request.referrer)
          password_hash = generate_password_hash(password)
          admin_db.add_admins(username,password_hash)
          admin_db.add_logs(username,"True","تم انشاء حساب جديد")
          for i in admin_db.get_admin() :
               if i["name"] ==username :
                    session["username"] =username
                    session["ID"] =i["ID"]
                    return redirect(url_for("adnim_panel"))

@app.route("/from_sidebar")
def from_sidebar():
    action = request.args.get("action")
    if action == "Homepage":
         return redirect(url_for("adnim_panel"))
    elif action == "add_admin":
         return render_template("add_admin.html")
    elif action == "add_code":
         return render_template("add_code.html")#
    elif action == "disable_code":
         return render_template("disable_code.html")
    elif action == "disable_admin":
         return render_template("disable_admin.html")
    elif action == "settings":
         return render_template("settings.html",settings_Choose=settings_Choose)
    elif action == "log_out":
          session.clear()
          return redirect(url_for('index'))
    else:
         return "خطااا"
@app.route("/add_code", methods=["POST"])
def add_code():
     user_id = session["ID"]
     used_count= 0
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          try :
               Number_of_codes  = int (request.form.get("Number_of_codes"))
               Number_of_numbers= int (request.form.get("Number_of_numbers"))
               max_uses         = int (request.form.get("max_uses"))
               duratlon_minutes = int (request.form.get("duratlon_minutes"))
          except ValueError:
               detals_text="محاوله اضافه اكواد فاشله لسبب ادخاله لحقل غير الارقام "
               admin_db.add_logs(session["username"],"False",detals_text)
               flash("عفوا يجب ادخال جميع الحقول كارقام") 
          try : 
                    if Number_of_numbers >= 6:
                         admin_db.add_new_codes(Number_of_codes,Number_of_numbers,max_uses,used_count,duratlon_minutes,user_id)
                         flash (f" تمت اضافه {Number_of_codes} كود بنجاح")
                         detals_text=f"تم اضافه {Number_of_codes} كود طول الكود {Number_of_numbers} "
                         admin_db.add_logs(session["username"],"True",detals_text)
                    else:
                        flash ("طول الكود يجب ان لا يقل عن 6 ارقام")
                        detals_text="محاوله اضافه اكواد فاشله لسبب قصر طول الكود"
                        admin_db.add_logs(session["username"],"False",detals_text)
          except ValueError: 
                  flash ("حدث خطا فني في السيرفر يرجي المحاوله  لاحقا")
     return redirect(request.referrer)        
@app.route("/add_admin_new" , methods=["POST"])
def add_admin_new():#add_admin
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          username = request.form.get("uesrname")
          password = request.form.get("password")
          names = []
          data=  admin_db.get_admin()
          for i in data:
               names.append(i["name"])
          if username not in names:
               password_hash = generate_password_hash(password)
               admin_db.add_admins(username,password_hash)
               detals_text=f" تم اضافه {username} ادمن"
               admin_db.add_logs(session["username"],"True",detals_text)
               flash (f"تم اضافة {username} ادمن ")
          else:
               detals_text=" عملية اضافه ادمن فاشله لسبب الاسم المضاف مستخدم بالفعل "
               admin_db.add_logs(session["username"],"False",detals_text)          
               flash(" خطا هذا الاسم مستخدم بالفعل ادخل اسم اخر")
     return redirect(request.referrer)
@app.route("/settimgs", methods=["POST"])
def settimgs():
     data = request.form.get("choice")
     if data == "تغير الاسم":
          return render_template("input_new_name.html")
     elif data == "تغير الباسورد":
          return render_template("input_new_password.html")
@app.route("/new_name", methods=["POST"])
def new_name():
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          new_name = request.form.get("new_name")
          admin_db.admin_update_username(new_name,session["ID"])
          flash("تم تغيير الاسم بنجاح")
          detals_text=f" تم تغير اسم المستخدم من {session["username"]} الي {new_name}"
          admin_db.add_logs(session["username"],"True",detals_text)
          session["username"] = new_name
     return  redirect(url_for("adnim_panel"))
@app.route("/new_password", methods=["POST"])
def new_password():
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          old_password     = request.form.get("old_password")
          new_password     = request.form.get("new_password")
          confirm_password = request.form.get("confirm_password")
          data= admin_db.get_admin()
          for i in data:
               if  i["ID"] == session["ID"] :
                    if check_password_hash( i["password"],old_password):
                              if new_password == confirm_password:
                                   password_hash= generate_password_hash(new_password)
                                   admin_db.admin_update_password(password_hash,session["ID"])
                                   admin_db.add_logs(session["username"],"True"," تم تغير كلمه الرسر ")
                                   session.clear()
                                   flash ("تم تغيير كلمه السر بنجاح يجب تسجيل الدخول من جديد")
                                   return redirect(url_for('index'))
                              else :
                                   admin_db.add_logs(session["username"],"False"," عمليه فاشله لتغير كلمه السر")
                                   flash ("تاكد من كتابه واعاده كتابه كلمه السر الجديده") 
                    else :
                          admin_db.add_logs(session["username"],"False"," عمليه فاشله لتغير كلمه السر الخاصه")
                          flash ("قم بادخال كلمه السر القديمه صحصح")
          return redirect(url_for("adnim_panel"))
@app.route("/to_code_user")
def to_code_user():
    return render_template("input_code_user.html")
@app.route("/code_user", methods=["POST"])
def code_user():
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          code = request.form.get("code")
          data= admin_db.view_codes_data()
          for i in data:
                    if i["code"]== code:
                         if i["status"] =="active":
                                   flash( "تم تسجيل الدخول بنجاح")
                                   admin_db.used_count_add1(i["ID"])
                                   admin_db.add_logs(code,"True","تم تسجيل دخول بستخدام كود ")
                                   return redirect(request.referrer)
                         elif i["status"] =="disabled":
                                   flash( "لقد  اوقف المالك هذا الكود" )
                                   admin_db.add_logs(code,"False","محاوله تسجيل بستخدام الكود  فاشله لسبب ايقاف للكود")
                                   return redirect(request.referrer)
                         else:
                                   flash( "تم انتهاء هذا الكود" )
                                   admin_db.add_logs(code,"False","محاوله تسجيل بستخدام الكود فاشله لسبب انتهاء الكود")
                                   return redirect(request.referrer)
          flash( "لقد ادخلت الكود بشكل غير صحيح" )
          admin_db.add_logs(code,"False"," عمليه تسجيل غير صحيحه بستخدام كود")
     return redirect(request.referrer)
@app.route("/admin_choose",methods=["POST"])
def admin_choose():
     with DB() as database_connection:
          admin_db = Admin(db_instance=database_connection)
          data = admin_db.view_codes_data()
          admin_choose = request.form.get("Choose")
          active=[]
          expired=[]
          for i in data:
                    if i["status"] =="active":
                         active.append(i)
                    elif i["status"] =="expired":
                         expired.append(i)
          if admin_choose ==  "عرض كل الاكواد":
               return render_template("view_codes.html",data_code=data)
          elif admin_choose =="عرض الاكواد المستخدمه":
               return render_template("view_codes.html",data_code=expired)
          elif admin_choose =="عرض الاكواد الغير مستخدمخ":
               return render_template("view_codes.html",data_code=active)
          elif admin_choose =="عرض سجل النظام":
               data2= admin_db.view_logs()
               return render_template("view_logs.html",data2=data2)
          else :
               return "خطا في اختيار الادمن "

if __name__ == "__main__":
    app.run(debug=True)