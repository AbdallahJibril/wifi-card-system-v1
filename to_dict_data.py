class Get_dict_data():
    def __init__(self,data):
        self.data = data
    def to_dict_codes_data(self):
        R = []
        for i in self.data:
            R.append({
                "ID"              :  i[0],
                "code"            :  i[1],
                "max_uses"        :  i[2],
                "used_count"      :  i[3],
                "duration_minutes":  i[4],
                "status"          :  i[5],
                "created_at"      :  i[6],
                "user_id"         :  i[7],
                "username"        :  i[8],
            })
        return R
    def get_codes(self):
        R = []
        for i in self.data:
            R.append( i[1] )
        return R
    def to_dict_admin_data(self):
        R = []
        for i in self.data:
            R.append({
                "ID"       :i[0],
                "name"     :i[1],
                "password" :i[2],
                "add time" :i[3],
            })
        return R
    def to_dict_code_usage_data(self):
        R = []
        for i in self.data:
            R.append({
                "ID"           :i[0],
                "code_id "     :i[1],
                "add_time"     :i[2],
                "ip_address"   :i[3],  
            })
        return R
    def to_dict_logs_data(self):
        R = []
        for i in self.data:
            R.append({
                "ID"        :i[0],
                "created_by":i[1],
                "action"    :i[2],
                "detals"    :i[3],
                "add_time"  :i[4], 
            })
        return R
    # def to_dict_status_codes(self,data2):
    #     # return{
    #     #         "active"   :   self.data[0],
    #     #         "expired"  :   self.data[1],
    #     #         "disabled" :   self.data[2],
    #     # }
    #     return print(data2)


