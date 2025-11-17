#!/bin/zsh
# Script to build Hora Widget macOS application

echo "🔨 Building Hora Widget application..."

# Activate virtual environment
source venv/bin/activate

# Load environment variables
export $(cat .env | xargs) 2>/dev/null || true

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the application
echo "📦 Building .app bundle..."
python setup.py py2app

# Check if build was successful
if [ -d "dist/Hora Widget.app" ]; then
    echo "✅ Successfully built: dist/Hora Widget.app"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Copy to Applications: cp -r 'dist/Hora Widget.app' /Applications/"
    echo "  2. Double-click to launch from Applications folder"
    echo "  3. Or run directly: open 'dist/Hora Widget.app'"
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi
