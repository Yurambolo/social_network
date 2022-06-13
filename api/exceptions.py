class LikeError(Exception):
    def __init__(self, message="Something went wrong during liking"):
        self.message = message
        super().__init__(self.message)
