## Financial Transaction Analysis Microservice
-[English](#financial-transaction-analysis-microservice)  
-[Русский](#микросервис-анализа-финансовых-транзакций)

A microservice for processing and analyzing financial transactions, built with FastAPI, Celery, and PostgreSQL.

### Features
- Transaction processing via REST API
- Real-time statistics calculation
- Top-3 transaction analysis using heap algorithm
- Currency-based transaction breakdown
- Asynchronous task processing
- API key authentication

### Tech Stack
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker
- SQLAlchemy

### Installation and Setup

#### Using Docker (recommended)
1. Clone the repository:
```bash
git clone git@github.com:imelbow/TestWork006.git
cd TestWork006
```

2. Create a `.env` file in the root directory and add this example:
```env
DATABASE_URL=postgresql://user:password@db:5432/transactions_db
REDIS_URL=redis://redis:6379/0
API_KEY=your-secret-api-key
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=transactions_db
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The service will be available at `http://localhost:8000`

#### Local Development Setup
1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL and Redis locally:

##### PostgreSQL Setup
- Install PostgreSQL:
  ```bash
  # MacOS
  brew install postgresql@14
  brew services start postgresql@14

  # Ubuntu/Debian
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  sudo systemctl start postgresql
  sudo systemctl enable postgresql

  # Windows
  # Download the installer from https://www.postgresql.org/download/windows/
  # Run the installer and follow the instructions
  ```

- Create the database and user:
  ```bash
  # For MacOS/Linux
  sudo -u postgres psql

  # For Windows
  # Open SQL Shell (psql) from the Start menu
  ```

- In the PostgreSQL command line:
  ```sql
  CREATE DATABASE transactions_db;
  CREATE USER user WITH PASSWORD 'password';
  GRANT ALL PRIVILEGES ON DATABASE transactions_db TO user;

  # Important additional step for PostgreSQL 15+
  \c transactions_db
  GRANT ALL ON SCHEMA public TO user;
  \q
  ```

If you are not familiar with PostgreSQL, you can access the PostgreSQL command line by running the `psql` command or `sudo -u postgres psql`, depending on your system.

##### Redis Setup
- Install Redis:
  ```bash
  # MacOS
  brew install redis
  brew services start redis

  # Ubuntu/Debian
  sudo apt update
  sudo apt install redis-server
  sudo systemctl start redis-server
  sudo systemctl enable redis-server

  # Windows
  # Install Windows Subsystem for Linux (WSL2) and install Redis there
  # Or use the Windows installer from https://github.com/microsoftarchive/redis/releases
  ```

- Verify Redis installation:
  ```bash
  redis-cli ping
  # Should return PONG
  ```

- Basic Redis configuration (optional):
  ```bash
  # Edit Redis configuration
  sudo nano /etc/redis/redis.conf

  # Key settings to consider:
  # bind 127.0.0.1
  # port 6379
  # requirepass your_password
  ```

4. Create a `.env` file with local configuration:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/transactions_db
REDIS_URL=redis://localhost:6379/0
API_KEY=your-secret-api-key
```

5. Run the services:
```bash
# Terminal 1: FastAPI
uvicorn src.main:app --reload

# Terminal 2: Celery Worker
celery -A src.tasks.celery_tasks worker --loglevel=info

# Terminal 3: Celery Beat
celery -A src.tasks.celery_tasks beat --loglevel=info
```

### API Documentation

API documentation is available through:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Endpoints

1. `POST /api/v1/transactions`
   - Creates a new transaction
   - Requires API key authentication
   - Request body example:
```json
{
    "transaction_id": "123456",
    "user_id": "user_001",
    "amount": 150.50,
    "currency": "USD",
    "timestamp": "2024-03-20T12:00:00Z"
}
```

2. `GET /api/v1/statistics`
   - Returns transaction statistics
   - Requires API key authentication
   - Response example:
```json
{
    "total_transactions": 25,
    "average_transaction_amount": 180.03,
    "top_transactions": [
        {"transaction_id": "1", "amount": 1000.00},
        {"transaction_id": "2", "amount": 850.00},
        {"transaction_id": "3", "amount": 500.00}
    ],
    "currency_breakdown": [
        {
            "currency": "USD",
            "average_amount": 180.03,
            "transaction_count": 25
        }
    ]
}
```

3. `DELETE /api/v1/transactions`
   - Deletes all transactions
   - Requires API key authentication

### Authentication
All endpoints require API key authentication. Include the API key in the request headers:
```
Authorization: ApiKey your-secret-api-key
```

### Running Tests
```bash
pytest src/tests/ -v
```

---

## Микросервис анализа финансовых транзакций

Микросервис для обработки и анализа финансовых транзакций, построенный на FastAPI, Redis, Celery и PostgreSQL.

### Возможности
- Обработка транзакций через REST API
- Расчет статистики в реальном времени
- Анализ топ-3 транзакций с использованием алгоритма кучи
- Разбивка транзакций по валютам
- Асинхронная обработка задач
- Аутентификация по API-ключу

### Технологический стек
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker
- SQLAlchemy

### Установка и настройка

#### Использование Docker (рекомендуется)
1. Клонируйте репозиторий:
```bash
git clone git@github.com:imelbow/TestWork006.git
cd TestWork006
```

2. Создайте файл `.env` в корневой директории и добавьте данные:
```env
DATABASE_URL=postgresql://user:password@db:5432/transactions_db
REDIS_URL=redis://redis:6379/0
API_KEY=your-secret-api-key
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=transactions_db
```

3. Соберите и запустите с помощью Docker Compose:
```bash
docker-compose up --build
```

Сервис доступен по адресу `http://localhost:8000`

#### Локальная установка для разработки
1. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройка PostgreSQL и Redis локально:

##### Установка PostgreSQL
- Установите PostgreSQL:
  ```bash
  # MacOS
  brew install postgresql@14
  brew services start postgresql@14

  # Ubuntu/Debian
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  sudo systemctl start postgresql
  sudo systemctl enable postgresql

  # Windows
  # Скачайте установщик с https://www.postgresql.org/download/windows/
  # Запустите установщик и следуйте инструкциям
  ```

- Создайте базу данных и пользователя:
  ```bash
  # Для MacOS/Linux
  sudo -u postgres psql

  # Для Windows
  # Откройте SQL Shell (psql) из меню Пуск
  ```

- В командной строке PostgreSQL:
  ```sql
  CREATE DATABASE transactions_db;
  CREATE USER user WITH PASSWORD 'password';
  GRANT ALL PRIVILEGES ON DATABASE transactions_db TO user;

  # Важный дополнительный шаг для PostgreSQL 15+
  \c transactions_db
  GRANT ALL ON SCHEMA public TO user;
  \q
  ```

Если вы не знакомы с PostgreSQL, вы можете попасть в командную строку PostgreSQL, выполнив команду `psql` или `sudo -u postgres psql` в зависимости от вашей операционной системы.

##### Установка Redis
- Установите Redis:
  ```bash
  # MacOS
  brew install redis
  brew services start redis

  # Ubuntu/Debian
  sudo apt update
  sudo apt install redis-server
  sudo systemctl start redis-server
  sudo systemctl enable redis-server

  # Windows
  # Установите Windows Subsystem for Linux (WSL2) и установите Redis там
  # Или используйте установщик Windows с https://github.com/microsoftarchive/redis/releases
  ```

- Проверьте установку Redis:
  ```bash
  redis-cli ping
  # Должен вернуть PONG
  ```

- Базовая настройка Redis (опционально):
  ```bash
  # Редактирование конфигурации Redis
  sudo nano /etc/redis/redis.conf

  # Основные настройки для рассмотрения:
  # bind 127.0.0.1
  # port 6379
  # requirepass your_password
  ```

4. Создайте файл `.env` с локальной конфигурацией:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/transactions_db
REDIS_URL=redis://localhost:6379/0
API_KEY=your-secret-api-key
```

5. Запустите сервисы:
```bash
# Терминал 1: FastAPI
uvicorn src.main:app --reload

# Терминал 2: Celery Worker
celery -A src.tasks.celery_tasks worker --loglevel=info

# Терминал 3: Celery Beat
celery -A src.tasks.celery_tasks beat --loglevel=info
```

### Документация API

API документация доступна по следующим ссылкам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Эндпоинты

1. `POST /api/v1/transactions`
   - Создает новую транзакцию
   - Требует аутентификацию по API-ключу
   - Пример тела запроса:
```json
{
    "transaction_id": "123456",
    "user_id": "user_001",
    "amount": 150.50,
    "currency": "USD",
    "timestamp": "2024-03-20T12:00:00Z"
}
```

2. `GET /api/v1/statistics`
   - Возвращает статистику по транзакциям
   - Требует аутентификацию по API-ключу
   - Пример ответа:
```json
{
    "total_transactions": 25,
    "average_transaction_amount": 180.03,
    "top_transactions": [
        {"transaction_id": "1", "amount": 1000.00},
        {"transaction_id": "2", "amount": 850.00},
        {"transaction_id": "3", "amount": 500.00}
    ],
    "currency_breakdown": [
        {
            "currency": "USD",
            "average_amount": 180.03,
            "transaction_count": 25
        }
    ]
}
```

3. `DELETE /api/v1/transactions`
   - Удаляет все транзакции
   - Требует аутентификацию по API-ключу

### Аутентификация
Все эндпоинты требуют аутентификацию по API-ключу. Включите API-ключ в заголовки запроса:
```
Authorization: ApiKey your-secret-api-key
```

### Запуск тестов
```bash
pytest src/tests/ -v
```