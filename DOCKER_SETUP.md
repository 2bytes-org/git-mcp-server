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
        "--mount", "type=bind,src=C:/Users/username/Documents,dst=/workspace",
        "mcp/git"
      ]
    }
  }
}
```

**ВАЖНО!** Замените `C:/Users/username/Documents` на абсолютный путь к вашей директории с проектами:
- Используйте прямые слеши `/` даже в Windows
- Путь должен быть абсолютным (не используйте переменные вроде `${workspaceFolder}`)
- Убедитесь, что указанная директория существует

### 3. Проверка настройки

Перезапустите Claude Desktop и убедитесь, что вы можете использовать Git-команды через MCP.

## Доступ к различным директориям

Если вам нужен доступ к нескольким директориям, вы можете изменить конфигурацию следующим образом:

```json
{
  "mcpServers": {
    "git": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount", "type=bind,src=C:/path/to/dir1,dst=/projects/dir1",
        "--mount", "type=bind,src=C:/path/to/dir2,dst=/projects/dir2",
        "mcp/git"
      ]
    }
  }
}
```

## Устранение проблем

### Проблемы с путями

Наиболее распространенная ошибка - это неправильно указанные пути в конфигурации:

```
Error response from daemon: invalid mount config for type "bind": invalid mount path: '${workspaceFolder}' mount path must be absolute
```

Решение:
- Убедитесь, что вы используете абсолютные пути (например, `C:/Users/username/Documents`)
- Используйте прямые слеши `/` вместо обратных `\`, даже в Windows
- Не используйте переменные типа `${workspaceFolder}` - они не поддерживаются в Claude Desktop

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
"--mount", "type=bind,src=C:/path/to/logs,dst=/home/mcpuser/.logs"
```