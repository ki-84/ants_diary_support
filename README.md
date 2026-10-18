# アリさん日記 公式サイト

公開URL: https://ki-84.github.io/ants_diary_support/

App Storeへの誘導を目的にした公式サイトです。アプリの35のApp Storeロケール（33言語、スペイン語・ポルトガル語の地域別版を含む）に対応し、各ページに翻訳済みの本文と実際の同言語のゲーム画面を静的HTMLで掲載しています。App Store Connectで2026年10月18日に175の配信地域を確認しました。

## 更新

本文の原稿は `content/locales.json`、デザインは `assets/site.css`、HTMLテンプレートは `scripts/build.py` です。

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 scripts/check.py
```

アプリリポジトリから最新の翻訳・実機画面を取り込む場合のみ、PillowをインストールしたPythonで次を実行します。アプリの `fastlane/screenshots/<locale>` に最新画面が必要です。

```sh
python3 scripts/import_app.py --app-root /path/to/ants_diary
python3 scripts/build.py
```

SNS共有カードはmacOSで再生成できます。AppKitのフォントフォールバックを使い、アラビア語やヒンディー語などの文字組みも行います。

```sh
swift -module-cache-path /tmp/ants-site-swift-cache scripts/generate_social.swift .
```

## 公開

既存のGitHub Pages設定（`main` ブランチのルート）を使います。生成HTML、画像、CSS、原稿、スクリプトをコミットしてpushすると公開されます。ビルドサービスや有料ホスティングは不要です。既存の `support*.html`、`privacy-policy*.html`、`app-ads.txt` は引き続き利用します。紹介ページのURLも既存の11ページを継続し、24ページを追加しています。

ローカル確認:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

## 検索対策と導線

- 各言語の自然な検索語をタイトル・主見出しに近い説明・本文に使用。
- 自己参照canonical、全ロケールを相互指定するhreflang、英語のx-default。
- `sitemap.xml` に紹介35ページと既存サポート・ポリシー22ページを登録。
- SoftwareApplication構造化データ。実在しない評価やレビューは掲載しません。
- 各言語専用OG画像、SNSメタデータ、iOS Smart App Banner。
- App Storeリンクは国を固定せず、訪問者のストア地域を尊重します。
- モバイル画面の下部にダウンロードボタンを常設。JavaScript無効でもリンク・言語選択・本文は機能します。

### 公開後の検索登録

Google Search ConsoleのURLプレフィックスプロパティ `https://ki-84.github.io/ants_diary_support/` で、次のサイトマップを送信すると発見を促せます。

https://ki-84.github.io/ants_diary_support/sitemap.xml

検索掲載・順位は検索エンジンが決定します。サイトの公開だけでインデックス登録や上位表示が保証されることはありません。Search Consoleへの送信・所有権確認は、この変更では実行していません。

GitHub Pagesのプロジェクト配下のrobots.txtはサイトルートのrobots.txtとして扱われないため、誤解を招く設定は追加していません。ルートのクロール制御が必要な場合は、`ki-84.github.io`側で管理してください。

アプリ側の `fastlane/build_metadata.py` と `metadata/*/marketing_url.txt` も新しい言語ページを指すよう更新しています。App Store Connectのメタデータ送信は、このサイトの公開とは別です。

参考: [Googleの多言語ページの指定方法](https://developers.google.com/search/docs/specialty/international/localized-versions)
