from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import domain


class UserFactory(SQLAlchemyFactory[domain.User]):
    __model__ = domain.User


class FinancialInstitutionFactory(SQLAlchemyFactory[domain.FinancialInstitution]):
    __model__ = domain.FinancialInstitution
