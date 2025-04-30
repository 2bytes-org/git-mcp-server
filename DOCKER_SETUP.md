# Установка и использование MCP Git Server через Docker

## Требования

- Docker
- Git (установленный на хосте)
- Claude Desktop

## Установка и настройка

### 1. Сборка Docker-образа

Выполните следующие команды для сборки Docker-образа:

#### Linux/macOS:
```bash
# Клонировать репозиторий
git clone https://github.com/2bytes-org/git-mcp-server.git
cd git-mcp-server

# Сделать скрипт исполняемым
chmod +x scripts/build-docker.sh

# Запустить сборку
./scripts/build-docker.sh
```

#### Windows:
```powershell
# Клонировать репозиторий
git clone https://github.com/2bytes-org/git-mcp-server.git
cd git-mcp-server

# Запустить сборку через PowerShell
.\scripts\build-docker.ps1
```

### 2. Настройка Claude Desktop

1. Откройте файл конфигурации Claude Desktop:
   - Windows: `%APPDATA%\Claude\config.json`
   - macOS: `~/Library/Application Support/Claude/config.json`
   - Linux: `~/.config/Claude/config.json`

2. Добавьте следующую конфигурацию в файл:

```json
{
  "mcpServers": {
    "git": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount", "type=bind,src=${workspaceFolder},dst=/workspace",
        "mcp/git"
      ]
    }
  }
}
```

### 3. Проверка настройки

Перезапустите Claude Desktop и убедитесь, что вы можете использовать Git-команды через MCP.

## Доступ к различным директориям

Если вы хотите предоставить доступ к нескольким директориям, вы можете изменить конфигурацию следующим образом:

```json
{
  "mcpServers": {
    "git": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount", "type=bind,src=/path/to/dir1,dst=/projects/dir1",
        "--mount", "type=bind,src=/path/to/dir2,dst=/projects/dir2",
        "mcp/git"
      ]
    }
  }
}
```

## Устранение проблем

### Проблемы с правами доступа

Если у вас возникают проблемы с правами доступа, убедитесь, что:

1. Docker имеет права на доступ к монтируемым директориям
2. Пользователь `mcpuser` в контейнере (UID 1000) имеет права на запись в монтируемые директории

### Проблемы с подключением

Если Claude Desktop не может подключиться к MCP Git Server, проверьте:

1. Образ Docker успешно собран (`docker images` должен показывать `mcp/git`)
2. Docker демон запущен и работает
3. В логах Claude Desktop нет ошибок

### Логи и отладка

Для просмотра логов запустите:

```bash
docker logs $(docker ps -q --filter "ancestor=mcp/git")
```

Или добавьте монтирование директории логов:

```json
"--mount", "type=bind,src=/path/to/logs,dst=/home/mcpuser/.logs"
```