class Arguments:
    def __init__(self, *_):
        self.directory: str | None = None
        self.path_specified: str | None = None
        self.text_specified: str | None = None
        self.mode: str | None = None
        self.mode_init_value: str | None = None
        self.lines_displayed: str | None = None
        self.trim_text: str | None = None