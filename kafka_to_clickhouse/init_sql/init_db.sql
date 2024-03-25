CREATE TABLE IF NOT EXISTS user
(
    user_id String,
    timestamp DateTime,
    value String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, user_id);

CREATE TABLE IF NOT EXISTS film
(
    user_id String,
    timestamp DateTime,
    value String,
    film_id String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, user_id);