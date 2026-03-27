CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    sn NOT NULL,
    feature_id INTEGER,
    machine,
    value,
    lsl, 
    usl,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(feature_id) REFERENCES features(id)
);

CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    machine TEXT,
    units,
    lsl, 
    usl,
    product_id,
    FOREIGN KEY(product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    measurement_id,
    note_text TEXT,
    FOREIGN KEY(measurement_id) REFERENCES measurements(id)
)