# -*- coding: utf-8 -*-
"""
Lib to reuse chrome windows
"""

#from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException

class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        rewrite start_session
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = True
        self.command_executor.w3c = self.w3c
        
def ReUse():
    with open("F:\GitHub\lib_ChromeReuse\SessionInfo.txt", 'r') as f:  #specify the right location of SessionInfo.txt
        executor_url=f.readline().strip('\n')
        print executor_url
        session_id=f.readline().strip('\n')
        print session_id
        f.close()

    driver = ReuseChrome(command_executor=executor_url, session_id=session_id)

    return driver
