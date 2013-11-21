def js_click(browser, selector):
    return browser.execute_script("$('{selector}').click();".format(selector=selector))


def js_is_visible(browser, selector):
    return browser.execute_script("return $('{selector}').is(':visible');".format(selector=selector))


def no_browser_popups(browser):
    return browser.execute_script("window.onbeforeunload = function(e){};")
