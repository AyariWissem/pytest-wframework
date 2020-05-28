# -*- coding: utf-8 -*-

import pytest
import os.path
from pytest_jsonreport.plugin import JSONReport
from .excelbuilder import excelBuilder

def pytest_configure(config):
   plugin = JSONReport()
   config.pluginmanager.register(plugin)

def pytest_addoption(parser):
    path = os.path.realpath(__file__)
    group = parser.getgroup('wframework')
    group.addoption(
        '--wexcel',
        action='store',
        dest='excelpath',
        default=path,
        help='generate excel file in a given path'
    )


def pytest_sessionfinish(session, exitstatus):
    #TODO check if the path provided is valid
    # path= session.config.getoption("excel")
    # print("the path is : ", path)
    report = session.config._json_report.report
    path = session.config.getvalue("excelpath")
    if path:
        excelBuilder(report, path).generateExcelt()