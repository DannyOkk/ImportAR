from abc import ABC, abstractmethod
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.hash import pbkdf2_sha256

class EncrypterService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def check_password(self, stored_password_hash: str, provided_password: str) -> bool:
        pass

class StandardEncrypterService(EncrypterService):
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password.
        :param password: The plain text password to hash.
        :return: The hashed password.
        """
        return generate_password_hash(password)

    @staticmethod
    def check_password(stored_password_hash: str, provided_password: str) -> bool:
        """
        Verify a provided password against the stored password hash.
        :param stored_password_hash: The hashed password stored in the database.
        :param provided_password: The plain text password to verify.
        :return: True if the password matches, else False.
        """
        return check_password_hash(stored_password_hash, provided_password)

class PasslibEncrypterService(EncrypterService):
     
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password using PBKDF2.
        :param password: The plain text password to hash.
        :return: The hashed password.
        """
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def check_password(stored_password_hash: str, provided_password: str) -> bool:
        """
        Verify a provided password against the stored PBKDF2 password hash.
        :param stored_password_hash: The hashed password stored in the database.
        :param provided_password: The plain text password to verify.
        :return: True if the password matches, else False.
        """
        return pbkdf2_sha256.verify(provided_password, stored_password_hash)
    
class EncrypterManager:
    _encrypter: EncrypterService = StandardEncrypterService()

    @classmethod
    def set_encrypter(cls, encrypter: EncrypterService):
        cls._encrypter = encrypter

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls._encrypter.hash_password(password)

    @classmethod
    def check_password(cls, stored_password_hash: str, provided_password: str) -> bool:
        return cls._encrypter.check_password(stored_password_hash, provided_password)