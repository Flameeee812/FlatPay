import quart as qa

from FlatPay.app.controllers.handlers import (
    index_handler, register_handler, dashboard_handler, homepage_handler, update_user_readings,
    login_handler, get_readings_info, apply_user_payment, get_user_current_debt, logout_handler
)


blueprint = qa.Blueprint('blueprint', __name__, url_prefix="FlatPay")


@blueprint.route("/", methods=["GET"])
async def index():
    return await index_handler()


@blueprint.route("/register", methods=["POST", "GET"])
async def register():
    return await register_handler()


@blueprint.route("/login", methods=["GET", "POST"])
async def login():
    return await login_handler()


@blueprint.route("/dashboard", methods=["GET"])
def dashboard():
    return dashboard_handler()


@blueprint.route("/homepage", methods=["POST", "GET"])
async def homepage():
    return await homepage_handler()


@blueprint.route("/logout", methods=["POST", "GET"])
async def logout():
    return await logout_handler()


@blueprint.route("/update_readings", methods=["POST", "GET"])
async def update_readings():
    return await update_user_readings()


@blueprint.route("/get_readings", methods=["POST", "GET"])
async def get_readings():
    return await get_readings_info()


@blueprint.route("/update_debt", methods=["POST", "GET"])
async def update_debt():
    return await apply_user_payment()


@blueprint.route("/get_debt", methods=["POST", "GET"])
async def get_debt():
    return await get_user_current_debt()
