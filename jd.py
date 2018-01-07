def jd(driver, time, re, urllib, path, ActionChains, Keys):
    driver.maximize_window()
    time.sleep(1)
    driver.find_element_by_xpath(".//*/div[@id='comment-count']/a").click() # 累计评论
    time.sleep(2)
    try:
        driver.find_element_by_xpath(".//*/ul[@class='filter-list']/li[2]/a").click() # 晒图
        flag = True
    except:
        driver.find_element_by_xpath (".//*/li[@clstag='shangpin|keycount|product|shaidantab']/a").click () # 晒图，京东有两种UI，一种类似于商城，一种类似于小店
        flag = False
    time.sleep(6)

    while True:

        # 分别存储每个买家秀的property和对应的用户发表的评论时间及内容
        img_ele = driver.find_element_by_xpath(".//*/img[@class='J-photo-img']")
        p, d, c = '', '', ''
        try:
            p = driver.find_element_by_xpath(".//*/div[@class='p-features']/ul").text.replace ('/', '-').replace ('\\', '--').replace('\n', '-') # p = '【超10万好评 5升经典爆款】'
            d = driver.find_element_by_xpath(".//*/div[@class='comment-time type-item']").text # d = '2018.01.05'
            c = driver.find_element_by_xpath(".//*/div[@class='p-comment']").text.replace ('/', '-').replace ('\\', '--')
        except Exception as e:
            print("ERROR happens when getting corresponding property of img :::", e)

        url = img_ele.get_attribute('src')
        with open (path + '/' + p + '-' + d + '-' + str(time.time())+ '.jpg', 'wb+') as f_img:
            try:
                f_img.write (urllib.request.urlopen (url).read ())
            except:
                print("Img url illegal: " + url)
            else:
                print ("A new img!!! PROPERTY = %s, DATETIME = %s\n, COMMENT = %s\n, DOWALOADING url = %s"
                        %(p, d, c, url))

        # ---------------翻页---------------
        try:
            current_img = driver.find_element_by_xpath(".//*/li[@class='selected']")
            next_img = current_img.find_element_by_xpath("./following-sibling::li[1]/a")
            ActionChains(driver).move_to_element(next_img).click(next_img).perform()
            time.sleep (1)
        except:
            print("last img collected")
            exit()


