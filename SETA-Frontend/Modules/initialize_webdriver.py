from selenium.webdriver import Firefox, FirefoxOptions, Chrome, ChromeOptions, Ie, DesiredCapabilities
from Data.data_path import DOWNLOAD_DIR_PATH


# Enable FireFox to accept untrusted Certs and download CSVs as Default behaviour without clicking ok on the pop up
def ff_webdriver(url, log_name=None, jenkins=False):
    # # Create FF Options Object
    ff_options = FirefoxOptions()
    ff_options.set_preference('acceptInsecureCerts', True)
    ff_options.set_preference('browser.cache.disk.enable', False)
    ff_options.set_preference('browser.cache.memory_enable', False)
    ff_options.set_preference('browser.cache.offline.enable', False)
    ff_options.set_preference('browser.cache.check_doc_frequency', 2)
    ff_options.set_preference('network.http.use-cache', False)
    # ff_options.set_preference('browser.cache.memory.capacity', 10000000)
    # tells FF not to use default download dir
    ff_options.set_preference("browser.download.folderList", 2)
    # sets new download directory
    ff_options.set_preference('browser.download.dir', DOWNLOAD_DIR_PATH)
    # automatically save csv, excel, pcap files without asking for confirmation
    ff_options.set_preference('browser.helperApps.neverAsk.saveToDisk',
                              'text/csv,application/vnd.ms-excel,application/pcap,application/x-zip-compressed')
    # setting headless using set_preference('headless',True) doesn't work somehow
    if jenkins:
        ff_options.headless = True
    if log_name:
        log_name = 'firefox_{}.log'.format(log_name)
        ff_options.log.level = 'trace'
        driver = Firefox(options=ff_options, service_log_path=log_name)
        driver.get(url)
        return driver
    driver = Firefox(options=ff_options)
    driver.get(url)
    return driver


# Chrome WebDriver with accept untrusted cert.
def chrome_webdriver(url):
    options = ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = Chrome(chrome_options=options)
    driver.get(url)
    return driver


# Internet Explorer with option to accpet untrusted certs
def ie_webdriver(url):
    capabilities = DesiredCapabilities().INTERNETEXPLORER
    capabilities['acceptSslCerts'] = True
    driver = Ie(capabilities=capabilities)
    assert driver.lower() != 'Not a supported browser'
    driver.get(url)
