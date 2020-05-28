pytest_plugins = 'pytester'
import logging
import pytest
from selenium import webdriver
from pytest_wframework.api import API

@pytest.fixture(autouse=True, scope="function")
def api(request):
    # driverspath=request.config.option.driverspath
    ChromePath = r"C:\Users\X\Desktop\MyPFE\VCS\ST-MCU-Finder\DriversAndApps\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=ChromePath)
    FunctionLevelApi=API(driver)
    logging.StreamHandler(FunctionLevelApi.getLogStream())
    return FunctionLevelApi
