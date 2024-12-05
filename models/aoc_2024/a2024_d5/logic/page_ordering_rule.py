from dataclasses import dataclass


@dataclass(frozen=True)
class PageOrderingRule:
    page_before: int
    page_after: int
