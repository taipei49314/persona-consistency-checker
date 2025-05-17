#!/bin/bash

# 更新 changelog function
append_changelog() {
  local TAG=$1
  local TITLE=$2
  local NOTES=$3
  local DATE=$(date +%F)

  echo -e "\n## [$TAG] - $DATE\n**標題：** $TITLE\n**說明：**\n$NOTES\n" >> CHANGELOG.md
}

# 建立 release 並同步 changelog
create_or_replace_release() {
  local TAG=$1
  local TITLE=$2
  local NOTES=$3

  echo "處理版本：$TAG"

  # 刪除舊版
  gh release delete "$TAG" -y 2>/dev/null
  git tag -d "$TAG" 2>/dev/null
  git push origin :refs/tags/"$TAG" 2>/dev/null

  # 建立新版
  gh release create "$TAG" --title "$TITLE" --notes "$NOTES"

  # 更新 changelog
  append_changelog "$TAG" "$TITLE" "$NOTES"
}

# 執行三個版本建立
create_or_replace_release "v2.0-basic" \
  "PersonaChain v2.0. 多句分析原型" \
  "最簡版，支援單句一致性分析與語氣規則，單句初步測試語氣人格，單一輸入框設計，原件僅觀測。"

create_or_replace_release "v2.2-daily" \
  "PersonaChain v2.2. 每日任務模組" \
  "每日任務機制！使用者可選擇語氣、體驗每日一句語氣挑戰，並累積一致性分數與風格客製程度。"

create_or_replace_release "v2.3-arena" \
  "PersonaChain v2.3. 人格對戰模組" \
  "支援多人語氣比對與語風分數，啟用 Persona Arena 對戰機制，可匿名比對語句，開啟語系人格分類分析資料庫。"

# 自動 commit 並推送 changelog 更新
git add CHANGELOG.md
git commit -m "Auto-update changelog after release"
git push origin main
