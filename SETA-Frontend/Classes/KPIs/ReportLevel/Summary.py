from selenium.webdriver.common.by import By
from ..KPIsReportLevel import KPIsReportLevel


class Summary(KPIsReportLevel):
    def open(self):
        super()._open()
        summary = self.driver.find_element(By.CSS_SELECTOR, 'ul > li[title="Report Summary"] > a')
        summary.click()
