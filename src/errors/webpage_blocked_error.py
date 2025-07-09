class WebpageBlockedError(Exception):
    """
    Exception for attempting to scrape web pages blocked by robots.txt.

    Parameters:
            message (str): Error message. Defaults to "The URL you are trying to scrape is blocked by robots.txt".
            error_code (int | None): Optional HTTP error code. Defaults to 403.
    """

    def __init__(
        self,
        message: str = "The URL you are trying to scrape is blocked by robots.txt",
        error_code: int | None = 403,
    ):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        """
        Get a string representation of the error.

        Returns:
            str: String with the error plus the error code if there is one.
        """
        if self.error_code:
            return f"{self.args[0]} (Error Code: {self.error_code})"
        return self.args[0]
