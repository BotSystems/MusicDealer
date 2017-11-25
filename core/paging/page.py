class Page:
    offset = None
    limit = None
    count = None

    def __init__(self, count, limit, offset):
        self.limit = limit
        self.offset = offset
        self.count = count

    @property
    def get_offset(self):
        return int(self.offset)

    @property
    def get_limit(self):
        return int(self.limit)

    @property
    def get_count(self):
        return int(self.count)

    @property
    def has_prev(self):
        return self.offset + self.limit > self.limit

    @property
    def has_next(self):
        return self.count - (self.offset + self.limit) >= self.limit


if __name__ == '__main__':
    pager = Page(5, 7, 5)
    print(pager.has_prev)
    print(pager.has_next)