const { Pool } = require("pg");

const pool = new Pool({
    host: process.env.DB_HOST || "localhost",
    port: Number(process.env.DB_PORT || 5432),
    database: process.env.DB_NAME || "security_lab",
    user: process.env.DB_USER || "lab_user",
    password: process.env.DB_PASSWORD || "lab_password"
});

async function query(sql, params = []) {
    return pool.query(sql, params);
}

module.exports = { query };
