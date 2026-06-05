CREATE TABLE IF NOT EXISTS raw_events (
    id SERIAL PRIMARY KEY,
    page TEXT NOT NULL,
    user_id TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS page_stats (
    page TEXT PRIMARY KEY,
    total_views INT NOT NULL,
    unique_users INT NOT NULL,
    last_updated TIMESTAMP NOT NULL DEFAULT NOW()
);