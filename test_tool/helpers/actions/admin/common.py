from test_tool.settings import DEFAULT_WAIT, LONG_AJAX, MAX_WAIT
from test_tool.helpers.selenium_stuff import(
    wait_for_visible_by_css, )


def wait_for_flash(browser):
    try:
        wait_for_visible_by_css(browser, MAX_WAIT, 'div.flash')
    except Exception:
        pass
