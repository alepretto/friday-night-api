from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import domain


class UserFactory(SQLAlchemyFactory[domain.User]):
    __model__ = domain.User

    __set_relationships__ = False


class FinancialInstitutionFactory(SQLAlchemyFactory[domain.FinancialInstitution]):
    __model__ = domain.FinancialInstitution

    __set_relationships__ = False


class AccountFactory(SQLAlchemyFactory[domain.Account]):
    __model__ = domain.Account

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id

    @classmethod
    def institution_id(cls):
        return FinancialInstitutionFactory.build().id


class PaymentMethodFactory(SQLAlchemyFactory[domain.PaymentMethod]):
    __model__ = domain.PaymentMethod

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id


class TransactionTagFactory(SQLAlchemyFactory[domain.TransactionTag]):
    __model__ = domain.TransactionTag

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id


class CurrencyFactory(SQLAlchemyFactory[domain.Currency]):
    __model__ = domain.Currency

    __set_relationships__ = False


class TransactionFactory(SQLAlchemyFactory[domain.Transaction]):
    __model__ = domain.Transaction

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build()

    @classmethod
    def account_id(cls):
        return AccountFactory.build()

    @classmethod
    def transaction_tag_id(cls):
        return TransactionTagFactory.build().id

    @classmethod
    def payment_method_id(cls):
        return PaymentMethodFactory.build().id

    @classmethod
    def currency_id(cls):
        return CurrencyFactory.build().id
