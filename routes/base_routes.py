from flask import Blueprint

class BaseRoutes:
    def __init__(self, name, controller):
        self.controller = controller
        self.blueprint = Blueprint(name, __name__)
        plural_name = f"{name[:-1]}ies" if name[-1] == "y" else name + ("es" if name[-1] == "s" else "s")

        self.blueprint.add_url_rule(f"/{name}", methods=["POST"], view_func=controller.add_record)
        self.blueprint.add_url_rule(f"/{plural_name}", methods=["GET"], view_func=controller.get_all_records)
        self.blueprint.add_url_rule(f"/{name}/<record_id>", methods=["GET"], view_func=controller.get_record_by_id)
        self.blueprint.add_url_rule(f"/{name}/<record_id>", methods=["PUT"], view_func=controller.update_record)
        self.blueprint.add_url_rule(F"/{name}/<record_id>", methods=["DELETE"], view_func=controller.delete_record)
