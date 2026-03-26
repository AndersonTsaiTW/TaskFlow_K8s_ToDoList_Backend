# GitHub Actions ECR Push Role Setup(包含OIDC Provider 設定)

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

## OIDC Provider 設定（必要）
若 Actions 出現 `No OpenIDConnect provider found for https://token.actions.githubusercontent.com`，代表 AWS 帳號還沒建立 GitHub OIDC provider。

### AWS Console 操作
1. IAM → Identity providers → Add provider
2. Provider type：`OpenID Connect`
3. Provider URL：`https://token.actions.githubusercontent.com`
4. Audience：`sts.amazonaws.com`
5. 建立後確認清單中有 `token.actions.githubusercontent.com`

### Role Trust Relationship 檢查
1. IAM → Roles → `github-actions-ecr-push-role` → Trust relationships
2. `Principal.Federated` 應為：
	`arn:aws:iam::YOUR_AWS_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com`
3. `Condition` 應包含：
	- `token.actions.githubusercontent.com:aud = sts.amazonaws.com`
	- `token.actions.githubusercontent.com:sub` 含 backend/frontend repo 的 tag pattern

## 重跑 Workflow
同一個 tag 推過後通常不會再觸發，建議推新版本 tag：

```bash
git tag v1.0.1
git push origin v1.0.1
```
