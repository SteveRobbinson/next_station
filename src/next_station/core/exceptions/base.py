class UnifiedAPIError(Exception):
    def __init__(self, source: str, status_code: int, details: str):
        self.source = source
        self.status_code = status_code
        self.details = details
        
        title = f"{source} - Status code: {status_code}\nDetails: {details}"

        super().__init__(title)
