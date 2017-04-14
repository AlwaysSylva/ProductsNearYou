DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS shops;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS taggings;
CREATE TABLE products (
        id TEXT primary key,
        shop_id TEXT,
        title TEXT,
        popularity REAL,
        quantity INTEGER
        );
CREATE TABLE shops (
        id TEXT primary key,
        name TEXT,
        lat REAL,
        lng REAL
        );
CREATE TABLE tags (
        id TEXT primary key,
        tag TEXT
        );
CREATE TABLE taggings (
        id TEXT primary key,
        shop_id TEXT,
        tag_id TEXT
        );