def js_click(browser, selector):
    return browser.execute_script("$('{selector}').click();".format(selector=selector))


def js_is_visible(browser, selector):
    return browser.execute_script("return $('{selector}').is(':visible');".format(selector=selector))


def no_browser_popups(browser):
    browser.execute_script("window.original_onbeforeunload_function = window.onbeforeunload")
    browser.execute_script("window.onbeforeunload = function(e){};")


def restore_no_browser_popups(browser):
    browser.execute_script("window.onbeforeunload = window.original_onbeforeunload_function")


def handle_js_confirm(browser, accept=True):
    if accept:
        accept = 'true'
    else:
        accept = 'false'
    browser.execute_script("window.original_confirm_function = window.confirm")
    browser.execute_script("window.confirm = function(msg) {{ return {accept}; }}".format(accept=accept))


def restore_js_confirm(browser):
    browser.execute_script("window.confirm = window.original_confirm_function")

