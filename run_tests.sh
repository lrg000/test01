#!/bin/bash

echo "Activating virtual environment..."
source venv/Scripts/activate

echo "Running tests with pytest..."
pytest --html=report.html --self-contained-html

echo "Opening report.html..."

# 根据操作系统打开 HTML 报告
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    explorer.exe report.html
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open report.html
elif command -v open >/dev/null 2>&1; then
    open report.html
else
    echo "请手动打开 report.html 文件"
fi
