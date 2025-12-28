@echo off
REM Clear the Claude Code plugin cache for nethercore-ai-plugins
REM Run this after making changes to plugin files

set CACHE_DIR=%USERPROFILE%\.claude\plugins\cache\nethercore-ai-plugins

if exist "%CACHE_DIR%" (
    rmdir /s /q "%CACHE_DIR%"
    echo Cleared: %CACHE_DIR%
    echo Restart Claude Code to reload plugins
) else (
    echo Cache directory not found: %CACHE_DIR%
)
