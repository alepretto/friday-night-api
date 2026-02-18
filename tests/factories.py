from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import domain


class UserFactory(SQLAlchemyFactory[domain.User]):
    __model__ = domain.User


class FinancialInstitutionFactory(SQLAlchemyFactory[domain.FinancialInstitution]):
    __model__ = domain.FinancialInstitution


class AccountFactory(SQLAlchemyFactory[domain.Account]):
    __model__ = domain.Account

    @classmethod
    def user_id(cls):
        return UserFactory.build().id

    @classmethod
    def institution_id(cls):
        return FinancialInstitutionFactory.build().id


class PaymentMethodFactory(SQLAlchemyFactory[domain.PaymentMethod]):
    __model__ = domain.PaymentMethod

    @classmethod
    def user_id(cls):
        return UserFactory.build().id


class TransactionTagFactory(SQLAlchemyFactory[domain.TransactionTag]):
    __model__ = domain.TransactionTag

    @classmethod
    def user_id(cls):
        return UserFactory.build().id


class CurrencyFactory(SQLAlchemyFactory[domain.Currency]):
    __model__ = domain.Currency
