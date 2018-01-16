def jd_hk(driver, time, re, urllib, path, ActionChains, Keys):
    driver.maximize_window()
    time.sleep(1)
    driver.find_element_by_xpath(".//*[@clstag='shangpin|keycount|product|pingjia_oversea']").click() # 累计评论
    time.sleep(2)
    driver.find_element_by_xpath(".//*[@clstag='shangpin|keycount|product|shandan_oversea']/a").click() # 晒图
    time.sleep(6)

    while True:

        # 分别存储每个买家秀的property和对应的用户发表的评论时间及内容
        img_ele_list = driver.find_elements_by_xpath(".//*/div[@id='comments-list']/div[@id='comment-4']/div[@class='com-table-main']/div[@class='comments-item']/table[@class='com-item-main clearfix']/tbody/tr/td[@class='com-i-column column2']/div[@class='p-comment-wrap']/div[@class='J-thumb-wrap p-photos-thumbnails']/div[@class='thumb-list J-thumb-list']/ul/li[@class='J-thumb-item']/a/img[@class='J-thumb-img']")
        property_list = []
        datetime_list = []
        comment_list = []
        for img_ele in img_ele_list:
            p, d, c = '', '', ''
            try:
                p = img_ele.find_element_by_xpath (
                    "./../../../../../../../preceding-sibling::td[1]/div[@class='type-item']").text.replace (
                    '/', '-').replace ('\\', '--').replace ('\n', '-')  # p = '颜色：MMZ 600ML 黑色'
                d = img_ele.find_element_by_xpath (
                    "./../../../../../../../preceding-sibling::td[1]/p[@class='time']").text.replace (
                    '/','-').replace ('\\', '--')
                c = img_ele.find_element_by_xpath (
                    "./../../../../../preceding-sibling::div[1]/span[@class='desc']").text
            except Exception as e:
                print ("ERROR happens when getting corresponding property of img :::", e)
            datetime_list.append (d)
            property_list.append (p)
            comment_list.append (c)

        # 四个列表长度一致，所以可以用同一个指针i来对四个列表同步遍历
        for i in range (len (img_ele_list)):
            url = img_ele_list[i].get_attribute ('src').replace ('46x46', '460x460')
            with open (path + '/' + property_list[i] + '-' + datetime_list[i] + '-' + str (time.time ()) + '.jpg',
                       'wb+') as f_img:
                try:
                    f_img.write (urllib.request.urlopen (url).read ())
                except:
                    print ("Img url illegal: " + url)
                else:
                    print ("A new img!!! PROPERTY = %s, DATETIME = %s\n, COMMENT = %s\n, DOWALOADING url = %s"
                           % (property_list[i], datetime_list[i], comment_list[i], url))

        # ---------------翻页---------------
        try:
            current_page = driver.find_element_by_xpath(".//*/div[@class='ui-page']/a[@class='ui-page-curr']")
            print("current_page = ", current_page.text)
            next_page = current_page.find_element_by_xpath("./following-sibling::a")
            ActionChains(driver).move_to_element(next_page).click(next_page).perform()
            time.sleep (1)
        except:
            print("last img collected")
            exit()


