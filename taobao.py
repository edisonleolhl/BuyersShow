def taobao(driver, time, re, urllib, path, ActionChains, Keys):
    driver.maximize_window()
    time.sleep(2)
    driver.find_element_by_xpath(".//*/a[@id='J_ReviewTabTrigger']").click() # 累计评论
    time.sleep(1)
    driver.find_element_by_xpath(".//*/label/input[@id='reviews-t-val3']").send_keys(Keys.SPACE) # 有图
    time.sleep(3)

    while True:

        # 得到把该页的所有买家秀，存入列表中，并且创建另外三个列表，长度一样，
        # 分别存储每个买家秀的property和对应的用户发表的评论时间及内容
        # 我认为带买家秀的评论比较重要，最后在图片文件名中给出
        img_ele_list = driver.find_elements_by_xpath(".//*/li[@class='photo-item']/img")
        property_list = []
        datetime_list = []
        comment_list = []

        for img_ele in img_ele_list:
            p, d, c = '', '', ''
            try:
                p = img_ele.find_element_by_xpath("./../../../following-sibling::div[1]/div[@class='tb-r-info']") # p = '2017年11月27日 10:06颜色分类：红色  参考身高：130cm'
                d = re.findall (r'^20[0-9][0-9].[0-1][0-9].[0-3][0-9].', p.text)
                if len(d) > 0:
                    d = d[0]  # 得到日期时间
                else:
                    d = ''
                p = re.findall (r'(?<=[0-9][0-9]:[0-9][0-9]).+$', p.text)
                if len(p) > 0:
                    p = p[0].replace('/', '-').replace('\\', '--').replace('<', '[').replace('>', ']').replace(':','：').replace(
    '?','？').replace('"','``').replace('|', '$').replace ('\n', '-')  # 删掉日期时间，得到款式等信息
                else:
                    p = ''
                c = img_ele.find_element_by_xpath(".//../../../preceding-sibling::div[1]").text.replace('/', '-').replace('\\', '--').replace('<', '[').replace('>', ']').replace(':','：').replace(
    '?','？').replace('"','``').replace('|', '$').replace ('\n', '-')
            except Exception as e:
                print("ERROR happens when getting corresponding property of img :::", e)
            datetime_list.append (d)
            property_list.append (p)
            comment_list.append (c)

        # 四个列表长度一致，所以可以用同一个指针i来对四个列表同步遍历
        for i in range(len(img_ele_list)):
            url = img_ele_list[i].get_attribute('src').replace('40x40', '400x400')
            with open (path + '/' + property_list[i] + '-' + datetime_list[i] + '-' + str(time.time()) + '.jpg', 'wb+') as f_img:
                try:
                    f_img.write (urllib.request.urlopen (url).read ())
                except:
                    print("Img url illegal: " + url)
                else:
                    print ("A new img!!! PROPERTY = %s, DATETIME = %s\n, COMMENT = %s\n, DOWALOADING url = %s"
                           %(property_list[i], datetime_list[i], comment_list[i], url))

        # ---------------翻页---------------
        driver.execute_script ("window.scrollBy(0,-100)")
        time.sleep(1)
        try:
            next = driver.find_element_by_xpath(".//*/ul/li[@class='pg-current']/./following-sibling::li[1]") # 淘宝的评论页码工具条，每个都是li标签
            if next.text.isdigit():
                ActionChains(driver).click(next).perform()
                time.sleep(1)
            else:
                exit()
        except:
            print('only one page with img')
            exit()