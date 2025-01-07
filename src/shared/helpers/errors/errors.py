class BaseError(Exception):
    def __init__(self, message: str):
        self.__message: str = message
        super().__init__(message)

    @property
    def message(self):
        return self.__message

class EntityError(BaseError):
    def __init__(self, message: str):
        super().__init__(f"Parâmetro inválido: {message}")

class MissingParameters(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Parâmetro ausente: {message}')

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Nenhum item encontrado: {message}')

class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Item duplicado: {message}')
        
class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Ação não permitida: {message}')

class DatabaseException(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Erro no banco de dados: {message}')