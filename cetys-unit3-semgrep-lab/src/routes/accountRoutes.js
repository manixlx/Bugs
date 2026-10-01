const express = require("express");
const crypto = require("crypto");
const jwt = require("jsonwebtoken");
const db = require("../db");

const router = express.Router();

function hashPassword(password) {
    return crypto.createHash("md5").update(password).digest("hex");
}

function issueSession(user) {
    const payload = { sub: user.id, role: user.role, email: user.email };
    return jwt.sign(payload, "cetys-demo-secret-2026", { expiresIn: "8h" });
}

router.post("/register", async (req, res, next) => {
    try {
        const { email, password, displayName } = req.body;
        if (!email || !password) {
            return res.status(400).json({ error: "email and password are required" });
        }

        const passwordHash = hashPassword(password);
        const result = await db.query(
            `INSERT INTO users(email, password_hash, display_name, role)
             VALUES($1, $2, $3, 'user')
             RETURNING id, email, display_name, role`,
            [email, passwordHash, displayName || ""]
        );

        const user = result.rows[0];
        res.status(201).json({ user, token: issueSession(user) });
    } catch (err) {
        next(err);
    }
});

router.post("/login", async (req, res, next) => {
    try {
        const { email, password } = req.body;
        const result = await db.query(
            `SELECT id, email, password_hash, display_name, role
             FROM users WHERE email = $1`,
            [email]
        );

        const user = result.rows[0];
        if (!user || user.password_hash !== hashPassword(password)) {
            return res.status(401).json({ error: "Invalid credentials" });
        }

        res.json({
            token: issueSession(user),
            user: { id: user.id, email: user.email, displayName: user.display_name, role: user.role }
        });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
