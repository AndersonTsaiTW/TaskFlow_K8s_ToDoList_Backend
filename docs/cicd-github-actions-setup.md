# GitHub Actions Setup Guide

## 目標
在 GitHub repo 設定 Secrets & Variables，讓 workflow 能使用 AWS OIDC token 推 image 到 ECR。

---

## Step 1: 設定 Secrets & Variables

### 位置
進你的 backend repo → **Settings** → **Secrets and variables** → **Actions**

### 新增 Variable（公開資訊）
| 名稱 | 值 |
|------|-----|
| `AWS_REGION` | `ca-central-1` |

### 新增 Secret（不公開）
| 名稱 | 值 |
|------|-----|
| `AWS_ROLE_ARN` | `arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/github-actions-ecr-push-role` |

---

## Step 2: 推送 Workflow 檔案

Workflow 檔案位置：`.github/workflows/build-and-push-ecr.yml`

執行指令：
```bash
git add .github/workflows/build-and-push-ecr.yml
git commit -m "ci: add ECR build and push workflow"
git push origin main
```

---

## Step 3: 測試發版流程

### 3.1 本地建立 tag
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 3.2 監看執行狀態
進 repo → **Actions** tab → 看新的 workflow 執行狀況

### 3.3 檢查 ECR
AWS Console → ECR → `taskflow/api` repository
應該能看到新 image：`taskflow/api:v1.0.0`

---

## Workflow 運作流程

```
1. git tag v1.0.0
   ↓
2. git push origin v1.0.0
   ↓
3. GitHub 偵測到 tag push，觸發 workflow
   ↓
4. Workflow 執行：
   - Checkout 程式碼
   - 用 OIDC token assume AWS role
   - 登入 ECR
   - Build Docker image (tag = v1.0.0)
   - Push 到 ECR
   ↓
5. Image 在 ECR 可用：
   YOUR_AWS_ACCOUNT_ID.dkr.ecr.ca-central-1.amazonaws.com/taskflow/api:v1.0.0
```

---

## 常見問題排查

### ❌ Actions 報錯：`InvalidAuthorizationTokenException`
- 檢查 `AWS_ROLE_ARN` 是否正確
- 檢查 Role trust policy 是否包含你的 repo

### ❌ Actions 卡住：`OIDC token validation failed`
- 確認 AWS IAM 有建立 GitHub OIDC provider
- 重新檢查 `AWS_ROLE_ARN` 格式

### ❌ ECR push 失敗
- 檢查 Role 權限是否有 ECR push 權限
- 確認 `ECR_REPOSITORY` 值（應為 `taskflow/api`）

---

## 前端 Repo 設定

如果前端 repo（`hengmintsao/TaskFlow_K8s_ToDoList_Frontend`）要推 `taskflow/web` image：

1. copy 相同的 `.github/workflows/build-and-push-ecr.yml`
2. 改 `ECR_REPOSITORY: taskflow/web`（原本是 `taskflow/api`）
3. 在前端 repo 設同樣的 `AWS_REGION` 和 `AWS_ROLE_ARN`
4. 發版時流程相同：`git tag → git push origin TAG`

---

## 相關文件
- [ci-cd-pipeline.md](ci-cd-pipeline.md) - 整體流程
- [cicd-github-actions-ecr-push-role.md](cicd-github-actions-ecr-push-role.md) - IAM Role 設定
