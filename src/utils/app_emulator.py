"""
Flow Executor
"""

from sqlalchemy import Engine
from logging import getLogger
from flows.flow import FlowSet
from .config import AppEmulatorConfig
from .db import get_session


class AppEmulator:
    logger = getLogger("emulator")

    def __init__(self, config: AppEmulatorConfig, engines: dict[str, Engine]):
        self.size = config.flow_size
        self.engines = engines

    def run(self, flow_set: FlowSet):
        self.logger.info(f"Starting App Emulator with {self.size} iterations")
        for _ in range(self.size):
            flow = flow_set.get_random_flow()
            engine = self.engines.get(flow.db_conn)
            session, session_meta = get_session(engine)
            with session:
                flow.run_flow(session)

            self.logger.info(
                f"Flow {flow.name} terminated. {session_meta.transaction_count} Transactions(s) made."
            )
