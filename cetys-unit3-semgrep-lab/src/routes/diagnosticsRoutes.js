const express = require("express");
const { exec } = require("child_process");

const router = express.Router();

router.get("/ping", (req, res) => {
    const host = String(req.query.host || "").trim();
    if (!host) return res.status(400).json({ error: "host query parameter is required" });

    const command = `ping -c 2 ${host}`;
    exec(command, { timeout: 5000 }, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ ok: false, command, stderr: stderr || error.message });
        }
        res.json({ ok: true, command, output: stdout });
    });
});

module.exports = router;
