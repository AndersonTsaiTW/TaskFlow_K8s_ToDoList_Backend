# Cross-Account ECR Access (Friend Full Control)

## 目標
讓朋友在自己的 AWS 帳號中，透過 AssumeRole 進入你的 AWS 帳號，並可完整操作以下兩個 ECR repositories：
- `taskflow/api`
- `taskflow/web`

---

## 推薦架構（AssumeRole）
1. 你的 AWS 帳號建立角色：`taskflow-ecr-fullaccess-share`
2. 該角色 trust 朋友帳號（或朋友指定 role）可 `sts:AssumeRole`
3. 該角色掛上只限兩個 ECR repo 的完整權限 policy
4. 朋友用 AWS Console `Switch Role` 或 CLI `assume-role` 使用該角色

> 不建議直接發 Access Key。AssumeRole 比較安全、可審計、可隨時撤銷。

---

## Step 1: 你這邊建立角色權限政策（Permission Policy）(未實施)
目前直接使用 AmazonEC2ContainerRegistryPowerUser  

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRGlobalReadAuth",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:DescribeRegistry",
        "ecr:GetRegistryPolicy",
        "ecr:DescribeRepositories"
      ],
      "Resource": "*"
    },
    {
      "Sid": "FullControlTwoRepos",
      "Effect": "Allow",
      "Action": "ecr:*",
      "Resource": [
        "arn:aws:ecr:ca-central-1:YOUR_AWS_ACCOUNT_ID:repository/taskflow/api",
        "arn:aws:ecr:ca-central-1:YOUR_AWS_ACCOUNT_ID:repository/taskflow/web"
      ]
    }
  ]
}
```

---

## Step 2: 你這邊設定該角色的 Trust Policy

將 `FRIEND_AWS_ACCOUNT_ID` 換成朋友帳號（更安全可改成朋友的特定 role ARN）：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::FRIEND_AWS_ACCOUNT_ID:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

## Step 3: 朋友帳號需要的 AssumeRole 權限

朋友自己的 IAM user/role 需有：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/taskflow-ecr-fullaccess-share"
    }
  ]
}
```

---

## Console 使用方式

### 朋友在 AWS Console
1. 右上角帳號選單 → `Switch Role`
2. Account: `YOUR_AWS_ACCOUNT_ID`
3. Role: `taskflow-ecr-fullaccess-share`
4. 切換後進 ECR，就可看到並操作 `taskflow/api`、`taskflow/web`

---

## 驗證清單
- 朋友可在 ECR 清單看到兩個 repositories
- 可成功 `DescribeImages` / `PutImage` / `DeleteImage`
- 其他不在白名單的 repositories 不可操作

---

## 安全建議
- 先給 `ReadOnly` 測試，再升級到 Full Access
- Trust policy 優先限制到朋友的「特定 role ARN」而非整個 root
- 若僅需拉 image，改成 pull-only policy（避免給 `ecr:*`）
- 定期審查 CloudTrail 的 `AssumeRole` 與 ECR 操作記錄
