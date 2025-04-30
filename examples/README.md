# Примеры интеграции MCP Git Server

В этой директории находятся примеры конфигурации для интеграции MCP Git Server с различными редакторами и средами.

## Claude Desktop

### Стандартная установка

Файл `claude_desktop_config.json` содержит пример конфигурации для Claude Desktop при обычной установке.

### Docker установка (рекомендуется)

Файл `claude_desktop_docker_config.json` содержит пример конфигурации для запуска через Docker, что обеспечивает более стабильную и изолированную работу.

Расположение файла конфигурации Claude Desktop:
- Windows: `%APPDATA%\Claude\config.json`
- macOS: `~/Library/Application Support/Claude/config.json`
- Linux: `~/.config/Claude/config.json`

## VS Code

Файл `.vscode/mcp.json` в корне проекта содержит пример конфигурации для VS Code.

Вы можете также добавить эту конфигурацию в настройки пользователя VS Code, открыв 
Command Palette (Ctrl+Shift+P) и выбрав "Preferences: Open User Settings (JSON)".

## Zed

Файл `zed_settings.json` содержит пример конфигурации для редактора Zed.
Скопируйте содержимое в ваш файл конфигурации Zed settings.json.

## Docker (рекомендуемый способ)

### Сборка Docker образа

Сначала соберите Docker образ с помощью скриптов в директории `scripts/`:

```bash
# Linux/macOS
./scripts/build-docker.sh

# Windows
.\scripts\build-docker.ps1
```

### Запуск через Docker

```bash
docker run --rm -i --mount type=bind,src=/path/to/repo,dst=/workspace mcp/git
```

### Доступ к разным директориям

Если вам нужен доступ к нескольким директориям:

```bash
docker run --rm -i \
  --mount type=bind,src=/path/to/dir1,dst=/projects/dir1 \
  --mount type=bind,src=/path/to/dir2,dst=/projects/dir2 \
  mcp/git
```

Подробные инструкции по настройке Docker см. в файле `DOCKER_SETUP.md` в корне проекта.