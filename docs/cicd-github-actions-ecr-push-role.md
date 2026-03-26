# GitHub Actions ECR Push Role Setup

## 目的
讓 GitHub Actions 能透過 OIDC token 推 Docker image 到 AWS ECR，不用長期金鑰。

## 建立的 Role
- **Role 名稱**：github-actions-ecr-push-role
- **Account**：YOUR_AWS_ACCOUNT_ID (ca-central-1)
- **ECR Repositories**：taskflow/api、taskflow/web

## Trust Policy
參考 ecr-policy-github.json
允許兩個 repo tag push 時使用：
- `repo:AndersonTsaiTW/TaskFlow_K8s_ToDoList_Backend:ref:refs/tags/v*`
- `repo:hengmintsao/TaskFlow_K8s_ToDoList_Frontend:ref:refs/tags/v*`

## Permissions
- Attached：`AmazonEC2ContainerRegistryPowerUser`（暫時用 managed policy，後續可換成最小權限）

## 使用流程
1. Git tag v1.0.0 → push to repo
2. GitHub Actions trigger on tag
3. Actions 用 OIDC token assume role
4. Role 允許後執行 docker build & push
5. Image push 到 ECR 對應 repo
