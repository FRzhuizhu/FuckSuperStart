# -*- coding:utf-8 -*-

from selenium import webdriver
import time
from code_deal import *
from PIL import Image
from ShowProcess import ShowProcess
from selenium.webdriver import ActionChains




TEST_CODE = True
TEST_HEADLESS = True
TEST_BUG = False
MAX_RETRY_TIMES = 10

Exclude_lesson = ['大学物理（Ⅰ）','马克思主义基本原理概论']



class FuckSuperStart(object):

    def __init__(self, uname, password):

        self.uname = uname
        self.password = password
        # self.lesson = lesson_name

        chromeoption = webdriver.ChromeOptions()
        if TEST_HEADLESS:
            chromeoption.add_argument('-headless')
            chromeoption.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(chrome_options=chromeoption)

    def __getcode_frompic(self):
        self.browser.save_screenshot('All.png')  # 截取当前网页，该网页有我们需要的验证码
        codepic = self.browser.find_element_by_id('numVerCode')
        location = codepic.location  # 获取验证码x,y轴坐标
        size = codepic.size  # 获取验证码的长宽
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
        i = Image.open("All.png")  # 打开截图
        result = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        result.save('code.png')
        if TEST_CODE:
            res = from_flie_to_num('code.png')
        else:
            result.show()
            res = input()
        return res

    def _auto_login(self):

        # 登陆网址，登陆后自动跳转到个人空间
        login_url = 'http://passport2.chaoxing.com/login?fid=2224&refer=http://i.mooc.chaoxing.com/space/index.shtml'

        self.browser.get(login_url)
        time.sleep(2)
        # 投递学号
        self.browser.find_element_by_id('unameId').send_keys(self.uname)

        # 投递密码
        self.browser.find_element_by_id('passwordId').send_keys(self.password)


        # 截图 裁剪 得到验证码，调用打码平台api 返回验证码
        codenum = self.__getcode_frompic()
        # print (codenum)

        # 投递验证码
        self.browser.find_element_by_id('numcode').send_keys(codenum)

        # 点击登录
        self.browser.find_element_by_class_name('zl_btn_right').click()

    def _get_lesson_list(self):

        # 点击 课程 标签
        self.browser.find_element_by_id('zne_kc_icon').click()
        time.sleep(5)
        # 选择 右边框架
        self.browser.switch_to_frame(self.browser.find_element_by_id('frame_content'))

        # 获取所有课程url
        lessons = self.browser.find_elements_by_css_selector('.clearfix > a')
        # 打印所有课程
        lessons_info = []
        for lesson in lessons:
            if lesson.text not in Exclude_lesson:
                print(lesson.text)
                lessons_info.append((lesson.text,lesson.get_attribute('href')))

        return lessons_info






    def _find_lesson(self):
        pass


    def _seevideo(self,articlename):
        articlename.find_element_by_tag_name('a').click()
        time.sleep(3)
        if TEST_BUG:
            pass
            # self.browser.save_screenshot('{}.png'.format(articlename.text))
        tabtags = self.browser.find_element_by_class_name("tabtags")
        moviespan = tabtags.find_elements_by_css_selector("[title=视频]")
        if (len(moviespan) > 0):
            moviespan[0].click()
        time.sleep(3)

        # iframe = browser.find_element_by_tag_name("iframe")
        # iframe.click()
        time.sleep(3)
        iframe = self.browser.find_element_by_tag_name("iframe")
        self.browser.switch_to.frame(iframe)
        iframe = self.browser.find_element_by_tag_name("iframe")
        self.browser.switch_to.frame(iframe)
        # browser.execute_script(JavaScript)
        video = self.browser.find_element_by_id("video_html5_api")
        playspan = self.browser.find_element_by_class_name("vjs-big-play-button")
        playspan.click()
        # video.click()

        actions = ActionChains(self.browser)
        actions.move_to_element_with_offset(video, 50, 30).click()
        actions.click()

        actions.perform()
        time.sleep(1)
        alltime = self.browser.find_element_by_class_name("vjs-duration-display").text
        while (alltime == "0:00"):
            print("(▼ヘ▼#)【呀！总时长溜走了！】")
            actions = ActionChains(self.browser)
            actions.move_to_element_with_offset(video, 50, 30)
            actions.move_to_element_with_offset(video, 30, 30)
            actions.perform()
            alltime = self.browser.find_element_by_class_name("vjs-duration-display").text
        print("总时长 " + '[' + alltime + ']')

        max_steps = int(alltime[:alltime.find(':')]) * 60 + int(alltime[alltime.find(':') + 1:])
        process_bar = ShowProcess(max_steps)

        nowtime = self.browser.find_element_by_class_name("vjs-current-time-display").text
        # stay_times = 0
        while alltime != nowtime:
            # if stay_times > 30:
            #     filename = time.ctime()+'.html'
            #     with open(filename,'w',encoding = 'utf-8') as f:
            #         f.write(self.browser.page_source)
            #     print ('停留时间过长，刷新页面并已保存网页源码',filename)
            #     self.browser.refresh()
            #     break
            question = self.browser.find_elements_by_class_name("ans-videoquiz-title")
            if question:
                print(question[0].text)
                true_inputls = self.browser.find_elements_by_css_selector('[value="true"]')
                try:
                    for true_input in true_inputls:
                        # print(true_input[0].text)
                        true_input.click()
                    submit_input = self.browser.find_element_by_id('ext-gen1045')
                    submit_input.click()
                except:
                    print('答题失败！刷新页面并保存网页源码')
                    filename = time.ctime()+'.html'
                    with open(filename,'w',encoding = 'utf-8') as f:
                        f.write(self.browser.page_source)
                    self.browser.refresh()
                    break

            time.sleep(3)
            newnowtime = self.browser.find_element_by_class_name("vjs-current-time-display").text
            if (nowtime == newnowtime and newnowtime != '' and newnowtime != alltime):
                stay_times += 1
                actions = ActionChains(self.browser)
                actions.move_to_element_with_offset(video, 50, 30).click()
                actions.perform()
            else:
                stay_times = 0
            nowtime = newnowtime
            # print(i)
            # print(nowtime)
            if (nowtime == ''):
                actions = ActionChains(self.browser)
                actions.move_to_element_with_offset(video, 50, 30)
                actions.move_to_element_with_offset(video, 20, 30)
                actions.perform()
            else:
                i = int(nowtime[:nowtime.find(':')]) * 60 + int(nowtime[nowtime.find(':') + 1:]) - 1
                process_bar.show_process(i=i, formtitle='[' + nowtime + ']')
        else:
            process_bar.show_process(i=i + 1, formtitle='[' + nowtime + ']')
        self.browser.switch_to.default_content()
        self.browser.find_element_by_class_name("goback").find_element_by_tag_name("a").click()
        time.sleep(3)


    def _study_lesson(self,catalog_web_url):

        while (1):
            # flag = False
            print('<(▰˘◡˘▰)>正在查找未完成课程')
            # timelline = self.browser.find_element_by_class_name("timeline")
            # units = timelline.find_elements_by_class_name("units")
            h3ls = self.browser.find_elements_by_css_selector('h3[class="clearfix"]')

            h3_not_i = []
            for h3 in h3ls:
                i = h3.find_elements_by_tag_name('i')
                if not i:
                    h3_not_i.append(h3)
            # for unit in units:
            #     # print(unit.text)
            #     leveltwos = unit.find_elements_by_class_name("leveltwo")
            #     for leveltwo in leveltwos:
            #         em = leveltwo.find_element_by_tag_name("em")
            # catalog_web_url = self.browser.current_url
            for h3 in h3_not_i:
                em = h3.find_element_by_tag_name('em')
                if (em.text != "" and int(em.text) > 1):
                    articlename = h3.find_element_by_class_name("articlename")
                    print('ヾ(๑╹◡╹)ﾉ"开始学习 ' + '[' + articlename.text + ']')
                    if TEST_BUG:
                        self._seevideo(articlename)
                    else:
                        try:
                            self._seevideo(articlename)
                        except:
                            print('学习出错了，刷新目录页面')
                            print(self.browser.window_handles)
                            self.browser.get(catalog_web_url)
                            time.sleep(5)
                    break
            else:
                break
            continue
            #             flag = True
            #             break
            #     if (flag):
            #         break
            # if (flag == False):
            #     break

        print('（づ￣3￣）づ╭❤～已经完成所有课程啦~~~')


    def run(self):

        self._auto_login()
        lessons_info = self._get_lesson_list()

        for lesson in lessons_info:
            if not lesson[0] or not lesson[1]:
                continue
            print ('当前学习的是'+lesson[0])

            self.browser.get(lesson[1])
            time.sleep(5)
            #
            # ###################
            if TEST_BUG:
                self._study_lesson(lesson[1])
            # ###################
            #
            else:
                try:
                    self._study_lesson(lesson[1])
                except KeyboardInterrupt:
                    print ('已释放Chrome进程')
                    self.browser.quit()
                    exit()
                except:
                    lessons_info.append(lesson)
                    print ('(╥╯^╰╥) 出错了，待会再学')



        self.browser.quit()


if __name__ == '__main__':
    stid = input('学号：')
    pswd = input('密码：')
    if TEST_BUG:
        app = FuckSuperStart(stid,pswd)
        app.run()
    else:
        for _ in range(MAX_RETRY_TIMES):
            try:
                app = FuckSuperStart(stid,pswd)
                app.run()
                break
            except KeyboardInterrupt:
                app.browser.quit()
                print('已释放Chrome进程')
                break
            except:
                try:
                    app.browser.quit()
                except:
                    print ('webdriver创建失败')
                    break
                else:
                    print ('未知异常，已释放Chrome进程')
