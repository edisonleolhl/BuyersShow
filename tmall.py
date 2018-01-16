def tmall(driver, time, re, urllib, path, ActionChains, Keys):
    driver.maximize_window()
    time.sleep(3)
    driver.find_element_by_xpath(".//*/em[@class='J_ReviewsCount']").click()
    # driver.find_element_by_xpath(".//*/li[@id='J_ItemRates']/div[@class='tm-indcon']").click()  #有时候这个按钮无法点击，所以注释掉这个
    time.sleep(1)
    driver.find_element_by_xpath(".//*/span[@class='rate-filter']/input[@class='rate-list-picture rate-radio-group']").send_keys(Keys.SPACE)
    time.sleep(3)

    while True:

        # 得到把该页的所有买家秀，存入列表中，并且创建另外三个列表，长度一样，
        # 分别存储每个买家秀的property和对应的用户发表的评论时间及内容
        # 我认为带买家秀的评论比较重要，最后在图片文件名中给出
        img_ele_list = driver.find_elements_by_xpath(".//*/ul[@class='tm-m-photos-thumb']/li/img")
        property_list = []
        datetime_list = []
        comment_list = []
        for img_ele in img_ele_list:
            p, d, c = '', '', ''
            try:
                p = img_ele.find_element_by_xpath("./../../../../../following-sibling::td[@class='col-meta']/div[@class='rate-sku']").text.replace ('/', '-').replace ('\\', '--').replace('\n', '-') # p = '颜色分类：01黑色尺码：42[偏大一码]'
                d = img_ele.find_element_by_xpath("./../../../../following-sibling::div[1]").text.replace ('/', '-').replace ('\\', '--')
                c = img_ele.find_element_by_xpath("./../../../preceding-sibling::div[1]").text
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
        # driver.execute_script ("window.scrollBy(0,-100)")
        time.sleep(1)
        try:
            last_ahref = driver.find_element_by_xpath(".//*/div[@class='rate-paginator']/a[last()]")
            # 当到达最后一页时，“下一页”标签由a标签变为span标签，所以判断最后一个a标签如果是数字的话，那么则到达最后一页，即退出
            if last_ahref.text.isdigit():
                exit()
            else:
                ActionChains(driver).click(last_ahref).perform()
                time.sleep(1)
        except:
            print("only one page with img")
            exit()

