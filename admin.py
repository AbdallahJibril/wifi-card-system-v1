from codes import Codes as codes
from db import DB , DB_code_usage , DB_logs
from to_dict_data import Get_dict_data
class Admin():
    def __init__(self,db_instance):
        self.db = db_instance
        self.codes = codes
    def add_new_codes(self,Number_of_codes,Number_of_numbers,max_uses,used_count,duratlon_minutes,user_id):
        data_codes = self.db.get_codes()
        codes_list=Get_dict_data(data_codes).get_codes()
        co =self.codes().add_codes(Number_of_codes,Number_of_numbers,codes_list)
        self.db.add_codes(co,max_uses,used_count,duratlon_minutes,user_id)
    def add_admins (self,username,password):
        self.db.add_admins(username,password)
    def add_logs (self,created_by,action,detals_text):
        self.db.add_logs(created_by,action,detals_text)
    def add_code_usage (self,Code_ID,IP_address):
        self.db.add_code_usage(Code_ID,IP_address)
    def view_codes_data (self):
        data =self.db.get_codes()
        return Get_dict_data(data).to_dict_codes_data()
    def view_code_usage(self):
        return self.db.get_code_usage_data()
    def used_count_add1 (self,ID):
        self.db.used_count_add1(ID)
    def Codes_filtering (self,status):
        return self.db.Codes_filtering(status)
    def view_logs(self):
        return self.db.get_logs_data()
    def get_admin(self):
        data =self.db.get_admin_data()
        return  data
    def admin_update_password(self,new_password,ID):
        self.db.admin_update_password(new_password,ID)
    def admin_update_username(self,new_username,ID):
        self.db.admin_update_username(new_username,ID)