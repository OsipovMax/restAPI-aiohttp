from aiohttp import web
import json
import random
import os


class Service:
    def __init__(self):
        application = web.Application()
        application.add_routes(
            [
                web.get("/", self.handle_get),
                web.get("/{id}", self.handle_get_id),
                web.put("/edit/{id}", self.handle_edit),
                web.put("/delete/{id}", self.handle_remove_id),
                web.post("/add", self.handle_post),
            ]
        )
        web.run_app(application)

    async def handle_get(self, request):
        try:
            with open("db.json", "r") as f:
                users = json.load(f)
            users_list = [user["name"] for user in users]
            return web.Response(text=str(users_list), status=200)
        except Exception as err:
            response_object = {"status": "failed", "reason": str(err)}
            return web.Response(text=json.dumps(response_object), status=500)

    async def handle_get_id(self, request):
        try:
            id = int(request.match_info["id"])
            with open("db.json", "r") as f:
                users = json.load(f)
            for user in users:
                if user["id"] == id:
                    return web.Response(text=str(user["name"]), status=200)
            return web.Response(text="No user with such id", status=400)
        except Exception as err:
            response_object = {"status": "failed", "reason": str(err)}
            return web.Response(text=json.dumps(response_object), status=500)

    async def handle_edit(self, request):
        try:
            id = int(request.match_info["id"])
            with open("db.json", "r") as f:
                users = json.load(f)
            for user in users:
                if user["id"] == id:
                    user["name"] = request.query["name"]
                    with open("db.json", "w") as f:
                        f.write(json.dumps(users))
                    return web.Response(text="Successful change", status=200)
            return web.Response(text="No user with such id", status=400)
        except Exception as err:
            response_object = {"status": "failed", "reason": str(err)}
            return web.Response(text=json.dumps(response_object), status=500)

    async def handle_remove_id(self, request):
        try:
            id = int(request.match_info["id"])
            with open("db.json", "r") as f:
                users = json.load(f)
            for user in users:
                if user["id"] == id:
                    users.remove(user)
                    with open("db.json", "w") as f:
                        f.write(json.dumps(users))
                    return web.Response(text="Successful change", status=200)
            return web.Response(text="No user with such id", status=400)
        except Exception as err:
            response_object = {"status": "failed", "reason": str(err)}
            return web.Response(text=json.dumps(response_object), status=500)

    async def handle_post(self, request):
        try:
            user = {"id": 0, "name": ""}
            user["id"] = random.randint(1, 100000)
            user["name"] = request.query["name"]
            user_array = json.loads(open("db.json").read())
            user_array.append(user)
            with open("db.json", "w") as f:
                f.write(json.dumps(user_array))
            return web.Response(text="Succesful change", status=200)
        except Exception as e:
            response_obj = {"status": "failed", "reason": str(e)}
            return web.Response(text=json.dumps(response_obj), status=500)


if __name__ == "__main__":
    if os.stat("db.json").st_size == 0:
        initial_user_list = []
        with open("db.json", "w") as f:
            f.write(json.dumps(initial_user_list))
    restApi = Service()
