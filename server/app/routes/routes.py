import quart as qa

from server.app.handlers import (
    home_handler, registration, delete_user_passport,
    update_user_readings, get_readings_info,
    apply_user_payment, get_debt_info
)


blueprint = qa.Blueprint('blueprint', __name__)


@blueprint.route("/", methods=["GET"])
async def home():
    return await home_handler()


@blueprint.route("/reg_user", methods=["POST", "GET"])
async def reg_user():
    return await registration()


@blueprint.route("/delete_user", methods=["POST", "GET"])
async def delete_user():
    return await delete_user_passport()


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
    return await get_debt_info()
