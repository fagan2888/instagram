from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException      
# paths & urls
from infos import ig_log_page, username_box, password_box, save_info_popup, new_post_button, user_agent

# tag the options field
options = webdriver.FirefoxOptions()  
# disable push/popups 
options.set_preference("dom.push.enabled", False)  

# tag the profile option
profile = webdriver.FirefoxProfile() 
# adjust profile to reflect user_agent profile
profile.set_preference("general.useragent.override", user_agent)


def check_xpath(webdriver, xpath, click=False, send_keys=False, keys=None):
    """
    checks if an xpath exists on the current page

    inputs)
        > webdriver
            >> driver being used
        > xpath
            >> xpath in question
        > click
            >> if clicking the element once/if found
        > send_keys
            >> if sending keys to element once/if found
        > keys
            >> keys being sent if sending keys (i.e. send_keys=True)
    """
    # test this 
    try:
        # find xpath in question
        find_element = webdriver.find_element_by_xpath(xpath)
        # element was found, step 1 complete
        # are we clicking
        if click == True:
            # yes, so click
            find_element.click()
            # hedge time
            sleep(3)
        # are we sending keys
        if send_keys == True:
            # yes, so send them
            find_element.send_keys(keys)
            # hedge time
            sleep(3)
    # if it didn't work
    except NoSuchElementException:
        print(f'NoSuchElementException : {xpath}')
    pass


def login(username, password, opts=None, prof=None):
    """
    loads and logs in to instagram

    inputs)
        > username
            >> phone number, username, or email of account
        > password
            >> password for logging in to account
        > opt
            >> driver options 
        > pro
            >> driver profile 
    """
    # set driver w/ options
    driver = webdriver.Firefox(options=opts, firefox_profile=prof)
    # driver load instagram.com
    driver.get(ig_log_page)
    # wait (hedge load time)
    sleep(2)

    # find user input box, type out username
    driver.find_element_by_xpath(username_box).send_keys(username)
    # wait a sec
    sleep(1)

    # find pwrd input box, type out pass, then hit enter
    driver.find_element_by_xpath(password_box).send_keys(password, Keys.RETURN)
    # and wait a bit for safety 
    sleep(3)

    # take care if "save info" pop-up page pops up
    check_xpath(webdriver=driver, xpath=save_info_popup, click=True)

    # def new_post(opts=None, prof=None):
    """sets up post for sharing
    """

    # find and click button to start new post    
    driver.find_element_by_xpath(new_post_button)


# run the script
if __name__ == '__main__':
    # load login info 
    from _pile import utv, ptv  
    # log in to instagram
    login(username=utv, password=ptv, opts=options, prof=profile)
