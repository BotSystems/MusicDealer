def do_download():
    pass


def do_forward():
    pass


def get_download_strategy(download_link):
    if (StrategyLink.find(download_link)):
        return do_forward
    return do_download

