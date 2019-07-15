from fateadm_api import FateadmApi


def codepic_to_num(image):
    app_id = '312367'
    app_key = 'c9q4gGEahBxWyRfZNtCHLNJTL1ukclzo'
    pd_id = '112367'
    pd_key = 'PEZ0jJDI0X2QawFdbs9QQWYqoETFU85q'
    a = FateadmApi(app_id=app_id,app_key=app_key,pd_id=pd_id,pd_key=pd_key)
    res = a.PredictExtend(pred_type='10400',img_data=image)
    print ("Score:"+str(a.QueryBalcExtend()))
    return res

def from_flie_to_num(filename):
    app_id = '312367'
    app_key = 'c9q4gGEahBxWyRfZNtCHLNJTL1ukclzo'
    pd_id = '112367'
    pd_key = 'PEZ0jJDI0X2QawFdbs9QQWYqoETFU85q'
    a = FateadmApi(app_id=app_id,app_key=app_key,pd_id=pd_id,pd_key=pd_key)
    res = a.PredictFromFileExtend(pred_type='10400',file_name=filename)
    print ("Score:"+str(a.QueryBalcExtend()))
    return res



# 以下代码仅供测试

# import requests
#
# res = requests.get('http://passport2.chaoxing.com/num/code?1558593660678')
#
# with open('e:/code.png','wb') as f:
#     f.write(res.content)
#
# print (codepic_to_num(res.content))
