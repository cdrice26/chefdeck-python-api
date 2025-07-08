class InvalidIngredientsError(Exception):
    def __init__(
        self,
        message: str = "Each ingredient must have 'amount', 'unit', and 'name'",
        error_code: int | None = 400,
    ):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"{self.args[0]} (Error Code: {self.error_code})"
        return self.args[0]
