CREATE TABLE "public".menu (
    id SERIAL NOT NULL,
    title VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE "public".submenu (
    id SERIAL NOT NULL,
    title VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    menu_id BIGINT NOT NULL REFERENCES "public".menu (id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

CREATE TABLE "public".dish (
    id SERIAL NOT NULL,
    title VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    price NUMERIC(10, 3) NOT NULL,
    CHECK (price > 0),
    submenu_id BIGINT NOT NULL REFERENCES "public".submenu (id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);