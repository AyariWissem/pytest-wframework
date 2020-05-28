import io
import logging
import traceback
import allure
from allure_commons import plugin_manager
from allure_pytest.listener import AllureListener
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def styleHTML(msg, status, html):  # TODO better implementation for html using the custom message and headers
    """" FAIL, WARING, PASS, DONE use colors, html and excel """
    status = status.lower().strip()

    logColors = {'debug': '1da1f2',
                 'info': '0F9D58',
                 'warning': 'f48042',
                 'error': 'fd5a3e',
                 'critical': 'fd5a3e',
                 'pass': '97cc64', 'passed': '97cc64',
                 'fail': 'fd5a3e', 'failed': 'fd5a3e',
                 'done': 'aaa',
                 'generic': '000000'
                 }
    levels = ['debug', 'info', 'warning', 'error', 'critical']
    if status in levels:
        msg = msg.replace(status.upper(),
                          f"<span style='color: #{logColors[status]};font-weight:bold;'>{status.upper()}</span>")
        msg = f"<p>{msg}</p>"
        # for level in levels:
        #     msg = msg.replace(level.upper(),
        #                       f"<span style='color: #{logColors[level]};font-weight:bold;'>{level.upper()}</span>")
    else:
        msg = msg[msg.find("MESSAGE: ") + len("MESSAGE: "):]  # no longer needed but will leave it here
        msg = f"<p style='color:#{logColors[status]};font-weight:bold;font-size: 150%;'>{msg}</p>"
        # msg += "<br>"
    html += msg
    allure.dynamic.description_html(html)
    return html


def getAllureDescription():  # very fragile, UNUSED for now
    plugin = next(p for p in plugin_manager.get_plugins() if isinstance(p, AllureListener))
    testDescription = plugin.allure_logger.get_test(None).description
    return testDescription


# for the custom log level message
def message(self, msg, *args, **kwargs):
    if self.isEnabledFor(60):
        self._log(60, msg, args, **kwargs)


class API:
    def __version__(self):
        self.__version__ = "1.0.1"

    def __init__(self, driver, logLevel=logging.DEBUG):
        self.driver = driver
        # due to the app nature we won't be using it for now
        self.wait = WebDriverWait(self.driver, timeout=10,
                                  poll_frequency=0.5,
                                  # ignored_exceptions=[NoSuchElementException,  # activated by default
                                  #                     ElementNotVisibleException,
                                  #                     ElementNotSelectableException]
                                  )
        # Private logger
        logging.Logger.message = message
        logging.addLevelName(60, 'MESSAGE')
        ###
        self.logLevel = logLevel
        self.logger = logging.getLogger()
        self.logger.setLevel(self.logLevel)
        #  - %(name)s
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s',
                                      datefmt='%m/%d/%Y %H:%M:%S %p')
        self.LogStream = io.StringIO()
        self.streamHandler = logging.StreamHandler(self.LogStream)
        self.streamHandler.setFormatter(formatter)
        self.logger.addHandler(self.streamHandler)
        self.html = ""

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (session="{1}")>'.format(
            type(self), self.driver.session_id)

    # Logger methods
    def getLogger(self):
        return self.logger

    def getLog(self):
        return self.LogStream.getvalue()

    def getLogStream(self):
        return self.LogStream

    def info(self, msg):
        self.logger.info(msg)
        msg = self.getLog().splitlines()[-1]  # getting the last log message
        self.html = styleHTML(msg, "info", self.html)

    def debug(self, msg):
        self.logger.debug(msg)
        msg = self.getLog().splitlines()[-1]  # getting the last log message
        self.html = styleHTML(msg, "debug", self.html)

    def warning(self, msg):
        self.logger.warning(msg)
        msg = self.getLog().splitlines()[-1]  # getting the last log messagessage
        self.html = styleHTML(msg, "warning", self.html)

    def error(self, msg):
        self.logger.error(msg)
        msg = self.getLog().splitlines()[-1]  # getting the last log message
        self.html = styleHTML(msg, "error", self.html)

    def critical(self, msg):
        self.logger.critical(msg)
        msg = self.getLog().splitlines()[-1]  # getting the last log message
        self.html = styleHTML(msg, "critical", self.html)
        assert False

    def message(self, msg, status):
        self.logger.message(msg)
        msg = self.getLog().splitlines()[-1]
        self.html = styleHTML(msg, status, self.html)

    def writeMsginReport(self, msg, status):
        status = status.lower()
        if status in ['pass', 'passed', 'fail', 'failed', 'done']:
            self.message(msg, status)
            if status == "fail" or status == "failed": assert False
            if status == "pass" or status == "passed" or "done": assert True
            if status == "done": assert True
        else:
            self.error("Invalid status: " + status)

        # FAIL, WARING, PASS, DONE use colors, html and excel
        # oldDescription = getAllureDescription()
        # if oldDescription:
        #     oldDescription = oldDescription.strip()
        #     oldDescription += styleHTML(msg, status)
        #     allure.dynamic.description_html(oldDescription)
        # else:
        #     allure.dynamic.description_html(styleHTML(msg, status))

    # internal Logging methods
    def formatLocator(self, locatorType, location):
        return f"| locatorType: {locatorType} Value: {location}"

    def logError(self, msg, locatorType, location):
        self.error(msg + self.formatLocator(locatorType, location))
        self.error(f"Exception Caught: {traceback.format_exc()}")

    def logCritical(self,msg, locatorType, location):
        self.critical(msg + self.formatLocator(locatorType, location))
        self.critical(f"Exception Caught: {traceback.format_exc()}")

    # Driver methods
    def getElement(self, locatorType, locator):
        locator = locator.strip()
        locatorType = locatorType.strip()
        element = None
        try:
            if locator and locatorType:
                element = self.wait.until(EC.presence_of_element_located((locatorType, locator)))
                self.info("Element found " + self.formatLocator(locatorType, locator))
                return element
            else:
                self.logCritical("Locator or locatorType is an empty string" , locatorType, locator)
        except:
            self.logCritical(f"Element not found ", locatorType, locator)

    def sendKeys(self, locatorType, locator, data, element=None):
        data = data.strip()
        try:
            element = self.getElement(locatorType, locator)
            element.send_keys(data)
            self.info(f"Sent data on element with locator: {locator} locatorType: {locatorType}")
        except:
            self.logCritical("Cannot send data to the element ", locatorType, locator)

    def clickLink(self, locatorType, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable((locatorType, locator)))
            element.click()
        except:
            self.logCritical("Cannot click on the Link ", locatorType, locator)

    def activateChoice(self, locatorType, locator):
        element = self.getElement(locatorType, locator)
        state = element.is_selected()
        try:
            if state:
                self.warning("Element is already selected")
                pass
            else:
                self.wait.until(EC.element_to_be_selected(element))
        except:
            self.logCritical(f"Cannot select the element ", locatorType, locator)

    def deactivateChoice(self, locatorType, locator):
        element = self.getElement(locatorType, locator)
        state = element.is_selected()
        try:
            if not state:
                self.warning("Element is already deselected")
                pass
            else:
                self.wait.until_not(EC.element_to_be_selected(element))
        except:
            self.logCritical(f"Cannot deselect the element ", locatorType, locator)

    def search_product(self, locatorType, locator, data):
        self.sendKeys(locatorType, locator, data)

    def get(self, URL):
        return self.driver.get(URL)

    def quit(self):
        return self.driver.quit()