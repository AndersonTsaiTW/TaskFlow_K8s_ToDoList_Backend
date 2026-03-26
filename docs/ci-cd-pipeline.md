# CI/CD Pipeline Setup: ECR + GitHub Actions

## 目標
1. 推送 Docker image 到 AWS ECR
2. 版本號由 Git tag 控制
3. GitHub Actions 自動觸發 build & push
4. Image tag = Git tag（例：v1.3.0）

---

## 流程圖
```
Git Push Tag (v1.3.0)
    ↓
GitHub Actions Triggered (on: push.tags)
    ↓
Build Dockerfile
    ↓
Assume IAM Role (OIDC)
    ↓
Login ECR
    ↓
Push Image: [ECR_REGISTRY]/taskflow/api:v1.3.0
    ↓
Image Available in ECR
```

---

## 已完成：AWS IAM 設置

### 1. Role 建立
- **Name**: `github-actions-ecr-push-role`
- **Account**: YOUR_AWS_ACCOUNT_ID (ca-central-1)
- 詳見：[cicd-github-actions-ecr-push-role.md](cicd-github-actions-ecr-push-role.md)

### 2. IAM Policy
- **Permissions**: `AmazonEC2ContainerRegistryPowerUser`（managed policy）
- ECR repositories 支援：`taskflow/api`、`taskflow/web`
- 詳見：[cicd-github-actions-ecr-push-role.md](cicd-github-actions-ecr-push-role.md)

### 3. Trust Policy
- Trust GitHub OIDC provider
- 支援兩個 repo：
  - `AndersonTsaiTW/TaskFlow_K8s_ToDoList_Backend` (backend)
  - `hengmintsao/TaskFlow_K8s_ToDoList_Frontend` (frontend)

---

## 待完成：GitHub Actions 設置

### 1. Repository Secrets/Variables
- [x] `AWS_REGION`: ca-central-1
- [x] `AWS_ROLE_ARN`: arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/github-actions-ecr-push-role
  - 詳見：[cicd-github-actions-setup.md](cicd-github-actions-setup.md#step-1-設定-secrets--variables)

### 2. Workflow 檔案
- [x] `.github/workflows/build-and-push-ecr.yml`
  - Trigger: `on: push.tags: ['v*.*.*']`
  - Build image with tag = `github.ref_name`
  - Push to ECR
  - 詳見：[cicd-github-actions-setup.md](cicd-github-actions-setup.md)

### 3. 本地發版指令
```bash
git tag v1.0.0
git push origin v1.0.0
```
→ 自動觸發 Actions → image 推到 ECR

---

## ECR 位置
- Backend: `YOUR_AWS_ACCOUNT_ID.dkr.ecr.ca-central-1.amazonaws.com/taskflow/api:TAG`
- Frontend: `YOUR_AWS_ACCOUNT_ID.dkr.ecr.ca-central-1.amazonaws.com/taskflow/web:TAG`

---

## 後續步驟
1. GitHub repo 設定上述 Secrets/Variables
2. 建立 Workflow YAML 檔（`.github/workflows/build-and-push-ecr.yml`）
3. 測試發版：tag push → check Actions logs → verify ECR image
