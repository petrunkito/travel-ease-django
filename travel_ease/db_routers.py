class WarehouseRouter:
    """Keep Django migrations away from the read-only warehouse database."""

    warehouse_alias = 'dw'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db != self.warehouse_alias
