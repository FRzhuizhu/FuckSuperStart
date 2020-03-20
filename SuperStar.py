# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import re


def chrome_init(user: str = '201702060122', psw:str = '45278835'):
    chrome = webdriver.Chrome()
    chrome.implicitly_wait(3)
    chrome.get('http://i.mooc.chaoxing.com/space/index?t=1544375321684')
    # 设置学校
    chrome.execute_script('document.getElementById("fid").setAttribute("value",2224)')
    chrome.execute_script('document.getElementById("fidName").setAttribute("value","成都理工大学")')
    # 用户密码
    chrome.find_element_by_id('unameId').send_keys(user)
    chrome.find_element_by_id('passwordId').send_keys(psw)
    # numcode = chrome.find_element_by_id('numVerCode')
    
    while True:
        # 验证码
        chrome.find_element_by_id('numcode').send_keys(input('请输入验证码>>>'))
        # 登陆
        chrome.find_element_by_class_name('zl_btn_right').click()
        try:
            # 检查验证码
            show_error = chrome.find_element_by_id('show_error')
        except NoSuchElementException:
            break
        
        chrome.find_element_by_id('passwordId').send_keys(psw)
        
    print('登陆成功')
    # sleep(5)
    # chrome.find_element_by_class_name('zne_kc_icon').click()
    # 直接跳转毛特中界面
    chrome.get('https://mooc1-1.chaoxing.com/mycourse/studentcourse?courseId=207379262&clazzid=15022250&vc=1&cpi=46413139&enc=1cf12d07d266a83af47d2d2479b3da87')
    
    return chrome




def test_init(user: str = '201702060122', psw:str = '45278835'):
    from selenium import webdriver
    from time import sleep
    chrome = webdriver.Chrome()
    chrome.get('http://i.mooc.chaoxing.com/space/index?t=1544375321684')
    # 设置学校
    chrome.execute_script('document.getElementById("fid").setAttribute("value",2224)')
    chrome.execute_script('document.getElementById("fidName").setAttribute("value","成都理工大学")')
    # 用户密码
    chrome.find_element_by_id('unameId').send_keys(user)
    chrome.find_element_by_id('passwordId').send_keys(psw)
    return chrome

def get_numofvideo(chrome):
    chrome.switch_to.default_content()
    try:
        chrome.switch_to.frame('iframe')
        numofvideo = len(chrome.find_elements_by_tag_name('iframe'))
        print(f'找到{numofvideo}个视频')
        return numofvideo
    except:
        print('找不到第一层框架')
        return 0


def get_play_progress(video):
    # ppg = video.find_elements_by_class_name('vjs-play-progress')
    ppg = video.find_elements_by_class_name('vjs-progress-holder')
    if ppg:
        # play_progress_in_style = ppg[0].get_attribute('style')      # width: 95.84%;
        # res = re.match(pattern='width:\s?(\d+\.?\d+)%;',string=play_progress_in_style)
        # if res:
            # play_progress = eval(res.group(1))
            # return play_progress
        percent = eval(ppg[0].get_attribute("aria-valuenow"))
        time_text = ppg[0].get_attribute("aria-valuetext")
        return percent, time_text
    return None
    


def get_video(chrome, idofvideo):
# chrome.switch_to.frame('iframe')
# chrome.switch_to.frame(0)
    chrome.switch_to.default_content()
    try:
        chrome.switch_to.frame('iframe')
        chrome.switch_to.frame(idofvideo)
        video = chrome.find_element_by_id('video')
    except:
        return None
    # print(f'获取到第{idofvideo+1}个视频')
    return video



def get_qestion_text(video):
    if qestion := video.find_elements_by_class_name('x-component'):
        if qt := qestion[0].text :
            qet_and_ans = qt.split('\n')
            true_ans = []
            if true_labels := qestion[0].find_elements_by_tag_name('label'):
                for index, true_lb in enumerate(true_labels):
                    if true_input := true_lb.find_elements_by_css_selector('input[value="true"]'):
                        true_ans.append(true_lb.text)
                        qet_and_ans[1+index] += '(对√)'
            qet_and_ans_text = "\n".join(qet_and_ans)
            print('=' * 30)
            print(f'获取到题目:\n{qet_and_ans_text}')
            print('=' * 30)
            with open(f'{qet_and_ans[0]}.txt','w',encoding = 'utf-8') as f:
                f.write(qet_and_ans_text)
                print('保存题目文件成功')
            return qet_and_ans, true_ans
    else:
        print('题目文本获取失败')
        return [],''
        



def submit_answer(video):
    # while chrome.find_elements_by_tag_name('iframe'):
        # chrome.switch_to.frame(0)
    if qestion := video.find_elements_by_css_selector('input[value="true"]'):
        taq, ta = get_qestion_text(video)
        for index, inp in enumerate(qestion):
            print(f'已选择{ta[index]}')
            inp.click()
    # try:
        if submit_button := video.find_elements_by_class_name('ans-videoquiz-submit'):
            submit_button[0].click()
        print('已提交问题')
    # except NoSuchElementException:
        # pass

def auto_play(video):
    try:
        temp = video.find_elements_by_class_name('vjs-control-text')
    except StaleElementReferenceException:
        print('已切换网页')
        return
        
    if not temp:
        print('找不到播放按钮')
        return
    # 加载页面第一次播放
    if temp[1].text == '播放视频':
        print('新视频第一次播放')
        video.click()
    play_button = temp[2]
    if play_button.text == '播放':
        try:
            video.click()
        except:
            print('播放不可点击，可能有题目')
            return
        print('激活播放')


def get_title_and_src(chrome, video_num):
    chrome.switch_to.default_content()
    if h1 := chrome.find_elements_by_tag_name('h1'):
        print(f'{h1[0].text}')
    chrome.switch_to.frame(0)
    spans = chrome.find_elements_by_class_name('ans-job-icon')
    for span in spans:
        print(span.text)
    for index in range(video_num):
        chrome.switch_to.frame(index)
        if vapi := chrome.find_elements_by_id('video_html5_api'):
            print(f'{vapi[0].get_attribute("src")}')
            chrome.switch_to.parent_frame()
    


def run(chrome):
    video_num = get_numofvideo(chrome)
    get_title_and_src(chrome, video_num)
    for num in range(video_num):
        print(f'开始播放：第{num + 1}个视频')
        while True:
            video = None
            if video := get_video(chrome,num):
                submit_answer(video)
                ppg, time_text = get_play_progress(video)
                print(f'{num=}',f'{ppg=}%',f'{time_text=}')
                if ppg == 100:
                    break
                auto_play(video)
            else:
                print('找不到播放器')
                break
            sleep(3)
        print(f'播放结束：第{num + 1}个视频')