from utils.config import load_config
from utils.logging import setup_logging
from utils.app_emulator import AppEmulator
from flows.flow import FlowSet
from flows.user_signup import UserSignupFlow
from utils.db import get_engine


def main():
    config = load_config("config/default.toml")

    setup_logging(config.logging)

    engines = {db.name: get_engine(db) for db in config.databases}

    flow_set = FlowSet({"user_sign_up": UserSignupFlow("main_db")})

    emulator = AppEmulator(config.emulator, engines)

    emulator.run(flow_set)


if __name__ == "__main__":
    main()

# from utils import URL
# from utils.db import get_engine, get_session
# from utils.fakerwrapper import get_faker


# url = URL.create(
#     drivername="postgresql",
#     username="postgres",
#     password="postgres",
#     host="localhost",
#     port=5432,
#     database="sample_db",
# )
# engine = get_engine(url)
# session, session_meta = get_session(engine)

# faker = get_faker()


# # with Session(engine) as session:
# #     FlowProvider = DynamicProvider(
# #         provider_name="flow",
# #         elements=[UserSignupFlow(session)],
# #     )
# #     faker.add_provider(FlowProvider)

# #     flow = faker.flow()
# #     flow.execute()
