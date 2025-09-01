```bash
#!/usr/bin/env bash
set -euo pipefail

# Detect privilege level
if [ "$(id -u)" -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

# Set workspace path
WORKSPACE="/home/kavia/workspace/code-generation/food-delivery-app-14946-15100/Hotel&MenuService"
cd "$WORKSPACE"

# === COMMAND: INSTALL ===
# Ensure Node development environment variables are globally set
echo 'export NODE_ENV=development' | $SUDO tee /etc/profile.d/react_env.sh >/dev/null

# === COMMAND: SCAFFOLD ===
# Scaffold new React project if none exists
if [ ! -f "$WORKSPACE/package.json" ]; then
    npx --yes create-react-app . --template cra-template --use-npm --quiet
fi

# === COMMAND: DEPS ===
# Install dependencies (idempotent); install additional TypeScript support if project uses TypeScript
if grep -q '"typescript"' package.json; then
    npm i --quiet --save-dev typescript @types/node @types/react @types/react-dom @types/jest
fi
npm i --quiet

# === COMMAND: BUILD ===
# Build the React application
npm run build --silent

# === COMMAND: TEST ===
# Run Jest tests in CI/headless mode
CI=true npm test -- --watchAll=false --silent

# === COMMAND: START ===
# Start the React development server in background on default port
NODE_ENV=development nohup npm start -- --no-open --port 3000 >/dev/null 2>&1 &
echo $! > react_app.pid

# === COMMAND: VALIDATE ===
# Check if server is up and serving on port 3000
timeout 20 bash -c 'until curl -s http://localhost:3000 > /dev/null; do sleep 1; done' || { echo "ERROR: App did not start on :3000"; exit 1; }
echo "VALIDATION SUCCESS: React dev server running at http://localhost:3000"

# === COMMAND: STOP ===
# Stop the React development server if running
if [ -f react_app.pid ]; then
    kill "$(cat react_app.pid)" 2>/dev/null || true
    rm -f react_app.pid
fi
```