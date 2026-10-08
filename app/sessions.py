"""In-memory session store: history + consecutive-failure counter."""
from dataclasses import dataclass, field

MAX_TURNS = 10


@dataclass
class Session:
    history: list[dict] = field(default_factory=list)    # {"role": "user"|"assistant", "content": str}
    failures: int = 0
    articles_tried: list[str] = field(default_factory=list)
    last_user_issue: str = ""

    def add_user(self, text: str) -> None:
        self.history.append({"role": "user", "content": text})
        self.history = self.history[-2 * MAX_TURNS:]

    def add_assistant(self, text: str) -> None:
        self.history.append({"role": "assistant", "content": text})
        self.history = self.history[-2 * MAX_TURNS:]

    def record(self, status: str, urls: list[str] | None = None) -> None:
        """answered resets the counter; clarify/out_of_scope increment it."""
        for u in urls or []:
            if u not in self.articles_tried:
                self.articles_tried.append(u)
        self.failures = 0 if status == "answered" else self.failures + 1


_STORE: dict[str, Session] = {}


def get_session(session_id: str) -> Session:
    return _STORE.setdefault(session_id, Session())


def reset_all() -> None:
    _STORE.clear()