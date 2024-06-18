from dataclasses import dataclass


@dataclass
class Business:
    business_id: str
    full_address: str
    active: str
    categories: str
    city: str
    review_count: int
    business_name: str
    neighborhoods: str
    latitude: float
    longitude: float
    state: str
    stars: float

    def __str__(self):
        return self.business_name

    def __repr__(self):
        return self.business_name

    def __hash__(self):
        return hash(self.business_id)
