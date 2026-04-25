# 測試實施計畫

## 目的

這份文件記錄 TaskFlow backend repo 的測試實施計畫。
目標是在 Docker image build 與 Kubernetes 部署之前，由 backend repo 先負責驗證應用程式行為是否正確。

Kubernetes repo 應該專注在 deployment manifests、runtime configuration injection、probes，以及 cluster-level verification。這個 backend repo 則應該負責 app tests、API tests，以及 CI test workflow。

## 範圍

### 此 Backend Repo 負責

- 使用 `pytest` 測試 backend 邏輯
- 使用 `hurl` 測試 API endpoint
- 提供一支 shell script 執行本機 CI 測試流程
- 在 Docker image build/push 前執行 GitHub Actions test job
- 使用環境變數驅動測試設定

### Kubernetes Repo 負責

- ConfigMap 與 Secret 定義
- Deployment、Service、Ingress 與 probe 設定
- Image tag 參數化
- 部署後的 cluster smoke checks

## 測試分層

### 1. Backend Logic Tests: pytest

目的：

- 不依賴完整瀏覽器流程，直接驗證 Python application 行為。
- 在可行範圍內覆蓋 service logic、schemas、auth helpers、database access patterns，以及 FastAPI route behavior。

規劃位置：

```text
tests/
  conftest.py
  test_health.py
  test_auth.py
  test_todos.py
```

初始測試目標：

- `GET /healthz` 回傳 `{"status": "ok"}`
- `GET /readyz` 回傳 `{"status": "ready"}`
- 使用有效資料可以成功註冊 user
- 重複註冊會回傳錯誤
- Login 會回傳 bearer token
- 建立 todo 需要 authentication
- 已登入 user 可以建立、列出、更新、刪除自己的 todos

實作備註：

- 使用 FastAPI `TestClient` 做 route-level tests。
- 優先使用隔離的 test database。
- 透過 `DATABASE_URL` 設定 test database。
- CI 不應依賴開發者本機的 `.env` 檔案。

預期指令：

```bash
pytest
```

## 2. API Endpoint Tests: hurl

目的：

- 以「正在執行的 HTTP service」形式驗證 backend。
- 從外部呼叫 API，接近 CI、Docker、Kubernetes smoke tests 實際呼叫 backend 的方式。

規劃位置：

```text
hurl/
  health.hurl
  auth.hurl
  todos.hurl
```

初始測試目標：

- `GET /healthz`
- `GET /readyz`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/todos`
- `GET /api/v1/todos`
- `PATCH /api/v1/todos/{todo_id}`
- `DELETE /api/v1/todos/{todo_id}`

實作備註：

- 使用 `HURL_BASE_URL` 或類似環境變數，讓同一批 hurl files 可以同時在本機與 CI 執行。
- 盡量產生唯一的測試 email，避免 duplicate-user conflicts。
- 從 login response 取得 auth token，並在需要 authentication 的 request 中重複使用。
- hurl files 只專注在 endpoint contract、HTTP status，以及 response body assertions。

預期指令：

```bash
hurl --test hurl/*.hurl
```

## 3. Optional End-To-End Tests: Playwright

目的：

- 從使用者角度驗證完整網站流程。
- 對 backend repo 來說這是 optional，因為 backend 本身沒有 frontend UI。

建議歸屬：

- Frontend repo 或獨立的 end-to-end test repo。
- 只有當這個 repo 未來包含 web UI，或有可靠的 docker-compose 設定可以同時啟動 frontend、backend、database 時，才建議把 Playwright 放在這裡。

可能流程：

- 開啟 TaskFlow web app
- 註冊或登入
- 建立 todo
- 編輯 todo
- 標記為完成
- 刪除 todo

## 4. Shell Script Flow

目的：

- 提供一個本機指令，用來模擬 CI test sequence。
- 讓開發者在 push 前可以方便執行同樣的檢查。

規劃位置：

```text
scripts/
  ci-test.sh
```

規劃流程：

```text
1. 安裝或確認 dependencies
2. 啟動必要服務，通常是透過 docker compose 啟動 PostgreSQL
3. 執行 database migrations
4. 執行 pytest
5. 啟動 API server
6. 等待 /readyz
7. 執行 hurl API tests
8. 如果 script 有啟動背景服務，結束時停止它們
```

預期指令：

```bash
bash scripts/ci-test.sh
```

實作備註：

- Script 應使用 `set -euo pipefail`，遇到錯誤立即失敗。
- Database URL、API base URL、host、port 都應使用環境變數設定。
- Cleanup logic 要可靠，避免本機測試後留下背景程序。

## CI 實施計畫

### 建議的 GitHub Actions Jobs

```text
test
  -> checkout
  -> setup Python
  -> install Python dependencies
  -> start PostgreSQL service
  -> run migrations
  -> run pytest
  -> install hurl
  -> start API
  -> wait for readiness
  -> run hurl tests

build-and-push
  -> only runs after test passes
  -> builds Docker image
  -> pushes image to ECR
```

目前狀態：

- `.github/workflows/build-and-push-ecr.yml` 會在 version tags 建立並 push image。
- 仍需要加入 test job。

目標行為：

- Pull requests 與 push 到 `main` 時應執行 tests。
- Version tags 應先執行 tests，通過後才 build and push image。
- 如果 tests 失敗，不應發布 image。

## 環境參數化

Tests 與 CI 應避免硬編碼本機值。規劃使用的變數如下：

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | Backend database connection | `postgresql://taskflow:password@localhost:5432/taskflow_test` |
| `TEST_DATABASE_URL` | Optional dedicated test DB URL | `postgresql://taskflow:password@localhost:5432/taskflow_test` |
| `HURL_BASE_URL` | hurl 測試用的 running API base URL | `http://localhost:8000` |
| `HOST` | API bind host | `0.0.0.0` |
| `PORT` | API port | `8000` |
| `ALLOWED_ORIGINS` | CORS origins | `http://localhost:3000,http://localhost:8000` |
| `SECRET_KEY` | test/prod 使用的 JWT signing key | `test-secret-key` |

## 建議實作順序

1. 新增 `pytest` test structure 與 health endpoint tests。
2. 使用隔離的 database setup 新增 auth 與 todo tests。
3. 新增 hurl health/auth/todo endpoint tests。
4. 新增 `scripts/ci-test.sh`，執行完整本機 test flow。
5. 新增 GitHub Actions test workflow。
6. 更新既有 ECR workflow，讓 image build/push 依賴 tests 通過。
7. 決定 Playwright 應放在 frontend repo，或留到之後的 e2e setup。

## Definition Of Done

- `pytest` 在本機與 GitHub Actions 都通過。
- `hurl --test hurl/*.hurl` 可以針對 running API 通過。
- `bash scripts/ci-test.sh` 可以在本機執行相同核心流程。
- GitHub Actions 會在 tests 失敗時阻止 image publishing。
- `.env.example` 記錄測試所需的環境變數。
- Kubernetes repo 使用已測試通過的 image，並只處理 deployment-specific checks。
