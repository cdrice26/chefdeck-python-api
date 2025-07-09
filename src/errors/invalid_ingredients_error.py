class InvalidIngredientsError(Exception):
    """
    Exception for invalid ingredients.

    Parameters:
            message (str): Error message. Defaults to "Each ingredient must have 'amount', 'unit', and 'name'".
            error_code (int | None): Optional HTTP error code. Defaults to 400.
    """

    def __init__(
        self,
        message: str = "Each ingredient must have 'amount', 'unit', and 'name'",
        error_code: int | None = 400,
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
