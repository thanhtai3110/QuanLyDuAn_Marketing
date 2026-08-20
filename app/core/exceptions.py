class NotFoundException(Exception):
    def __init__(self, message: str = "Không tìm thấy tài nguyên"):
        self.message = message


class BadRequestException(Exception):
    def __init__(self, message: str = "Yêu cầu không hợp lệ"):
        self.message = message


class ForbiddenException(Exception):
    def __init__(self, message: str = "Bạn không có quyền thực hiện thao tác này"):
        self.message = message