"""
currency_pair
"""

from yoyo import step

__depends__ = {'20240925_02_MXLPP-exchanger'}
steps = [
    step(
    """
        CREATE TABLE IF NOT EXISTS currency_pair (
            id SERIAL PRIMARY KEY,
            currency_from_id INTEGER NOT NULL REFERENCES currency(id) ON DELETE CASCADE,
            currency_to_id INTEGER NOT NULL REFERENCES currency(id) ON DELETE CASCADE,
            exchanger_id INTEGER NOT NULL REFERENCES exchanger(id) ON DELETE CASCADE
        );
    """,
        "DROP TABLE currency_pair;"
         )
]