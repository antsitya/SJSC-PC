#coding=GBK

import urllib
import urllib2
import cookielib
import bs4
from urllib import quote
import codecs
import re
import cgi,cgitb

form=cgi.FieldStorage()
print
class student:
    
    def __init__(self,num,pw,xuenian,xueqi,clicka):

        self.num=num
        self.state=True
        self.pw=pw
        self.arvpoint=0.0
        self.name=''
        self.banji=''
        self.zhuanye=''
        self.xueyuan=''
        self.grade=[]
        self.xuenian=xuenian
        self.xueqi=xueqi
        if clicka=="按学年查询":
            self.click="Button5"
        if clicka=="按学期查询":
            self.click="Button1"
        if clicka=="在校学习成绩查询":
            self.click="Button2"
        self.clicka=clicka
#         self.click="Button5"
#         self.clicka="按学年查询"
        self.status = False
    filename ='xinxi.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
    def zhuan(st):
        if not isinstance(st,unicode):   #检查编码是否为unicode  
            obj = unicode(st,'gbk')
            st=''.join(obj).encode('utf8')
        else:
            st=''.join(st).encode('utf8')
        return st
    def login(self):
        loginurl='http://218.94.104.201:85/default6.aspx'
        datas = {
            '__VIEWSTATE':'dDwtMTQxNDAwNjgwODt0PDtsPGk8MD47PjtsPHQ8O2w8aTwyMT47aTwyMz47aTwyNT47aTwyNz47PjtsPHQ8cDxsPGlubmVyaHRtbDs+O2w8Oz4+Ozs+O3Q8cDxsPGlubmVyaHRtbDs+O2w8Oz4+Ozs+O3Q8cDxsPGlubmVyaHRtbDs+O2w8Oz4+Ozs+O3Q8cDxsPGlubmVyaHRtbDs+O2w8Oz4+Ozs+Oz4+Oz4+Oz59envE1UwQehRVvzVOfsZyW7fzvQ==',
            'txtYhm':self.num,
            'txtMm':self.pw,
            'rblJs': '学生',
            'btnDl': '登录'
        }
        postdata = urllib.urlencode(datas)
        
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        self.opener.addheaders.append( ('Host', 'yjsgl.fzu.edu.cn') )
        self.opener.addheaders.append( ('User-Agent', user_agent) )
        self.opener.addheaders.append( ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8') )
        self.opener.addheaders.append( ('Accept-Language', 'zh-CN,zh;q=0.8') )
        self.opener.addheaders.append( ('Accept-Encoding', 'gzip, deflate') )
        self.opener.addheaders.append( ('Connection', 'keep-alive') )
        self.opener.addheaders.append( ('Referer', 'http://218.94.104.201:85/default6.aspx') )
        try:
            result = self.opener.open(loginurl,postdata)
        except self.opener.URLError, e: 
            print e.reason()         
        self.cookie.save(ignore_discard=True, ignore_expires=True)
#         print result.read()
        cd = bs4.BeautifulSoup(result.read(), 'html.parser')
        titles=cd.find('title').get_text()
#         print titles
#         print type(titles)
        title01=u"正方教务管理系统"
#         print title01
#         print type(title01)
        print '{',
#         print '{'+'"name":"'+self.name+'","xueyuan":"'+self.xueyuan+'","zhuanye":"'+self.zhuanye+'","banji":"'+self.banji+'",',
        if titles == title01:
            try:
                name = cd.find('span', id='xhxm').get_text()
            except Exception as e:
                self.status = False
                return
            self.status = True
            self.name = name[:-2]
    #         print self.name
            gbk_string=self.name.encode("gbk")
            gbk=quote(gbk_string)
    #         print gbk
    
    #         print result.read()
            
            gradeUrl = 'http://218.94.104.201:85/xscj.aspx?xh='+self.num+'&xm='+gbk+'&gnmkdm=N121605'
#             print gradeUrl
            result1 = self.opener.open(gradeUrl)
    #         print result1 .read()
            
            find_values = bs4.BeautifulSoup(result1.read(), "html.parser").find('input')['value']
    #         print find_values
            finddatas = {
                '__VIEWSTATE': find_values,
                'ddlXN':self.xuenian,
                'ddlXQ':self.xueqi,
                'txtQSCJ':'0',
                'txtZZCJ':'100',
    #             'Button1':'按学期查询'
#                 'Button5':'按学年查询'
                self.click:self.clicka
                }
            postdatas1 = urllib.urlencode(finddatas)
            result2 = self.opener.open(gradeUrl,postdatas1)
            news=self.name+'    '+self.num+'    '+self.pw+'\n'
            filename ='学生信息.txt'
            f=codecs.open(filename,'a+','gbk')
            states=True
            for i in f:  
                if not isinstance(i,unicode):   #检查编码是否为unicode  
                    obj = unicode(i,'utf-8')
                    x=''.join(obj).encode('gbk')
                else:
                    x=''.join(i).encode('gbk')
                y=''.join(news).encode('gbk')
                y=y[:-1]
                x=x[:-2]
                if x==y:
                    states=False
            f.close()
            if states==True:
                f=open(filename,"a+")
                f.write(''.join(news).encode('gbk'))
            f.close()
            scorehtml=result2.read()
    #         print type(scorehtml)
            scorehtmls= bs4.BeautifulSoup(scorehtml, 'html.parser')
            self.xueyuan=scorehtmls.find('span', id='Label6').get_text()[3:]
            self.zhuanye=scorehtmls.find('span', id='Label7').get_text()
            self.banji=scorehtmls.find('span', id='Label8').get_text()[4:]
            tables=scorehtmls.find('table', id='DataGrid1').find_all('tr')[1:]
            
            if not isinstance(self.name,unicode):   #检查编码是否为unicode  
                obj = unicode(self.name,'gbk')
                self.name=''.join(obj).encode('utf8')
            else:
                self.name=''.join(self.name).encode('utf8')
            if not isinstance(self.xueyuan,unicode):   #检查编码是否为unicode  
                obj = unicode(self.xueyuan,'gbk')
                self.xueyuan=''.join(obj).encode('utf8')
            else:
                self.xueyuan=''.join(self.xueyuan).encode('utf8')
            if not isinstance(self.zhuanye,unicode):   #检查编码是否为unicode  
                obj = unicode(self.zhuanye,'gbk')
                self.zhuanye=''.join(obj).encode('utf8')
            else:
                self.zhuanye=''.join(self.zhuanye).encode('utf8')
            if not isinstance(self.banji,unicode):   #检查编码是否为unicode  
                obj = unicode(self.banji,'gbk')
                self.banji=''.join(obj).encode('utf8')
            else:
                self.banji=''.join(self.banji).encode('utf8')
            
            print '"name":"'+self.name+'","xueyuan":"'+self.xueyuan+'","zhuanye":"'+self.zhuanye+'","banji":"'+self.banji+'",',
            scorestr=""
            for str in tables:
                scorestr=scorestr+str.encode('gbk')
    #         print scorestr
            string=u"<tr.*?>\n<td>.*?<td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td><td>([\u4e00-\u9fa5_a-zA-Z0-9]*.*?)</td>"       
            
            pattern = re.compile(string,re.S)
            matchs = pattern.findall(scorestr)
    #         print matchs
            spoint_sum=0
            credit_sum=0
            index=1
            
            for i in matchs:
                #转码
                s1=i[0]
                if not isinstance(s1,unicode):   #检查编码是否为unicode  
                    obj = unicode(s1,'gbk')
                    s1=''.join(obj).encode('utf8')
                else:
                    s1=''.join(s1).encode('utf8')
                s2=i[1]
                if not isinstance(s2,unicode):   #检查编码是否为unicode  
                    obj = unicode(s2,'gbk')
                    s2=''.join(obj).encode('utf8')
                else:
                    s2=''.join(s2).encode('utf8')
                s3=i[2]
                if not isinstance(s3,unicode):   #检查编码是否为unicode  
                    obj = unicode(s3,'gbk')
                    s3=''.join(obj).encode('utf8')
                else:
                    s3=''.join(s3).encode('utf8')
                s4=i[3]
                if not isinstance(s4,unicode):   #检查编码是否为unicode  
                    obj = unicode(s4,'gbk')
                    s4=''.join(obj).encode('utf8')
                else:
                    s4=''.join(s4).encode('utf8')
                s5=i[4]
                if not isinstance(s5,unicode):   #检查编码是否为unicode  
                    obj = unicode(s5,'gbk')
                    s5=''.join(obj).encode('utf8')
                else:
                    s5=''.join(s5).encode('utf8')
                s6=i[5]
                if not isinstance(s6,unicode):   #检查编码是否为unicode  
                    obj = unicode(s6,'gbk')
                    s6=''.join(obj).encode('utf8')
                else:
                    s6=''.join(s6).encode('utf8')
                s7=i[6]
                if not isinstance(s7,unicode):   #检查编码是否为unicode  
                    obj = unicode(s7,'gbk')
                    s7=''.join(obj).encode('utf8')
                else:
                    s7=''.join(s7).encode('utf8')
                s8=i[7]
                if not isinstance(s8,unicode):   #检查编码是否为unicode  
                    obj = unicode(s8,'gbk')
                    s8=''.join(obj).encode('utf8')
                else:
                    s8=''.join(s8).encode('utf8')
                s9=i[8]
                if not isinstance(s9,unicode):   #检查编码是否为unicode  
                    obj = unicode(s9,'gbk')
                    s9=''.join(obj).encode('utf8')
                else:
                    s9=''.join(s9).encode('utf8')
                    
                
#                 print s1,"    ",s2,"    ",s3,"    ",s4,"    ",s5,"    ",s6,"    ",s7,"    ",s8,"    ",s9
#                 print i[0],'      ',i[1],'      ',i[2],'      ',i[3],'     ',i[4],'     ',i[5],'     ',i[6],'     ',i[7],'     ',i[8]
                n1="s1"+repr(index)
                n2="s2"+repr(index)
                n3="s3"+repr(index)
                n4="s4"+repr(index)
                n5="s5"+repr(index)
                n6="s6"+repr(index)
                n7="s7"+repr(index)
                n8="s8"+repr(index)
                n9="s9"+repr(index)
#                 print "你好"+"呀"
                print '"'+n1+'":"'+s1+'",'+'"'+n2+'":"'+s2+'",'+'"'+n3+'":"'+s3+'",'+'"'+n4+'":"'+s4+'",'+'"'+n5+'":"'+s5+'",'+'"'+n6+'":"'+s6+'",'+'"'+n7+'":"'+s7+'",'+'"'+n8+'":"'+s8+'",'+'"'+n9+'":"'+s9+'",',
                if i[1]=='公共选修课':
                    ku=0
                else:
                    if i[3]=='优秀':
                        spoint=4.5
                    else:
                        if i[3]=='良好':
                            spoint=3.5
                        else:
                            if i[3]=='中等':
                                spoint=2.5
                            else:
                                if i[3]=='及格':
                                    spoint=1.5
                                else:
                                    if i[3]=='不及格':
                                        spoint=0
                                    else:
                                        spoint=(float(i[3])-50)/10
    #                 print spoint
    #                 print float(i[7])
                    spoint_sum=spoint_sum+spoint*float(i[7])
                    if i[3]!='不及格':
                        credit_sum=credit_sum+float(i[7])
                index=index+1
            sums=index-1
            print '"sums":',sums,',',
            self.arvpoint=spoint_sum/credit_sum
            print '"arvpoint":',self.arvpoint,',',
#             print spoint_sum
#             print credit_sum
            
            stau="登陆成功"
            if not isinstance(stau,unicode):   #检查编码是否为unicode  
                obj = unicode(stau,'gbk')
                stau=''.join(obj).encode('utf8')
            else:
                stau=''.join(stau).encode('utf8')
            print '"statu":"',stau,'"}'
        else:
            stau="登陆失败"
            if not isinstance(stau,unicode):   #检查编码是否为unicode  
                obj = unicode(stau,'gbk')
                stau=''.join(obj).encode('utf8')
#                 print '"statu":',stau,'}'
            else:
                stau=''.join(stau).encode('utf8')
            print '"statu":"',stau,'"}'

#         print self.xueyuan
#         print self.zhuanye
#         print self.banji
#         print self.name
                 
# print ("请输入学号")             
# a=raw_input()
# print '请输入密码'
# b=raw_input()

# a='12015052085'
# b='1996.09.01'
# c=''
# d=''
# e='在校学习成绩查询'

a=form.getvalue('user_num')
b=form.getvalue('user_pw')
c=form.getvalue('year1')
d=form.getvalue('term1')
e=form.getvalue('type1')
if not isinstance(e,unicode):   #检查编码是否为unicode  
    obj = unicode(e,'utf-8')
    e=''.join(obj).encode('gbk')
else:
    e=''.join(e).encode('gbk')
s1=student(a,b,c,d,e)
s1.login()   