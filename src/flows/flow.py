"""
Abstract base class for a flow
"""

from sqlalchemy.orm import Session
from logging import getLogger
from abc import ABC, abstractmethod
import random


class Flow(ABC):
    def __init__(self, name: str):
        self.__name = name
        self.logger = getLogger("flow")
        self.logger.debug(f"Flow {self.name} initialized")

    @abstractmethod
    def execute(self, session: Session):
        pass

    def run_flow(self, session: Session):
        self.logger.debug(f"Running flow: {self.name}")
        self.execute(session)
        self.logger.debug(f"Flow {self.name} completed")

    @property
    def name(self) -> str:
        return self.__name

    @property
    @abstractmethod
    def db_conn(self) -> str:
        """Abstract property for database connection name."""
        pass


class FlowSet:
    """
    A collection of flows that can yield random flows for execution.
    Acts as both a container and a generator for flows.
    """

    def __init__(self, flows=None):
        self.flows = flows if flows is not None else {}
        self.logger = getLogger("flow")

    def add_flow(self, flow):
        """Add a flow to the set."""
        self.flows[flow.name] = flow
        self.logger.info(f"Added flow '{flow.name}' to FlowSet")

    def remove_flow(self, flow_name: str):
        """Remove a flow from the set by name."""
        removed_flow = self.flows.pop(flow_name, None)
        if removed_flow:
            self.logger.info(f"Removed flow '{flow_name}' from FlowSet")
        return removed_flow

    def get_flow(self, flow_name: str):
        """Get a specific flow by name."""
        return self.flows.get(flow_name)

    def get_random_flow(self):
        """Get a single random flow from the set."""
        if not self.flows:
            self.logger.warning("No flows available in FlowSet")
            return None

        flow_name = random.choice(list(self.flows.keys()))
        flow = self.flows[flow_name]
        self.logger.debug(f"Selected random flow: {flow_name}")
        return flow

    def __len__(self):
        """Return the number of flows in the set."""
        return len(self.flows)

    def __iter__(self):
        """Make FlowSet iterable, yielding flows in random order."""
        flow_names = list(self.flows.keys())
        random.shuffle(flow_names)

        for flow_name in flow_names:
            yield self.flows[flow_name]

    def __call__(self):
        """Make FlowSet callable, returning a random flow."""
        return self.get_random_flow()

    def generate_flows(self, count=None):
        """
        Generator that yields random flows indefinitely or for a specified count.

        Args:
            count: Number of flows to generate. If None, generates indefinitely.

        Yields:
            Random Flow instances from the set.
        """
        if not self.flows:
            self.logger.warning("No flows available for generation")
            return

        generated = 0
        while count is None or generated < count:
            yield self.get_random_flow()
            generated += 1

    def get_flow_names(self):
        """Get a list of all flow names in the set."""
        return list(self.flows.keys())

    def is_empty(self):
        """Check if the FlowSet is empty."""
        return len(self.flows) == 0

    def clear(self):
        """Remove all flows from the set."""
        self.flows.clear()
        self.logger.info("Cleared all flows from FlowSet")
