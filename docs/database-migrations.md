FastAPI struction
```
User Request 
    ↓
Router (路由層) - 定義 endpoints、處理 HTTP 請求
    ↓
Schema (驗證層) - 驗證輸入/輸出格式 (Pydantic)
    ↓
Service (業務邏輯層) - 處理業務邏輯（可選但推薦）
    ↓
Model (資料層) - 與資料庫溝通 (SQLAlchemy)
    ↓
Database
```


1. 每次改 Models 都要手動執行嗎？
是的，但流程很簡單：

開發流程
```
1. 修改 Model
   ↓
2. alembic revision --autogenerate -m "說明"
   ↓
3. 檢查生成的 migration 檔案（確認 SQL 正確）
   ↓
4. alembic upgrade head
   ↓
5. 資料庫更新完成
```
範例：你想在 Todo 加一個欄位
```
# 修改 app/models/todo.py
class Todo(Base):
    # ... 原有欄位
    is_urgent = Column(Boolean, default=False)  # 新增
```
然後執行：
```
alembic revision --autogenerate -m "Add is_urgent field to todos"
alembic upgrade head
```

我的建議
環境	建議做法
本地開發	手動執行（有完全控制）
測試環境	Docker 啟動時自動執行
正式環境	CI/CD pipeline 執行，或 K8s init container
重點整理
✅ 每次改 Models 都要執行 alembic revision --autogenerate + alembic upgrade head
✅ Docker 化可以自動執行，但建議正式環境用 CI/CD 控制
✅ Migration 檔案要 commit 到 Git（團隊成員才能同步）
