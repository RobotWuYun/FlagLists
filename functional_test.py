import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    #setUp 和 tearDown 是特殊的方法，分别在各个测试方法之前和之后运行
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()
    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn(row_text, [row.text for row in rows])
    def test_can_start_a_list_and_retrieve_it_later(self):
        ## 打开一个位置的地址
        self.browser.get("http://localhost:8000")
        ## 发现页面的标题包含To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)
        ## 输入一个代办事项
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        ### 在文本框中输入代办
        inputData_1 = 'Find job'
        inputBox.send_keys(inputData_1)
        ### 回车保存输入，并刷新页面，且表格中出现了刚才填写的代办
        inputBox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table(inputData_1)
        ### 页面又出现了一个输入框，并且可以再次输入
        inputBox = self.browser.find_element(By.ID, 'id_new_item')
        ### 再次写入并保存
        inputData_2 = "Buy car"
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys(inputData_2)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table(inputData_1)
        self.check_for_row_in_list_table(inputData_2)

        
        ## 看看能否长久保存
        ### 保存url
        ### 关闭当前浏览器并保存url
        ### 再次访问url，检查代办事项是否还在
if __name__ == '__main__': # Python 脚本使用这个语句检查自己是否在命令行中运行，而不是在其他脚本中导入
    unittest.main(warnings='ignore') # warnings='ignore' 的作用是禁止抛出ResourceWarning 异常