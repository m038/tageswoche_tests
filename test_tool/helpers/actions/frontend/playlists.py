from test_tool.helpers.selenium_stuff import navigate


def goto_playlist(browser, playlist):
    playlist = playlist.lower()
    if playlist in ['base', 'front', 'frontpage']:
        return browser.get(navigate('/'))
    if playlist == 'basel':
        pid = 2
    if playlist == 'schweiz':
        pid = 3
    if playlist == 'international':
        pid = 4
    if playlist == 'sport':
        pid = 5
    if playlist == 'kultur':
        pid = 6
    if playlist == 'leben':
        pid = 7
    playlist_link = browser.find_element_by_xpath(
        '//*[@id="main-nav"]/nav/ul[1]/li[{0}]/a'.format(pid))
    return playlist_link.click()
