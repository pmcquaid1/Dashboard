// sass.config.js
const { execSync } = require("child_process");

const isProd = process.env.NODE_ENV === "production";

const input = "static/scss/main.scss";
const output = "static/css/main.css";

const flags = isProd
  ? "--no-source-map --style=compressed"
  : "--style=expanded";

const command = `sass ${flags} ${input} ${output}`;

console.log(`Running: ${command}`);
execSync(command, { stdio: "inherit" });
