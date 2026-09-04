from db_connection import DBConnection as con
from to_dict_data import Get_dict_data

class DB_logs():
    def add_logs(self,created_by,action,detals_text):
        cur =self.cursor()
        sql ="INSERT INTO logs(created_by,action,detals) VALUES (%s,%s,%s);"
        data =(created_by,action,detals_text)
        cur.execute(sql,data)
        self.commit()
    def get_logs_data(self):
        R=[]
        cur =self.cursor()
        cur.execute("SELECT id,created_by, action, detals, created_at FROM logs")
        v =cur.fetchall()
        for i in v:
            R.append(i)
        return Get_dict_data(R).to_dict_logs_data()

#*************************************************************************************************************
class DB_code_usage():
    def add_code_usage(self,Code_ID,IP_address):
        cur =self.cursor()
        sql ="INSERT INTO code_usage(code_id,ip_address) VALUES (%s,%s);"
        data =(Code_ID,IP_address)
        cur.execute(sql,data)
        self.commit()
    def get_code_usage_data(self):
        R=[]
        cur =self.cursor()
        cur.execute("SELECT id, code_id, used_at, ip_address FROM code_usage")
        v =cur.fetchall()
        for i in v:
            R.append(i)
        cur.fetchall()
        return 
#*************************************************************************************************************
class DB(con,DB_code_usage,DB_logs):
    def __init__(self):
        super().__init__()
    def add_codes(self,codes,max_uses,used_count,duratlon_minutes,user_id):
        cur = self.cursor()
        for i in codes:
            sql="INSERT INTO codes(code, max_uses, used_count, duratlon_minutes , user_id) VALUES (%s,%s,%s,%s,%s)"
            data = (i,max_uses,used_count,duratlon_minutes , user_id)
            cur.execute(sql,data)
        self.commit()
    def get_codes(self):
        cur = self.cursor()
        cur.execute("SELECT codes.*, admins.username FROM codes JOIN admins ON codes.user_id =admins.id")
        R =cur.fetchall()
        return R #Get_dict_data(R).to_dict_admin_data()
    def get_admin_data(self):
        R =[]
        cur =self.cursor()
        cur.execute(" SELECT id, username, password, created_at FROM admins ")
        v =cur.fetchall()
        for i in v:
            R.append(i)
        cur.fetchall()
        return Get_dict_data(R).to_dict_admin_data() 
    def Codes_filtering(self,status):
        cur = self.cursor()
        sql ="SELECT id , code , max_uses , used_count , duratlon_minutes , status , created_at FROM codes WHERE status =%s;"
        data =(status)
        cur.execute(sql,data)
        R =cur.fetchall()
        return Get_dict_data(R).to_dict_codes_data()
    def ubdate_status_admin(self,ID,status):
        cur = self.cursor()
        sql  ="UPDATE codes SET status=%s WHERE id=%s;"
        data =(status,ID) 
        cur.execute(sql,data)
        self.commit()
    def used_count_add1 (self,ID):
        cur = self.cursor()
        sql  ="UPDATE codes SET used_count=(used_count +1) WHERE id=%s;"
        data =(ID,) 
        cur.execute(sql,data)
        self.commit()
    def add_admins(self,username,password):
        cur = self.cursor()
        sql="INSERT INTO admins(username,password) VALUES (%s,%s);"
        data=(username,password)
        cur.execute(sql , data)
        self.commit()
    def admin_update_password(self,new_password,ID):
        cur = self.cursor()
        sql= "UPDATE admins SET password = %s WHERE id= %s;"
        data=(new_password,ID)
        cur.execute(sql,data)
        self.commit()
    def admin_update_username(self,new_username,ID):
        cur = self.cursor()
        sql= "UPDATE admins SET username = %s WHERE id= %s;"
        data=(new_username,ID)
        cur.execute(sql,data)
        self.commit()


