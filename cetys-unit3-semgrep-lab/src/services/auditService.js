const fs = require("fs");
const path = require("path");

const LOG_FILE = path.join(__dirname, "..", "..", "audit.log");

function recordSecurityEvent(event) {
    const line = JSON.stringify({
        timestamp: new Date().toISOString(),
        type: event.type,
        userId: event.userId || null,
        ip: event.ip || null,
        metadata: event.metadata || {}
    });
    fs.appendFileSync(LOG_FILE, line + "\n");
}

function recordLoginFailure(req, email) {
    recordSecurityEvent({
        type: "LOGIN_FAILURE",
        userId: null,
        ip: req.ip,
        metadata: { attemptedEmail: email, userAgent: req.get("user-agent") }
    });
}

module.exports = { recordSecurityEvent, recordLoginFailure };
