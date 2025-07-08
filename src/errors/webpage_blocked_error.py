class WebpageBlockedError(Exception):
    def __init__(
        self,
        message: str = "The URL you are trying to scrape is blocked by robots.txt",
        error_code: int | None = 403,
    ):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"{self.args[0]} (Error Code: {self.error_code})"
        return self.args[0]
