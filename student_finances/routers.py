"""
modified router to allow for easier mongo filtration
"""
class MongoRouter:
    """
    A router to control all database operations on models in the
    Transaction application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read Transaction models go to mongodb.
        """
        print(model._meta.model_name)
        print("-----")
        if model._meta.model_name == 'transaction':
            return 'mongodb'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write Transaction models go to mongodb.
        """
        print(model._meta.model_name)
        print("-----")
        if model._meta.model_name == 'transaction':
            return 'mongodb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the Transaction app is involved.
        """
        if obj1._meta.model_name == 'transaction' or \
           obj2._meta.model_name == 'transaction':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the Transaction app only appears in the 'mongodb'
        database.
        """
        if model_name == 'transaction':
            return db == 'mongodb'
        return None