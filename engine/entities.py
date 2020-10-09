from simpleflake import simpleflake
import typing


class Component:
    id: int = 0
    name: str = ""

    def __init__(self, name: str = "") -> None:
        self.id = simpleflake()
        self.name = name

    def __repr__(self) -> str:
        return f"<{Component.__name__} id='{self.id}' name='{self.name}'>"


class Entity:
    eindex: dict = {}
    cindex: dict = {}

    def __init__(self) -> None:
        self.id = simpleflake()
        self.components = {}
        self.eindex[self.id] = self

    def set_or_add_component(self, component: Component) -> None:
        component_id = type(component).__name__

        self.components[component_id] = component

        if component_id not in self.cindex:
            self.cindex[component_id] = []

        self.cindex[component_id].append(self)

    @classmethod
    def query(cls, component) -> typing.List:
        return cls.cindex.get(component) or []

    @classmethod
    def get(cls, eid) -> object:
        return cls.eindex.get(eid)

    def __repr__(self) -> str:
        return f"<{Entity.__name__} id='{self.id}' components={self.components}>"


class System:
    systems = []
    subscriptions = {}

    def __init__(self) -> None:
        self.systems.append(self)

    def update(self) -> None:
        pass

    @classmethod
    def update_all(cls) -> None:
        for system in cls.systems:
            system.update()
