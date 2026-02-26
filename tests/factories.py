from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import domain
from app import modules


class UserFactory(SQLAlchemyFactory[modules.User]):
    __model__ = modules.User

    __set_relationships__ = False


class FinancialInstitutionFactory(
    SQLAlchemyFactory[modules.finance.FinancialInstitution]
):
    __model__ = modules.finance.FinancialInstitution

    __set_relationships__ = False


class AccountFactory(SQLAlchemyFactory[modules.finance.Account]):
    __model__ = modules.finance.Account

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id

    @classmethod
    def institution_id(cls):
        return FinancialInstitutionFactory.build().id


class PaymentMethodFactory(SQLAlchemyFactory[modules.finance.PaymentMethod]):
    __model__ = modules.finance.PaymentMethod

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id


class CategoryFactory(SQLAlchemyFactory[modules.finance.Category]):
    __model__ = modules.finance.Category

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id


class SubcategoryFactory(SQLAlchemyFactory[modules.finance.Subcategory]):
    __model__ = modules.finance.Subcategory

    __set_relationships__ = False

    @classmethod
    def category_id(cls):
        return CategoryFactory.build().id


class TagFactory(SQLAlchemyFactory[modules.finance.Tag]):
    __model__ = modules.finance.Tag

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id

    @classmethod
    def category_id(cls):
        return CategoryFactory.build().id

    @classmethod
    def subcategory_id(cls):
        return SubcategoryFactory.build().id


class CurrencyFactory(SQLAlchemyFactory[modules.finance.Currency]):
    __model__ = modules.finance.Currency

    __set_relationships__ = False


class TransactionFactory(SQLAlchemyFactory[modules.finance.Transaction]):
    __model__ = modules.finance.Transaction

    __set_relationships__ = False

    @classmethod
    def user_id(cls):
        return UserFactory.build().id

    @classmethod
    def account_id(cls):
        return AccountFactory.build().id

    @classmethod
    def tag_id(cls):
        return TagFactory.build().id

    @classmethod
    def payment_method_id(cls):
        return PaymentMethodFactory.build().id

    @classmethod
    def currency_id(cls):
        return CurrencyFactory.build().id


class HoldingFactory(SQLAlchemyFactory[domain.Holding]):
    __model__ = domain.Holding

    __set_relationships__ = False
